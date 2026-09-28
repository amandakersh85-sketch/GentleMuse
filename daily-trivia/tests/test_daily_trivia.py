#!/usr/bin/env python3
"""Tests for the daily trivia job. No network, no HeyGen spend, no posts.

A fake HeyGen CLI and a fake Blotato server stand in for the real ones, so the
whole day runs: pick, gate, render, host, package, schedule.

  python3 daily-trivia/tests/test_daily_trivia.py
"""
import contextlib, datetime as dt, io, json, os, shutil, sys, tempfile, threading, unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(ROOT, 'filing-system', 'scripts'))
BANK = os.path.join(ROOT, 'filing-system', 'tests', 'trivia-pick.bank.csv')
SOURCES = os.path.join(ROOT, 'filing-system', 'tests', 'trivia.sources.csv')

FAKE_HEYGEN = r'''#!/usr/bin/env python3
import json, os, sys
log = os.environ['FAKE_HEYGEN_LOG']
mode = os.environ.get('FAKE_HEYGEN_MODE', 'ok')
args = sys.argv[1:]
with open(log, 'a') as f:
    f.write(json.dumps(args) + '\n')
if args[:2] == ['video', 'create']:
    if mode == 'refused':   # the real CLI v0.8.1: the error as JSON on stderr, exit 3
        sys.stderr.write(json.dumps({'error': {'code': 'insufficient_credit', 'message': 'insufficient API credits',
                                               'hint': 'Top up at https://app.heygen.com'}}) + '\n')
        sys.exit(3)
    print(json.dumps({'data': {'video_id': 'vid_123', 'status': 'pending'}}))
elif args[:2] == ['video', 'get']:
    n = sum(1 for line in open(log) if '"get"' in line)
    if mode == 'failed':
        print(json.dumps({'data': {'id': args[2], 'status': 'failed', 'failure_message': 'avatar not found'}}))
    elif n < 2:
        print(json.dumps({'data': {'id': args[2], 'status': 'processing'}}))
    else:
        print(json.dumps({'data': {'id': args[2], 'status': 'completed', 'duration': 21.5,
                                   'video_url': 'https://files.heygen.com/video/vid_123.mp4?expires=1'}}))
'''

HOSTED = 'https://database.blotato.io/storage/v1/object/public/public_media/x/trivia-vid_123.mp4'


class Blotato(BaseHTTPRequestHandler):
    """The 4 endpoints the job touches, with what it sent kept for the tests."""
    queue, published, sent = [], [], []

    def log_message(self, *a):
        pass

    def reply(self, code, obj):
        raw = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.headers.get('blotato-api-key') != 'bk':
            return self.reply(401, {'message': 'bad key'})
        if self.path.startswith('/v2/schedules'):
            return self.reply(200, {'items': Blotato.queue})
        if self.path.startswith('/v2/posts'):
            return self.reply(200, {'items': Blotato.published})
        self.reply(404, {})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
        Blotato.sent.append((self.path, body))
        if self.path == '/v2/media':
            return self.reply(201, {'url': HOSTED})
        if self.path == '/v2/posts':
            return self.reply(201, {'postSubmissionId': 'sub-%d' % len(Blotato.sent)})
        self.reply(404, {})


