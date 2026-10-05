"""Tests for refill.py. Run: python3 blotato-refill/tests/test_refill.py"""
import datetime as dt, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import refill

NOW = dt.datetime(2026, 10, 5, 12, 0)  # a Monday, 7:00 AM Central
C = lambda h, m=0, day=5, month=10: dt.datetime(2026, month, day, h, m)  # UTC

# A small registry: RESET answers on Instagram, CESA is retired on Facebook
# and lives on Cesa's own Instagram, which is how Blotato stood on 09/28.
REG = [dict(AutomationID=i, Keyword=k, Platform=p, AccountId=a, Handle='-', Active=on, Kind='magnet',
            Delivers='-', Destination='-', Note='') for i, k, p, a, on in (
    ('1', 'RESET', 'instagram', '45886', 'yes'),
    ('2', 'CESA', 'facebook', '30840', 'no'),
    ('3', 'CESA', 'instagram', '65540', 'yes'))]
CTA = [dict(Platform=p, KeywordWorks=w) for p, w in (
    ('instagram', 'yes'), ('facebook', 'yes'), ('tiktok', 'no'), ('youtube', 'no'), ('linkedin', 'no'))]


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


def run(lib, queue, reserve=0, now=NOW):
    loads, rep = refill.plan(lib, queue, now, reserve=reserve, registry=REG, cta=CTA)
    return {x['row']['id']: x for x in loads}, rep


