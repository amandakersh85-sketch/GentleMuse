"""Tests for refill.py. Run: python3 blotato-refill/tests/test_refill.py"""
import datetime as dt, json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import refill

NOW = dt.datetime(2026, 10, 5, 12, 0)  # a Monday


def make_lib(w1_rows, w2_rows=(), w1_log=(), validator_ok=True):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'content'))
    os.makedirs(os.path.join(d, 'scripts'))
    for wave, rows in (('wave1', w1_rows), ('wave2', w2_rows)):
        with open(os.path.join(d, 'content', f'{wave}-staging-library.txt'), 'w') as f:
            f.write('header\n=== ROWS ===\n' + '\n'.join(rows) + '\n')
    with open(os.path.join(d, 'content', 'wave1-loaded.log'), 'w') as f:
        f.write('# log\n' + ''.join(f'{i} loaded 2026-09-01\n' for i in w1_log))
    with open(os.path.join(d, 'scripts', 'validate-wave.py'), 'w') as f:
        f.write('import sys\n' + ('' if validator_ok else 'print("  FAIL  broken"); sys.exit(1)\n'))
    return d


def q(platform, at, text='other post', media='x.jpg', account=None):
    return dict(id='1', accountId=account or refill.ACCOUNTS[platform], platform=platform,
                scheduledAt=at + ':00.000Z', text=text, media=media)


def run(lib, queue, reserve=0):
    loads, rep = refill.plan(lib, queue, NOW, reserve=reserve)
    return {x['row']['id']: x for x in loads}, rep


class Plan(unittest.TestCase):
    def test_places_row_at_its_own_time(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 10, 6, 15, 0))

    def test_tiktok_cap_moves_to_next_day_same_slot(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, rep = run(lib, [q('tiktok', '2026-10-06T19:00')])
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 10, 7, 15, 0))
        self.assertEqual(len(rep['moved']), 1)

    def test_halloween_evening_post_does_not_use_up_the_cap(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, _ = run(lib, [q('tiktok', '2026-10-06T23:00')])
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 10, 6, 15, 0))

    def test_halloween_evening_post_still_holds_its_timestamp(self):
        lib = make_lib(['GW0001|2026-10-06T23:00|instagram|a.jpg|-|hello'])
        got, _ = run(lib, [q('instagram', '2026-10-06T23:00')])
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 10, 6, 15, 0))

    def test_instagram_weekend_cap_is_1(self):
        lib = make_lib(['GW0001|2026-10-10T23:00|instagram|a.jpg|-|hello'])  # Saturday
        got, _ = run(lib, [q('instagram', '2026-10-10T15:00')])
        self.assertEqual(got['GW0001']['at'].date(), dt.date(2026, 10, 11))

    def test_duplicate_by_text_or_media_is_skipped_and_marked(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|Same words / here',
                        'GW0002|2026-10-07T15:00|tiktok|b.mp4|-|new'])
        got, rep = run(lib, [q('tiktok', '2026-10-20T15:00', text='Same words\nhere', media='z.mp4'),
                             q('tiktok', '2026-10-21T15:00', media='b.mp4')])
        self.assertTrue(got['GW0001']['present'])
        self.assertTrue(got['GW0002']['present'])
        self.assertEqual(rep['dupes'], ['GW0001', 'GW0002'])

    def test_same_text_on_another_platform_is_not_a_duplicate(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, _ = run(lib, [q('instagram', '2026-10-20T15:00', text='hello', media='a.mp4')])
        self.assertFalse(got['GW0001'].get('present'))

    def test_hold_rows_never_load_and_are_named_when_close(self):
        lib = make_lib(['HOLD-GW0001|2026-10-08T15:00|tiktok|a.mp4|-|sale'])
        got, rep = run(lib, [])
        self.assertNotIn('HOLD-GW0001', got)
        self.assertEqual(rep['hold_soon'][0][0], 'HOLD-GW0001')

    def test_wave2_waits_for_wave1(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|one'],
                       ['GW2001|2026-11-06T16:00|tiktok|b.mp4|-|two'])
        got, _ = run(lib, [])
        self.assertEqual(list(got), ['GW0001'])
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|one'],
                       ['GW2001|2026-11-06T16:00|tiktok|b.mp4|-|two'], w1_log=['GW0001'])
        got, _ = run(lib, [])
        self.assertEqual(list(got), ['GW2001'])

    def test_past_row_moves_forward_and_after_nov_1_uses_new_slot(self):
        lib = make_lib(['GW0001|2026-09-21T15:00|tiktok|a.mp4|-|old',
                        'GW0002|2026-11-02T15:00|tiktok|b.mp4|-|nov'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 10, 5, 15, 0))
        self.assertEqual(got['GW0002']['at'], dt.datetime(2026, 11, 2, 16, 0))

    def test_x_over_280_is_not_loaded(self):
        lib = make_lib([f'GW0001|2026-10-06T13:30|twitter|-|-|{"a" * 281}'])
        got, rep = run(lib, [])
        self.assertNotIn('GW0001', got)
        self.assertIn('281', rep['skipped'][0][1])

    def test_failed_validator_loads_nothing(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'], validator_ok=False)
        got, rep = run(lib, [])
        self.assertEqual(got, {})
        self.assertIn('broken', rep['stop'])

    def test_reserve_for_halloween_can_stop_the_run(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        queue = [q('twitter', f'2026-12-{d:02d}T13:30', text=f't{d}', media=f'{d}') for d in range(1, 29)] * 6
        got, rep = run(lib, queue[:155], reserve=40)
        self.assertEqual(got, {})
        self.assertIn('Halloween', rep['stop'])

    def test_slash_means_line_break_but_urls_survive(self):
        self.assertEqual(refill.row_text('a /  / b https://payhip.com/b/9FE2U'),
                         'a\n\nb https://payhip.com/b/9FE2U')

    def test_rest_body_shape(self):
        a = refill.create_args(dict(platform='tiktok', text='t', media='a.mp4', title='-'),
                               dt.datetime(2026, 10, 6, 15, 0))
        b = refill.rest_body(a)
        self.assertEqual(b['scheduledTime'], '2026-10-06T15:00:00Z')
        self.assertEqual(b['post']['target']['privacyLevel'], 'PUBLIC_TO_EVERYONE')
        self.assertEqual(b['post']['accountId'], '41488')


if __name__ == '__main__':
    unittest.main(verbosity=1)