def queued(platform, account, at, media='other.mp4'):
    return {'id': 'q-%s-%s' % (platform, at), 'scheduledAt': at,
            'draft': {'accountId': account, 'content': {'platform': platform, 'text': 'x',
                                                        'mediaUrls': ['https://x/' + media]}}}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Blotato)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        os.environ['BLOTATO_API_BASE'] = 'http://127.0.0.1:%d/v2' % cls.server.server_port
        global make, schedule
        import make, schedule  # noqa: E401  imported after the base url is set
        make.BLOTATO = schedule.API = os.environ['BLOTATO_API_BASE']

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.approved = os.path.join(self.tmp, 'approved')
        self.out = os.path.join(self.tmp, 'out')
        self.heygen = os.path.join(self.tmp, 'heygen')
        with open(self.heygen, 'w') as f:
            f.write(FAKE_HEYGEN.replace('#!/usr/bin/env python3', '#!' + sys.executable, 1))
        os.chmod(self.heygen, 0o755)
        self.log = os.path.join(self.tmp, 'heygen.log')
        os.environ.update(FAKE_HEYGEN_LOG=self.log, FAKE_HEYGEN_MODE='ok',
                          HEYGEN_API_KEY='hk', BLOTATO_API_KEY='bk',
                          GITHUB_OUTPUT=os.path.join(self.tmp, 'gh-output'))
        Blotato.queue, Blotato.published, Blotato.sent = [], [], []

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_make(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = make.main(['--bank', BANK, '--sources', SOURCES, '--approved', self.approved,
                              '--out', self.out, '--heygen', self.heygen, '--poll-seconds', '0',
                              '--date', '2026-09-30'] + list(extra))
        return code, buf.getvalue()

    def heygen_calls(self):
        if not os.path.exists(self.log):
            return []
        with open(self.log) as f:
            return [json.loads(line) for line in f]

    def made(self):
        return sorted(os.listdir(self.approved)) if os.path.isdir(self.approved) else []


class Make(Base):
    def test_nothing_is_made_without_execute(self):
        code, out = self.run_make()
        self.assertEqual(code, 0)
        self.assertIn('PROPOSED', out)
        self.assertEqual(self.heygen_calls(), [])
        self.assertEqual(self.made(), [])
        self.assertEqual(Blotato.sent, [])

    def test_a_day_is_rendered_hosted_and_packaged(self):
        code, out = self.run_make('--execute')
        self.assertEqual(code, 0, out)
        calls = self.heygen_calls()
        self.assertEqual(calls[0][:3], ['video', 'create', '-d'])
        req = json.loads(calls[0][3])
        self.assertEqual(req['type'], 'avatar')
        self.assertIn(req['avatar_id'], ('3243536278874919a784ed66c135a473', '96af09cd10804111a290ecb70f39500f'))
        self.assertEqual(req['voice_id'], '05f19352e8f74b0392a8f411eba40de1')
        self.assertEqual(req['voice_settings'], {'speed': 0.92})
        self.assertEqual(req['aspect_ratio'], '9:16')
        self.assertTrue(req['script'].startswith('The paper that started the current wave of AI'))
        self.assertTrue(req['script'].endswith('You are not late to this.'))
        self.assertEqual([c[:2] for c in calls[1:]], [['video', 'get']] * (len(calls) - 1))
        self.assertEqual(Blotato.sent, [('/v2/media', {'url': 'https://files.heygen.com/video/vid_123.mp4?expires=1'})])

        self.assertEqual(self.made(), ['2026-09-30-TRV-001.json'])
        with open(os.path.join(self.approved, self.made()[0])) as f:
            pkg = json.load(f)
        self.assertEqual(pkg['video'], {'heygenVideoId': 'vid_123', 'duration': 21.5, 'url': HOSTED})
        with open(os.path.join(self.out, 'pr-body.md')) as f:
            body = f.read()
        self.assertIn(HOSTED, body)
        self.assertIn('Merge to approve', body)
        for p in pkg['posts']:
            self.assertIn(p['text'], body)
        with open(os.environ['GITHUB_OUTPUT']) as f:
            gh = f.read()
        self.assertIn('made=true', gh)
        self.assertIn('branch=daily-trivia/2026-09-30-TRV-001', gh)
        self.assertIn('title=Daily trivia for Wed 09/30: TRV-001', gh)

    def test_a_day_already_made_gets_its_pr_text_without_a_new_video(self):
        self.run_make('--execute')
        path = os.path.join(self.approved, self.made()[0])
        os.remove(os.path.join(self.out, 'pr-body.md'))
        before = len(self.heygen_calls())
        code, _ = self.run_make('--pr-body', path)
        self.assertEqual(code, 0)
        self.assertEqual(len(self.heygen_calls()), before)
        with open(os.path.join(self.out, 'pr-body.md')) as f:
            self.assertIn(HOSTED, f.read())

    def test_the_captions_follow_the_board(self):
        self.run_make('--execute')
        with open(os.path.join(self.approved, self.made()[0])) as f:
            pkg = json.load(f)
        text = {p['platform']: p['text'] for p in pkg['posts']}
        self.assertEqual(sorted(text), ['facebook', 'instagram', 'tiktok', 'youtube'])
        self.assertIn("Comment TUESDAY and I'll send you the weekly note.", text['instagram'])
        self.assertIn('https://just-another-tuesday-gm.subscribepage.io', text['facebook'])
        self.assertNotIn('TUESDAY', text['tiktok'])
        self.assertIn('The note is in my bio.', text['tiktok'])
        self.assertNotIn('Comment', text['youtube'])
        self.assertIn('1 email a week:\nhttps://just-another-tuesday-gm.subscribepage.io', text['youtube'])
        for t in text.values():
            self.assertNotIn('—', t)
        by = {p['platform']: p for p in pkg['posts']}
        self.assertEqual((by['instagram']['mediaType'], by['instagram']['shareToFeed']), ('reel', True))
        self.assertEqual(by['facebook']['pageId'], '1086399221215093')
        self.assertEqual(by['youtube']['title'],
                         'The paper that started the current wave of AI is called Attention Is All You Need')

    def test_an_approved_fact_is_not_made_again(self):
        os.makedirs(self.approved)
        with open(os.path.join(self.approved, '2026-09-29-TRV-001.json'), 'w') as f:
            json.dump({'factId': 'TRV-001'}, f)
        code, out = self.run_make()
        self.assertEqual(code, 0)
        self.assertIn('passed over TRV-001, already approved or declined', out)
        self.assertIn('"factId": "TRV-002"', out)

    def test_a_declined_fact_is_not_made_again(self):
        code, out = self.run_make('--skip', 'TRV-001')
        self.assertIn('"factId": "TRV-002"', out)

    def test_an_empty_bank_holds(self):
        code, out = self.run_make('--skip', 'TRV-001,TRV-002,TRV-006')
        self.assertEqual(code, 2)
        self.assertIn('Nothing to send', out)
        self.assertEqual(self.heygen_calls(), [])

    def test_a_dead_keyword_stops_before_anything_is_paid_for(self):
        code, out = self.run_make('--execute', '--fact', 'TRV-006')
        self.assertEqual(code, 1)
        self.assertIn('NOPE', out)
        self.assertEqual(self.heygen_calls(), [])

    def test_a_number_nobody_checked_stops_the_day(self):
        # Somebody edits an ask to carry a figure. T03 finds it before a render is paid for.
        import csv
        import gm_trivia_bank as B
        import gm_trivia_pick as P
        cta = os.path.join(self.tmp, 'trivia-cta.csv')
        with open(P.TRIVIA_CTA, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        rows[0]['Line'] = 'Join 4000 readers. ' + rows[0]['Line']
        with open(cta, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        pkg, code, lines = P.build(B.load_bank(BANK), dt.date(2026, 9, 30), sources=SOURCES, cta=cta)
        self.assertIsNone(pkg)
        self.assertEqual(code, 1)
        self.assertTrue(any('T03_NUMBER_NOT_IN_BANK' in line and '4000' in line for line in lines), lines)

    def test_a_refused_render_writes_nothing(self):
        os.environ['FAKE_HEYGEN_MODE'] = 'refused'
        code, out = self.run_make('--execute')
        self.assertEqual(code, 2)
        self.assertIn('insufficient_credit: insufficient API credits', out)
        self.assertNotIn('Top up', out)
        self.assertEqual(self.made(), [])
        self.assertEqual(Blotato.sent, [])

    def test_a_failed_render_writes_nothing(self):
        os.environ['FAKE_HEYGEN_MODE'] = 'failed'
        code, out = self.run_make('--execute')
        self.assertEqual(code, 2)
        self.assertIn('avatar not found', out)
        self.assertEqual(self.made(), [])

    def test_no_key_makes_nothing(self):
        del os.environ['HEYGEN_API_KEY']
        code, out = self.run_make('--execute')
        self.assertEqual(code, 2)
        self.assertIn('HEYGEN_API_KEY', out)
        self.assertEqual(self.heygen_calls(), [])


class Schedule(Base):
    NOW = '2026-09-30T14:00:00+00:00'   # 9:00 AM Central

    def package(self, fact='TRV-001'):
        self.run_make('--execute', '--fact', fact)
        return os.path.join(self.approved, '2026-09-30-%s.json' % fact)

    def run_schedule(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = schedule.main(['--now', self.NOW, '--approved', self.approved] + list(args))
        return code, buf.getvalue()

    def posts_sent(self):
        return [b for path, b in Blotato.sent if path == '/v2/posts']

    def test_nothing_is_sent_without_execute(self):
        path = self.package()
        code, out = self.run_schedule(path)
        self.assertEqual(code, 0, out)
        self.assertEqual(out.count('Would schedule'), 4)
        self.assertEqual(self.posts_sent(), [])

    def test_an_approved_day_becomes_4_timed_posts(self):
        path = self.package()
        code, out = self.run_schedule('--execute', path)
        self.assertEqual(code, 0, out)
        sent = self.posts_sent()
        self.assertEqual(sorted(b['post']['target']['targetType'] for b in sent),
                         ['facebook', 'instagram', 'tiktok', 'youtube'])
        for b in sent:
            self.assertTrue(b['scheduledTime'], 'a post without a time publishes at once')
            self.assertEqual(b['post']['content']['mediaUrls'], [HOSTED])
            # 9:00 AM Central now, so the first slot an hour out is 12:00 PM Central
            self.assertEqual(b['scheduledTime'], '2026-09-30T17:00:00Z')
        t = {b['post']['target']['targetType']: b['post']['target'] for b in sent}
        self.assertTrue(t['tiktok']['isAiGenerated'])
        self.assertEqual(t['tiktok']['privacyLevel'], 'PUBLIC_TO_EVERYONE')
        self.assertEqual(t['youtube']['privacyStatus'], 'public')
        self.assertEqual(t['facebook']['pageId'], '1086399221215093')
        self.assertTrue(t['instagram']['shareToFeed'])

    def test_it_keeps_2_hours_from_her_other_posts(self):
        path = self.package()
        Blotato.queue = [queued('instagram', '45886', '2026-09-30T18:30:00.000Z'),   # 1:30 PM Central
                         queued('tiktok', '41488', '2026-09-30T16:00:00.000Z')]      # 11:00 AM Central
        self.run_schedule('--execute', path)
        at = {b['post']['target']['targetType']: b['scheduledTime'] for b in self.posts_sent()}
        self.assertEqual(at['instagram'], '2026-09-30T21:00:00Z')   # 4:00 PM, the first clear slot
        self.assertEqual(at['tiktok'], '2026-09-30T19:30:00Z')      # 2:30 PM
        self.assertEqual(at['youtube'], '2026-09-30T17:00:00Z')

    def test_a_late_approval_goes_to_tomorrow_morning(self):
        path = self.package()
        self.NOW = '2026-09-30T21:30:00+00:00'   # 4:30 PM Central, every slot today has gone
        self.run_schedule('--execute', path)
        self.assertEqual({b['scheduledTime'] for b in self.posts_sent()}, {'2026-10-01T14:30:00Z'})

    def test_nothing_is_scheduled_twice(self):
        path = self.package()
        Blotato.queue = [queued('instagram', '45886', '2026-10-01T14:30:00.000Z', media='trivia-vid_123.mp4')]
        Blotato.published = [{'platform': 'tiktok', 'mediaUrls': [HOSTED]}]
        code, out = self.run_schedule('--execute', path)
        self.assertEqual(code, 0, out)
        self.assertEqual(sorted(b['post']['target']['targetType'] for b in self.posts_sent()), ['facebook', 'youtube'])
        self.assertEqual(out.count('Already queued or published'), 2)

    def test_the_halloween_countdown_keeps_its_room(self):
        path = self.package()
        Blotato.queue = [queued('linkedin', '20723', '2026-10-%02dT%02d:00:00.000Z' % (1 + i // 20, i % 20))
                         for i in range(187)]
        code, out = self.run_schedule('--execute', path)
        self.assertEqual(code, 1)
        self.assertIn('10 stay free for the Halloween countdown', out)
        self.assertEqual(self.posts_sent(), [])

    def test_a_package_with_no_video_is_refused(self):
        os.makedirs(self.approved, exist_ok=True)
        path = os.path.join(self.approved, '2026-09-30-TRV-009.json')
        with open(path, 'w') as f:
            json.dump({'factId': 'TRV-009', 'posts': []}, f)
        code, out = self.run_schedule('--execute', path)
        self.assertEqual(code, 1)
        self.assertIn('no video', out)

    def test_no_key_schedules_nothing(self):
        path = self.package()
        del os.environ['BLOTATO_API_KEY']
        code, out = self.run_schedule('--execute', path)
        self.assertEqual(code, 2)
        self.assertEqual(self.posts_sent(), [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
