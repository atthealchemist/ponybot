from datetime import datetime
import time
import pytest

from django.test import TestCase, TransactionTestCase
from .models import Pony


# Create your tests here.


@pytest.mark.django_db
def test_pony_created():
    my_pony = Pony.objects.create(
        name="Applejack",
        satiety=16
    )
    assert my_pony is not None
    assert my_pony.name == "Applejack"


@pytest.mark.django_db
def test_pony_has_experience():
    my_pony = Pony.objects.create(
        name="Applejack",
        satiety=16
    )
    assert my_pony.experience is not None
    assert 0 < my_pony.experience <= 10


@pytest.mark.django_db
def test_pony_has_satiety():
    my_pony = Pony.objects.create(
        name="Applejack",
        satiety=12
    )
    assert my_pony.satiety is not None
    assert 0 < my_pony.satiety <= my_pony.experience + 14


@pytest.mark.django_db
def test_pony_feeding():
    my_pony = Pony.objects.create(
        name="Twilight Sparkle",
        satiety=12
    )
    satiety_before = my_pony.satiety
    my_pony.feed()
    assert my_pony.satiety > satiety_before

    aj_pony = Pony.objects.create(name="Applejack", satiety=14)
    satiety_before = aj_pony.satiety
    aj_pony.feed()
    assert aj_pony.satiety == satiety_before


@pytest.mark.django_db
def test_pony_last_feeded():
    my_pony = Pony.objects.create(
        name="Rainbow Dash"
    )

    my_pony.feed()

    my_pony_feeding_hm = (
        my_pony.last_feeding.hour, my_pony.last_feeding.minute
    )
    now_hm = (
        datetime.now().hour, datetime.now().minute
    )

    assert my_pony_feeding_hm == now_hm


@pytest.mark.django_db
def test_pony_first_feed():
    my_pony = Pony.objects.create(name="Sweetie Belle")
    my_pony.feed()

    my_pony.feed()
    assert my_pony.first_feeding != my_pony.last_feeding


@pytest.mark.django_db
def test_pony_learned():
    my_pony = Pony.objects.create(
        name="Rainbow Dash"
    )

    level_before = my_pony.experience

    my_pony.learn()

    assert my_pony.experience > level_before


@pytest.mark.django_db
def test_pony_last_learned():
    my_pony = Pony.objects.create(
        name="Rainbow Dash"
    )

    my_pony.learn()

    my_pony_learning_hm = (
        my_pony.last_learning.hour, my_pony.last_learning.minute
    )
    now_hm = (
        datetime.now().hour, datetime.now().minute
    )

    assert my_pony_learning_hm == now_hm


@pytest.mark.django_db
def test_pony_stats():
    my_pony = Pony.objects.create(name="Derpy Hooves")

    assert 'Derpy' in str(my_pony)


@pytest.mark.django_db
def test_pony_lifecycle_is_pony_alive():
    my_pony = Pony.objects.create(name="Spike")

    assert my_pony.is_alive is True


@pytest.mark.django_db
def test_pony_lifecycle_dead_pony_should_not_eat():
    my_pony = Pony.objects.create(name="Flutter Bat", is_alive=False)

    my_pony.die()
    my_pony.feed()

    assert my_pony.satiety == 0
    assert my_pony.experience == 0
