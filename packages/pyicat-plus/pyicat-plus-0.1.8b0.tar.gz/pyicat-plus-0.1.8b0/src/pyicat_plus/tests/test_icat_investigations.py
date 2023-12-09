import random
from typing import Optional

from datetime import datetime, timedelta
from ..client.investigation import _select_investigation


def test_investigation_none():
    investigations = _Investigations()

    # No investigations
    investigations.check(timedelta())

    # Ignore open-ended
    # _____|‾‾‾‾‾
    #         |
    investigations.session(timedelta(days=1, seconds=1))
    investigations.check(timedelta(days=2), allow_open_ended=False)


def test_investigation_inside():
    investigations = _Investigations()

    # Inside single investigation
    # _____|‾‾‾‾‾|_____
    #        |
    investigations.session(timedelta(days=1), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=1, seconds=1))

    # Inside the earliest of two investigation
    # _____|‾‾‾‾‾|___________
    # ___________|‾‾‾‾‾|_____
    #        |
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.check(timedelta(days=1, hours=2))

    # ___________|‾‾‾‾‾|_____
    # _____|‾‾‾‾‾|___________
    #        |
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.check(timedelta(days=1, hours=2))

    # On the border of two subsequent investigations
    # _____|‾‾‾‾‾|___________
    # ___________|‾‾‾‾‾|_____
    #            |
    investigations.session(timedelta(days=1), timedelta(days=2))
    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2))

    # ___________|‾‾‾‾‾|_____
    # _____|‾‾‾‾‾|___________
    #            |
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.check(timedelta(days=2))

    # Inside closed-ended and open-ended investigation
    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾|_____
    #              |
    investigations.session(timedelta(days=1))
    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2, seconds=1))

    # ___________|‾‾‾‾‾|_____
    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    #              |
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.session(timedelta(days=1), expected=True)
    investigations.check(timedelta(days=2, seconds=1))

    # On the border of closed-ended and open-ended investigation (not same start date)
    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾|_____
    #            |
    investigations.session(timedelta(days=1))
    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2))

    # ___________|‾‾‾‾‾|_____
    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    #            |
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.session(timedelta(days=1), expected=True)
    investigations.check(timedelta(days=2))

    # On the border of closed-ended and open-ended investigation (same start date)
    # ___________|‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾|_____
    #            |
    investigations.session(timedelta(days=2))
    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2))

    investigations.session(timedelta(days=2))
    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2), allow_open_ended=False)

    # ___________|‾‾‾‾‾|_____
    # ___________|‾‾‾‾‾‾‾‾‾‾‾
    #            |
    investigations.session(timedelta(days=2), timedelta(days=3))
    investigations.session(timedelta(days=2), expected=True)
    investigations.check(timedelta(days=2))

    investigations.session(timedelta(days=2), timedelta(days=3), expected=True)
    investigations.session(timedelta(days=2))
    investigations.check(timedelta(days=2), allow_open_ended=False)

    # Select inside overlapping open-ended investigations
    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # _________________|‾‾‾‾‾‾‾‾‾‾‾
    #        |
    investigations.session(timedelta(days=1), expected=True)
    investigations.session(timedelta(days=2))
    investigations.session(timedelta(days=3))
    investigations.check(timedelta(days=1, seconds=1))

    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # _________________|‾‾‾‾‾‾‾‾‾‾‾
    #             |
    investigations.session(timedelta(days=1))
    investigations.session(timedelta(days=2), expected=True)
    investigations.session(timedelta(days=3))
    investigations.check(timedelta(days=2, seconds=1))

    # _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ___________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # _________________|‾‾‾‾‾‾‾‾‾‾‾
    #                   |
    investigations.session(timedelta(days=1))
    investigations.session(timedelta(days=2))
    investigations.session(timedelta(days=3), expected=True)
    investigations.check(timedelta(days=3, seconds=1))


def test_investigation_inbetween():
    investigations = _Investigations()

    # Between two investigations
    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾|_____
    #             |
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.session(timedelta(days=3), timedelta(days=4))
    investigations.check(timedelta(days=2, hours=2))

    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾|_____
    #                 |
    investigations.session(timedelta(days=1), timedelta(days=2))
    investigations.session(timedelta(days=3), timedelta(days=4), expected=True)
    investigations.check(timedelta(days=2, hours=13))

    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾‾‾‾‾‾‾
    #             |
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.session(timedelta(days=3))
    investigations.check(timedelta(days=2, hours=2))

    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾‾‾‾‾‾‾
    #                 |
    investigations.session(timedelta(days=1), timedelta(days=2))
    investigations.session(timedelta(days=3), expected=True)
    investigations.check(timedelta(days=2, hours=13))


def test_investigation_outside():
    investigations = _Investigations()

    # Date before investigation
    # _____|‾‾‾‾‾|_____
    #    |
    investigations.session(
        timedelta(days=1, seconds=1), timedelta(days=2), expected=True
    )
    investigations.check(timedelta(days=1))

    # Date before open-ended investigation
    # _____|‾‾‾‾‾
    # |
    investigations.session(timedelta(days=1), expected=True)
    investigations.check(timedelta())

    # Date after investigation
    # _____|‾‾‾‾‾|_____
    #             |
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.check(timedelta(days=2, seconds=1))

    # Date before two investigations
    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾|_____
    #  |
    investigations.session(timedelta(days=1), timedelta(days=2), expected=True)
    investigations.session(timedelta(days=3), timedelta(days=4))
    investigations.check(timedelta(hours=2))

    # Date after two investigations
    # _____|‾‾‾‾‾|_________________
    # _________________|‾‾‾‾‾|_____
    #                          |
    investigations.session(timedelta(days=1), timedelta(days=2))
    investigations.session(timedelta(days=3), timedelta(days=4), expected=True)
    investigations.check(timedelta(days=4, hours=2))


class _Investigations:
    def __init__(self):
        self._reset()

    def session(
        self,
        start_offset: timedelta,
        end_offset: Optional[timedelta] = None,
        expected: bool = False,
    ) -> None:
        startdate = self._date + start_offset
        investigation = {
            "id": len(self._investigations),
            "startDate": startdate.astimezone().isoformat(),
            "unique": random.uniform(0, 1),
        }
        if end_offset is not None:
            enddate = self._date + end_offset
            investigation["endDate"] = enddate.astimezone().isoformat()
        self._investigations.append(investigation)
        if expected:
            self._expected = investigation

    def _reset(self):
        self._investigations = list()
        self._expected = None
        self._nextid = 10000
        # +1 day: CEST -> EST
        self._date = datetime(year=2023, month=10, day=28, hour=8)

    def check(self, offset: timedelta, allow_open_ended: bool = True):
        if self._investigations:
            random.shuffle(self._investigations)
        date = (self._date + offset).astimezone()
        investigation = _select_investigation(
            self._investigations, date=date, allow_open_ended=allow_open_ended
        )
        assert investigation == self._expected
        self._reset()
