from datetime import datetime

MIN_CART_VALUE_AVOID_SURCHARGE = 1000
MIN_CART_FEE = 0
FREE_DELIVERY_THRESHOLD = 10000

BASE_DISTANCE_FEE_THRESHOLD = 1000
BASE_DISTANCE_FEE = 200
DISTANCE_SURCHARGE = 100

BULK_ITEM_FEE = 120
ITEM_SURCHARGE = 50
MAX_ITEMS_WITHOUT_SURCHARGE = 4
MIN_ITEM_FEE = 0

FRIDAY_DAY_OF_WEEK = 5
LOWER_THRESHOLD_UTC = 15
UPPER_THRESHOLD_UTC = 19
MULTIPLIER = 1.2


def cart_value_fee(cart_value):
    """
    The function calculates the cart fee based on cart value,
    and also checks if the cart value warrants free delivery.
    1.  If cart value < 10 Euro: then fee = cart_value - 10 Euro
    2.  If cart value >= 10 Euro: then fee = 0
    3.  If cart value >= 100 Euro: then free delivery.

    :param: cart_value: The value of the cart in cents.
    :return:
            Tuple(int, bool): e.g (cart_fee, free_delivery_check):
                cart_fee: (int) Additional fee on cart value in cents.
                free_delivery_check: (bool) If cart value warrants free delivery.
                cart_value: (int) The cart value in cents.
    """
    free_delivery_check = False
    if cart_value < MIN_CART_VALUE_AVOID_SURCHARGE:
        cart_fee = (MIN_CART_VALUE_AVOID_SURCHARGE - cart_value)
        return cart_fee, free_delivery_check
    elif cart_value >= FREE_DELIVERY_THRESHOLD:
        free_delivery_check = True
        return MIN_CART_FEE, free_delivery_check
    else:
        return MIN_CART_FEE, free_delivery_check


def delivery_distance_fee(delivery_distance):
    """
    The function calculates the distance fee based on the delivery distance:
    1. If delivery distance <= 1000 (meters) apply BASE_DISTANCE_FEE.
    2. If delivery distance > 1000, 1 Euro for every 500 meter.

    :param: delivery_distance: The delivery distance in meters.
    :return:
            BASE_DISTANCE_FEE: (int) The delivery distance fee in cents.
            distance_fee_mod_500: (int) The delivery distance fee in cents.
            distance_fee_rounded: (int) The delivery distance fee in cents.
    """
    if delivery_distance <= BASE_DISTANCE_FEE_THRESHOLD:
        return BASE_DISTANCE_FEE
    elif delivery_distance % 500 == 0:
        distance_fee_mod_500 = (delivery_distance // 500) * DISTANCE_SURCHARGE
        return distance_fee_mod_500
    else:
        rounded_distance = (delivery_distance + 500) - (delivery_distance % 500)
        distance_fee_rounded = (rounded_distance // 500) * DISTANCE_SURCHARGE
        return distance_fee_rounded


def number_of_items_fee(number_of_items):
    """
    The function calculates the item fee based on the number of items in the cart.
    1. No charge for 4 or fewer items.
    2. 50 cent surcharge on 5 and greater items.
    3. Additional bulk charge of 1,20 Euro on 13th item.

    :param: number_of_items: The number of items in the cart.
    :return:
            item_fee: (int) The item fee in cents.
            item_fee_bulk: (int) The item fee + bulk fee in cents.
            MIN_ITEM_FEE: (int) The min item fee (0).
    """
    if 5 <= number_of_items <= 12:
        item_fee = (number_of_items - MAX_ITEMS_WITHOUT_SURCHARGE) * ITEM_SURCHARGE
        return item_fee
    elif number_of_items > 12:
        item_fee_bulk = ((number_of_items - MAX_ITEMS_WITHOUT_SURCHARGE) * ITEM_SURCHARGE) + BULK_ITEM_FEE
        return item_fee_bulk
    else:
        return MIN_ITEM_FEE


def delivery_fee_multiplier(fee, time):
    """
    The function calculates the multiplier fee based on the time.
    1. Multiplier of 1.2x is applied to fee on Friday (3 - 7 UTC)

    :param: fee: The delivery fee in cents.
    :param: time: The time in UTC ('%Y-%m-%dT%H:%M:%SZ').
    :return:
            fee_multiplier: (int) The fee in cents after applying multiplier.
            fee: (int) The normal fee in cents.
    """
    date_time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    day_of_week = date_time.isoweekday()
    utc_hour = date_time.hour

    if day_of_week == FRIDAY_DAY_OF_WEEK and LOWER_THRESHOLD_UTC <= utc_hour <= UPPER_THRESHOLD_UTC:
        fee_multiplier = fee * MULTIPLIER
        return fee_multiplier
    else:
        return fee
