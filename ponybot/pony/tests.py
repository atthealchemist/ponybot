from datetime import datetime

from django.test import TestCase, TransactionTestCase
from .models import Pony

# Create your tests here.


class PonyTestCase(TransactionTestCase):

    def test_pony_created(self):
        my_pony = Pony(
            name="Lauren Faust"
        )

        self.assertIsNotNone(my_pony)
        self.assertEqual("Lauren Faust", my_pony.name)

        pinkie = Pony(
            name="Pinkie Pie"
        )
        self.assertNotEqual(my_pony.name, pinkie.name)

    def test_pony_has_default_experience(self):
        my_pony = Pony(
            name="Lauren"
        )
        self.assertIsNotNone(my_pony.experience, 1)
        self.assertGreater(my_pony.experience, 0)
        self.assertLess(my_pony.experience, 10)

    def test_pony_has_default_satiety(self):
        my_pony = Pony(name="Rarity")
        self.assertIsNotNone(my_pony.satiety)
        self.assertGreater(my_pony.satiety, 1)
        self.assertLess(my_pony.satiety, my_pony.experience + 14)

    def test_pony_feed(self):
        my_pony = Pony(name="Fluttershy")
        satiety_before = my_pony.satiety
        my_pony.feed()
        self.assertGreater(my_pony.satiety, satiety_before)

        aj_pony = Pony(
            name="Applejack",
            satiety=14
        )
        satiety_before = aj_pony.satiety
        aj_pony.feed()
        self.assertEqual(aj_pony.satiety, satiety_before)

    def test_pony_last_feeded(self):
        my_pony = Pony(
            name="Rainbow Dash"
        )

        my_pony.feed()

        self.assertEqual(
            (my_pony.last_feeding.hour, my_pony.last_feeding.minute),
            (datetime.now().hour, datetime.now().minute)
        )
