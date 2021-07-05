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