class Placement(unittest.TestCase):
    def test_goes_to_the_nearest_open_day_whatever_its_date(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|tiktok|a.mp4|-|hello'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0001']['at'], C(19))  # today, 2:00 PM Central

    def test_one_top_up_a_day_per_account_at_2_pm(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|tiktok|a.mp4|-|one',
                        'GW0002|2026-10-25T15:00|tiktok|b.mp4|-|two'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0002']['at'], C(19, day=6))  # noon was retired on 24 Aug

    def test_three_a_day_counts_everything_including_the_6_pm_post(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|tiktok|a.mp4|-|one'])
        busy = [q('tiktok', '2026-10-05T13:30', text='a', media='a'), q('tiktok', '2026-10-05T16:00', text='b', media='b'),
                q('tiktok', '2026-10-05T23:00', text='c', media='c')]
        got, _ = run(lib, busy)
        self.assertEqual(got['GW0001']['at'], C(19, day=6))
        got, _ = run(lib, busy[1:])
        self.assertEqual(got['GW0001']['at'], C(19))

    def test_two_hours_clear_of_every_other_post_on_the_account(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|instagram|a.jpg|-|hello'])
        got, _ = run(lib, [q('instagram', '2026-10-05T18:30')])  # 1:30 PM Central
        self.assertEqual(got['GW0001']['at'], C(19, day=6))

    def test_never_more_than_7_days_out(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        full = [q('tiktok', f'2026-10-{d:02d}T{h}', text=f'{d}{h}', media=f'{d}{h}')
                for d in range(5, 14) for h in ('14:00', '16:00', '20:00')]
        got, rep = run(lib, full)
        self.assertEqual(got, {})
        self.assertEqual(rep['waiting'], ['GW0001'])

    def test_the_evening_hour_is_held_before_its_post_is_loaded(self):
        day = dt.date(2026, 10, 7)
        self.assertFalse(refill.evening_clear('instagram', day, C(22, day=7)))   # 5:00 PM Central
        self.assertTrue(refill.evening_clear('instagram', day, C(21, day=7)))    # 4:00 PM Central
        self.assertTrue(refill.evening_clear('linkedin', day, C(22, day=7)))
        self.assertFalse(refill.evening_clear('facebook', dt.date(2026, 12, 20), dt.datetime(2026, 12, 20, 23, 0)))

    def test_after_the_clocks_go_back_the_central_time_holds(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, _ = run(lib, [], now=dt.datetime(2026, 10, 31, 23, 0))  # 6:00 PM Central on 10/31
        self.assertEqual(got['GW0001']['at'], dt.datetime(2026, 11, 1, 20, 0))  # 2:00 PM CST

    def test_a_6_pm_post_after_the_change_counts_on_its_central_day(self):
        self.assertEqual(refill.to_central(dt.datetime(2026, 11, 3, 0, 0)).date(), dt.date(2026, 11, 2))
        self.assertEqual(refill.utc_of(dt.date(2026, 11, 2), '18:00'), dt.datetime(2026, 11, 3, 0, 0))
        self.assertEqual(refill.utc_of(dt.date(2026, 10, 30), '18:00'), dt.datetime(2026, 10, 30, 23, 0))

    def test_a_named_weekday_only_goes_out_on_that_day(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|tiktok|a.mp4|-|a rainy Friday and a dog groomer run'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0001']['at'], C(19, day=9))  # Friday 10/09

    def test_just_another_tuesday_is_a_name_not_a_day(self):
        self.assertEqual(refill.weekdays_named('Just Another Tuesday, 1 email a week. Comment TUESDAY'), set())
        self.assertEqual(refill.weekdays_named('today is my Thursday'), {3})

    def test_two_text_only_rows_are_not_copies_of_each_other(self):
        lib = make_lib(['GW0001|2026-10-25T13:30|linkedin|-|-|one', 'GW0002|2026-10-25T13:30|linkedin|-|-|two'])
        got, rep = run(lib, [])
        self.assertEqual(rep['dupes'], [])
        self.assertFalse(got['GW0002'].get('present'))

    def test_linkedin_is_1_a_day_at_8_30(self):
        lib = make_lib(['GW0001|2026-10-25T13:30|linkedin|-|-|one',
                        'GW0002|2026-10-25T13:30|linkedin|-|-|two'])
        got, _ = run(lib, [])
        self.assertEqual(got['GW0001']['at'], C(13, 30))
        self.assertEqual(got['GW0002']['at'], C(13, 30, day=6))


class Refusals(unittest.TestCase):
    def test_a_dead_keyword_is_refused_and_named(self):
        lib = make_lib(['GW0001|2026-10-10T17:10|facebook|a.jpg|-|She is 19. / Comment CESA and I will send her guide.'])
        got, rep = run(lib, [])
        self.assertNotIn('GW0001', got)
        self.assertEqual(rep['refused'][0][0], 'GW0001')
        self.assertIn('CESA', rep['refused'][0][1])

    def test_a_live_keyword_loads(self):
        lib = make_lib(['GW0001|2026-10-10T15:00|instagram|a.jpg|-|Comment RESET and I will send it.'])
        got, rep = run(lib, [])
        self.assertIn('GW0001', got)
        self.assertEqual(rep['refused'], [])

    def test_a_keyword_on_tiktok_is_refused(self):
        lib = make_lib(['GW0001|2026-10-10T15:00|tiktok|a.mp4|-|Comment RESET below'])
        got, rep = run(lib, [])
        self.assertNotIn('GW0001', got)
        self.assertEqual(rep['refused'][0][0], 'GW0001')

    def test_x_rows_are_skipped_and_do_not_hold_wave_2_back(self):
        lib = make_lib(['GW0001|2026-10-06T13:30|twitter|-|-|a post for X'],
                       ['GW2001|2026-11-06T16:00|tiktok|b.mp4|-|two'])
        got, rep = run(lib, [])
        self.assertEqual(list(got), ['GW2001'])
        self.assertEqual(rep['dropped']['twitter'], 1)
        self.assertEqual(rep['left'], 1)

    def test_hold_rows_never_load_and_are_named_when_close(self):
        lib = make_lib(['HOLD-GW0001|2026-10-08T15:00|tiktok|a.mp4|-|sale'])
        got, rep = run(lib, [])
        self.assertNotIn('HOLD-GW0001', got)
        self.assertEqual(rep['hold_soon'][0][0], 'HOLD-GW0001')


class Room(unittest.TestCase):
    def queue(self, n):
        return [q('linkedin', f'2026-12-{d:02d}T13:30', text=f't{d}{i}', media=f'{d}{i}')
                for i in range(8) for d in range(1, 29)][:n]

    def test_10_slots_stay_free_by_default(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'])
        got, rep = refill.plan(lib, self.queue(181), NOW, registry=REG, cta=CTA)
        self.assertEqual(got, [])
        self.assertIn('nightly run', rep['stop'])
        got, rep = refill.plan(lib, self.queue(180), NOW, registry=REG, cta=CTA)
        self.assertEqual(len(got), 1)
        self.assertEqual(rep['reserve'], 10)

    def test_wave_1_goes_before_wave_2(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|one'],
                       ['GW2001|2026-11-06T16:00|tiktok|b.mp4|-|two'])
        loads, _ = refill.plan(lib, [], NOW, reserve=0, registry=REG, cta=CTA)
        self.assertEqual([x['row']['id'] for x in loads], ['GW0001', 'GW2001'])
        self.assertEqual(loads[0]['at'], C(19))  # wave 1 gets the first choice of slot

    def test_loads_stop_at_the_room_left(self):
        plats = ('instagram', 'tiktok', 'facebook', 'youtube')
        lib = make_lib([f'GW00{i:02d}|2026-10-06T15:00|{plats[i % 4]}|{i}.jpg|-|post {i}' for i in range(20)])
        got, rep = run(lib, self.queue(190), reserve=0)  # 10 free
        self.assertEqual(len([x for x in got.values() if not x.get('present')]), 10)


class Carried(unittest.TestCase):
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

    def test_failed_validator_loads_nothing(self):
        lib = make_lib(['GW0001|2026-10-06T15:00|tiktok|a.mp4|-|hello'], validator_ok=False)
        got, rep = run(lib, [])
        self.assertEqual(got, {})
        self.assertIn('broken', rep['stop'])

    def test_slash_means_line_break_but_urls_survive(self):
        self.assertEqual(refill.row_text('a /  / b https://payhip.com/b/9FE2U'),
                         'a\n\nb https://payhip.com/b/9FE2U')

    def test_rest_body_shape(self):
        a = refill.create_args(dict(platform='tiktok', text='t', media='a.mp4', title='-'),
                               dt.datetime(2026, 10, 6, 19, 0))
        b = refill.rest_body(a)
        self.assertEqual(b['scheduledTime'], '2026-10-06T19:00:00Z')
        self.assertEqual(b['post']['target']['privacyLevel'], 'PUBLIC_TO_EVERYONE')
        self.assertEqual(b['post']['accountId'], '41488')

    def test_the_report_names_each_post_in_central_time(self):
        lib = make_lib(['GW0001|2026-10-25T15:00|tiktok|a.mp4|-|hello',
                        'GW0002|2026-10-10T17:10|facebook|a.jpg|-|Comment CESA below',
                        'GW0003|2026-10-06T13:30|twitter|-|-|for X'])
        loads, rep = refill.plan(lib, [], NOW, reserve=0, registry=REG, cta=CTA)
        path = os.path.join(tempfile.mkdtemp(), 'r.md')
        refill.write_report(path, rep, [x for x in loads if not x.get('present')], [], False)
        with open(path) as f:
            text = f.read()
        self.assertIn('GW0001 tiktok, Mon Oct 5, 2:00 PM Central', text)
        self.assertIn('Refused GW0002', text)
        self.assertIn('Skipped 1 X rows. X is 0 a day since 09/08.', text)


if __name__ == '__main__':
    unittest.main(verbosity=1)
