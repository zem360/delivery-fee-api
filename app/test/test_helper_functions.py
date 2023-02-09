from app.helper import helper_functions
import pytest

def test_cart_value_fee():
    """
    Test for helper function cart_value_fee()
    :return:
            Tuple: (int, bool)
    """
    # Cart Value < 10 Euro.
    assert helper_functions.cart_value_fee(500) == (500, False)
    assert helper_functions.cart_value_fee(790) == (210, False)

    # Cart Value > 10 Euro.
    assert helper_functions.cart_value_fee(1000) == (0, False)
    assert helper_functions.cart_value_fee(1200) == (0, False)

    # Cart Value >= 100 Euro. Free Delivery
    assert helper_functions.cart_value_fee(10000) == (0, True)


def test_delivery_distance_fee():
    """
    Test for helper function delivery_distance_fee()
    :return:
            int
    """
    # Base Delivery Fee
    assert helper_functions.delivery_distance_fee(100) == 200
    assert helper_functions.delivery_distance_fee(500) == 200
    assert helper_functions.delivery_distance_fee(1000) == 200

    # Base Delivery Fee + 1 Euro per 500 meter
    assert helper_functions.delivery_distance_fee(1192) == 300
    assert helper_functions.delivery_distance_fee(1200) == 300
    assert helper_functions.delivery_distance_fee(1500) == 300
    assert helper_functions.delivery_distance_fee(2000) == 400


def test_number_of_items_fee():
    """
    Test for helper function number_of_items_fee()
    :return:
            int
    """
    # Items <= 4: Fee=0
    assert helper_functions.number_of_items_fee(2) == 0
    assert helper_functions.number_of_items_fee(4) == 0

    # Items > 4: 50 Cent surcharge on 5th item onwards.
    assert helper_functions.number_of_items_fee(5) == 50
    assert helper_functions.number_of_items_fee(10) == 300
    assert helper_functions.number_of_items_fee(12) == 400

    # 50 Cent surcharge on 5th item onwards + 120 Cent bulk fee on 13th item
    assert helper_functions.number_of_items_fee(13) == 570
    assert helper_functions.number_of_items_fee(14) == 620


def test_delivery_fee_multiplier():
    """
    Test for helper function delivery_fee_multiplier()
    :return:
            int
    """
    # Normal Days
    assert helper_functions.delivery_fee_multiplier(400,"2022-10-12T13:00:00Z") == 400
    assert helper_functions.delivery_fee_multiplier(1200, "2022-11-08T13:00:00Z") == 1200

    # Friday and between 15 - 19 UTC. Multiplier Activated
    assert helper_functions.delivery_fee_multiplier(1200, "2022-10-14T15:00:00Z") == 1440
    assert helper_functions.delivery_fee_multiplier(1000,"2022-10-14T15:00:00Z") == 1200

