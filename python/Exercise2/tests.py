import unittest
from datetime import datetime, timedelta
from CodeToRefactor import People, BirthingUnit


class TestPeople(unittest.TestCase):

    def test_given_no_dob_when_create_person_then_age_approx_15(self):
        p = People("Alice")
        approx_15_years_ago = datetime.utcnow() - timedelta(days=15 * 365)
        self.assertEqual(p.name, "Alice")
        self.assertAlmostEqual(
            (p.dob - approx_15_years_ago).total_seconds(),
            0,
            delta=5
        )

    def test_given_explicit_dob_when_create_person_then_dob_is_set(self):
        dob = datetime(2000, 1, 1)
        p = People("Alice", dob)
        self.assertEqual(p.dob, dob)


class TestBirthingUnit(unittest.TestCase):

    def test_generate_and_return_people(self):
        bu = BirthingUnit()
        people = bu.generate_and_return_people(5)
        self.assertEqual(len(people), 5)

    def test_generate_and_return_people_accumulates(self):
        bu = BirthingUnit()
        bu.generate_and_return_people(3)
        bu.generate_and_return_people(2)
        self.assertEqual(len(bu._people), 5)

    def test_when_generate_and_return_people_then_names_are_valid(self):
        bu = BirthingUnit()
        people = bu.generate_and_return_people(20)
        for p in people:
            self.assertIn(p.name, {"Bob", "Betty"})

    def test_when_generate_and_return_people_then_both_names_appear_in_sample(self):
        """
        This tests that both names appear in the sample.
        Technically there's a chance this test could fail randomly but it's very slim.
        """
        bu = BirthingUnit()
        people = bu.generate_and_return_people(20)
        self.assertIn("Bob", {p.name for p in people})
        self.assertIn("Betty", {p.name for p in people})

    def test_when_generate_and_return_people_none_under_15(self):
        bu = BirthingUnit()
        people = bu.generate_and_return_people(20)
        cutoff = datetime.utcnow() - timedelta(days=15 * 365)
        for p in people:
            # date of birth must be at least 15 years in the past
            self.assertLessEqual(p.dob, cutoff)

    def test_given_mixed_people_whenget_bobs_false_then_returns_all_bobs(self):
        bu = BirthingUnit()
        bu._people = [
            People("Bob"),
            People("Betty"),
            People("Bob"),
        ]
        bobs = bu.get_bobs(False)
        self.assertEqual(len(bobs), 2)

    def test_when_get_married_with_lastname_then_combines(self):
        bu = BirthingUnit()
        p = People("Bob")
        result = bu.get_married(p, "Smith")
        self.assertEqual(result, "Bob Smith")

    # Am not sure why this behaviour exists,
    # but I've included a test for it anyway,
    # because this exercise is about refactoring not changing behaviour.
    def test_when_get_married_with_testington_then_returns_name_only(self):
        bu = BirthingUnit()
        p = People("Bob")
        result = bu.get_married(p, "testington")
        self.assertEqual(result, "Bob")
    
    # This behaviour is wrong, the younger_than_30 flag actually gives Bobs under 30.
    # But I've written a test for the current behaviour since this exercise is about
    # refactoring not changing behaviour.
    def test_whenget_bobs_over_30_flag_then_returns_expected_count(self):
        bu = BirthingUnit()
        old_bob = People("Bob", datetime.utcnow() - timedelta(days=40*365))
        young_bob = People("Bob", datetime.utcnow() - timedelta(days=20*365))
        young_bob2 = People("Bob", datetime.utcnow() - timedelta(days=20*365))
        betty = People("Betty", datetime.utcnow() - timedelta(days=50*365))
        bu._people = [old_bob, young_bob, young_bob2, betty]
        bobs_over_30 = bu.get_bobs(younger_than_30=True)
        self.assertEqual(len(bobs_over_30), 2)


if __name__ == "__main__":
    unittest.main()
