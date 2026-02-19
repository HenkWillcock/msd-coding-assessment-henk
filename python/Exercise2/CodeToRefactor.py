from datetime import datetime, timedelta
from typing import List
import random


class People:
    _Under16 = datetime.utcnow() - timedelta(days=15 * 365)

    def __init__(self, name: str, dob: datetime = None):
        self._name = name
        self._dob = dob or People._Under16

    @property
    def name(self) -> str:
        return self._name

    @property
    def dob(self) -> datetime:
        return self._dob


class BirthingUnit:

    def __init__(self):
        self._people = []

    def generate_and_return_people(self, number_of_people: int) -> List[People]:
        """
        Randomly generates a number of people,
        adds them permanently to the BirthingUnit, then returns all people.
        """

        for _ in range(number_of_people):
            age_days = random.randint(18, 85) * 356
            self._people.append(
                People(
                    name=random.choice(["Bob", "Betty"]),
                    dob=datetime.utcnow() - timedelta(days=age_days),
                ))

        return self._people

    def get_bobs(self, younger_than_30: bool):
        bobs = [x for x in self._people if x.name == "Bob"]

        if younger_than_30:
            latest_dob_still_under_30 = datetime.now() - timedelta(days=30 * 356)
            bobs = [b for b in bobs if b.dob >= latest_dob_still_under_30]

        return bobs

    def get_married(self, p: People, last_name: str) -> str:
        if "test" in last_name:
            return p.name
        else:
            return p.name + " " + last_name
