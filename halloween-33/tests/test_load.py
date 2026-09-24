"""Tests for load.py against a fake Blotato. Run: python3 halloween-33/tests/test_load.py"""
import copy, json, os, sys, unittest
from unittest import mock
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import load

QUEUE = json.load(open(os.path.join(HERE, '..', 'backup', 'queue-2026-09-23-full.json')))
SCHED = json.load(open(os.path.join(HERE, '..', 'schedule.json')))


class FakeBlotato:
    def __init__(self):
        self.q = copy.deepcopy(QUEUE)
        self.calls = []

    def __call__(self, method, path, key, body=None, query=None):
        self.calls.append((method, path))
        if method == 'GET':
            return {'items': self.q, 'cursor': None}
        if method == 'DELETE':
            self.q = [x for x in self.q if x['id'] != path.rsplit('/', 1)[-1]]
            return {}
        if method == 'POST':
            p = body['post']
            self.q.append({'id': f'new{len(self.q)}', 'scheduledAt': body['scheduledTime'],
                           'draft': {'accountId': p['accountId'], 'content': p['content']}})
            return {'postSubmissionId': 'x'}
        if method == 'PATCH':
            x = [x for x in self.q if x['id'] == path.rsplit('/', 1)[-1]][0]
            x['scheduledAt'] = body['patch']['scheduledTime']
            return {}


def run(fake, now, execute=True, days=7):
    argv = ['load.py', '--now', now, '--days', str(days)] + (['--execute'] if execute else [])
    with mock.patch.object(load, 'api', fake), mock.patch.object(sys, 'argv', argv), \
            mock.patch.dict(os.environ, {'BLOTATO_API_KEY': 'k'}), mock.patch('builtins.print'):
        try:
            load.main()
        except SystemExit:
            pass


def with_media():
    s = copy.deepcopy(SCHED)
    for p in s['posts']:
        p['mediaUrl'] = p['mediaUrl'] or 'https://example/x.mp4'
    return s


class Loader(unittest.TestCase):
    def setUp(self):
        self.p = mock.patch('json.load', side_effect=self._load)
        self.p.start()

    def tearDown(self):
        self.p.stop()

    def _load(self, f):
        if f.name.endswith('schedule.json'):
            return with_media()
        return json.loads(f.read())

    def test_first_week_loads_and_replaces_old_repeats(self):
        fake = FakeBlotato()
        run(fake, '2026-09-24T12:00:00+00:00')
        posts = [c for c in fake.calls if c[0] == 'POST']
        dels = [c for c in fake.calls if c[0] == 'DELETE']
        # trailer (4) + nights 1 to 7 by Oct 1 12:00 UTC window: nights 1-2 fully, trailer
        self.assertGreater(len(posts), 0)
        self.assertGreater(len(dels), 0)
        self.assertLessEqual(len(fake.q), 200)
        ids = {x['id'] for x in fake.q}
        for keep in ('4459039', '4459043', '4137937', '4137938'):
            self.assertIn(keep, ids)

    def test_second_run_is_a_no_op(self):
        fake = FakeBlotato()
        run(fake, '2026-09-24T12:00:00+00:00')
        n = len(fake.q)
        fake.calls.clear()
        run(fake, '2026-09-24T13:00:00+00:00')
        self.assertEqual([c for c in fake.calls if c[0] in ('POST', 'DELETE')], [])
        self.assertEqual(len(fake.q), n)

    def test_propose_only_writes_nothing(self):
        fake = FakeBlotato()
        run(fake, '2026-09-24T12:00:00+00:00', execute=False)
        self.assertEqual([c for c in fake.calls if c[0] != 'GET'], [])

    def test_never_goes_over_200(self):
        fake = FakeBlotato()
        import datetime as dt
        day = dt.datetime(2026, 9, 24, 12, tzinfo=dt.timezone.utc)
        while day.month < 11:
            run(fake, day.isoformat())
            self.assertLessEqual(len(fake.q), 200)
            day += dt.timedelta(days=1)
        loaded = {p['key'] for p in SCHED['posts']
                  if any(x['draft']['content'].get('text') == p['text'] for x in fake.q)}
        self.assertGreater(len(loaded), 0)

    def test_samhain_is_retimed_to_6pm(self):
        fake = FakeBlotato()
        run(fake, '2026-10-25T12:00:00+00:00')
        s = [x for x in fake.q if x['id'] == '4137937'][0]
        self.assertEqual(s['scheduledAt'][:16], '2026-10-31T23:00')

    def test_every_night_is_in_the_schedule_once_per_platform(self):
        keys = [p['key'] for p in SCHED['posts']]
        self.assertEqual(len(keys), len(set(keys)))
        nights = {p['night'] for p in SCHED['posts'] if p['night']}
        self.assertEqual(nights, set(range(1, 34)))


class Requests(unittest.TestCase):
    def test_delete_sends_no_json_content_type(self):
        seen = {}

        def fake_open(req, timeout=0):
            seen.update(method=req.get_method(), ctype=req.get_header('Content-type'), data=req.data)
            class R:
                def __enter__(s): return s
                def __exit__(s, *x): pass
                def read(s): return b''
            return R()
        with mock.patch('urllib.request.urlopen', fake_open):
            load.api('DELETE', '/schedules/1', 'k')
        self.assertEqual(seen['method'], 'DELETE')
        self.assertIsNone(seen['ctype'])
        self.assertIsNone(seen['data'])
        with mock.patch('urllib.request.urlopen', fake_open):
            load.api('POST', '/posts', 'k', body={'a': 1})
        self.assertEqual(seen['ctype'], 'application/json')


if __name__ == '__main__':
    unittest.main(verbosity=1)
