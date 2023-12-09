from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Iterator

import pwnedpasswords
import zxcvbn
from pykeepass import PyKeePass
from pykeepass.entry import Entry


@total_ordering
class PasswordScore(Enum):
    TERRIBLE = 0, "terrible"
    WEAK = 1, "weak"
    FAIR = 2, "fair"
    STRONG = 3, "strong"
    VERY_STRONG = 4, "very strong"

    @property
    def score(self) -> int:
        return self.value[0]

    @property
    def label(self) -> str:
        return self.value[1]

    @staticmethod
    def get_by_score(score: int) -> 'PasswordScore':
        return PASSWORD_SCORES[score]

    def __lt__(self, other: 'PasswordScore') -> bool:
        if self.__class__ is other.__class__:
            return self.score < other.score
        return NotImplemented


PASSWORD_SCORES = {score.score: score for score in PasswordScore}


@dataclass
class EvaluatedPassword:
    password: str
    entries: list[Entry]
    entropy: float | None = None
    score: PasswordScore | None = None
    compromise_count: int | None = None

    @property
    def is_compromised(self) -> bool:
        return self.compromise_count > 0


@dataclass
class PasswordEvaluator:
    keepass_db: PyKeePass
    compromise_check_enabled: bool = True
    scoring_enabled: bool = True

    def count_passwords(self) -> int:
        return len({entry.password for entry in self.keepass_db.entries})

    def check_passwords(self) -> Iterator[EvaluatedPassword]:
        entries_by_password = {}

        for entry in self.keepass_db.entries:
            if entry.password:
                entries_by_password.setdefault(entry.password, []).append(entry)

        for password, entries in sorted(entries_by_password.items()):
            evaluated_password = EvaluatedPassword(password, entries)

            if self.compromise_check_enabled:
                evaluated_password.compromise_count = pwnedpasswords.check(password)

            if self.scoring_enabled:
                zxcvbn_result = zxcvbn.zxcvbn(password)
                evaluated_password.score = PasswordScore.get_by_score(zxcvbn_result['score'])
                evaluated_password.entropy = zxcvbn_result['guesses_log10']

            yield evaluated_password
