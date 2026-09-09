#!/usr/bin/env python3
"""Assertions for the Run 8 source list that are clearer here than in shell."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_trivia_bank as B  # noqa: E402


def approved_source_still_passes():
    approved = B.load_sources(os.path.join(HERE, "trivia.sources.csv"))
    bank = B.load_bank(os.path.join(HERE, "trivia.bank.csv"))
    # The rule is "not approved", not "has a FoundIn at all".
    return B.is_usable(bank["TRV-903"], None, approved)


def parked_source_is_held():
    approved = B.load_sources(os.path.join(HERE, "trivia.sources.csv"))
    bank = B.load_bank(os.path.join(HERE, "trivia.bank.csv"))
    problems = B.usable_problems(bank["TRV-902"], None, approved)
    return any("not an approved source" in p for p in problems)


def live_list_matches_her_answer():
    """Amanda approved tier 1 and 3 on 09/09 and parked tier 2."""
    a = B.load_sources()
    return (len(a) == 10
            and "techpresso@dupple.com" in a          # tier 1
            and "store-news@amazon.com" in a          # tier 3
            and "amn@mail.beehiiv.com" not in a       # the stock tips
            and "paul@shopifreaks.com" not in a)      # tier 2, parked


if __name__ == "__main__":
    fn = {"approved-passes": approved_source_still_passes,
          "parked-held": parked_source_is_held,
          "live-list": live_list_matches_her_answer}[sys.argv[1]]
    sys.exit(0 if fn() else 1)
