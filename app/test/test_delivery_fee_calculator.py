from fastapi.testclient import TestClient
from fastapi import status
from app.delivery_fee_calculator import app


client = TestClient(app=app)

############ Test for API. ##############
def test_api_example_data():
    """
    Test to check API response on example data from assignment GitHub page.
    :return:
            {"delivery_fee": 710}
    """
    response = client.post('/delivery_fee', json={
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2021-10-12T13:00:00Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"delivery_fee": 710}


def test_api_normal_data():
    """
    Test to check API response on randomly selected data.
    :return:
            {"delivery_fee": 710}
    """
    response = client.post('/delivery_fee', json={
        "cart_value": 800,
        "delivery_distance": 3500,
        "number_of_items": 5,
        "time": "2023-01-15T19:00:00Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"delivery_fee": 950}


def test_api_time_format_error_data():
    """
    Test to check that the API raises a BAD_REQUEST response when
    time format is not in '%Y-%m-%dT%H:%M:%SZ'.
    :return:
            status.HTTP_400_BAD_REQUEST
    """
    response = client.post('/delivery_fee', json={
        "cart_value": 1000,
        "delivery_distance": 2535,
        "number_of_items": 4,
        "time": "2021-10-12"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_free_delivery_data():
    """
    Test to check that delivery fee = 0 when cart value is >= 10000(100 Euro).
    :return:
            {"delivery_fee": 0}
    """
    response = client.post('/delivery_fee', json={
        "cart_value": 10000,
        "delivery_distance": 2535,
        "number_of_items": 4,
        "time": "2021-10-12T13:00:00Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"delivery_fee": 0}


def test_api_max_delivery_fee_data():
    """
    Test to check that delivery fee does not exceed 1500 (15 Euro).
    The delivery fee for parameters provided come out to 1644 (16.44 Euro).
    :parameter
        "cart_value": 7000,                 Cart Fee    : 0
        "delivery_distance": 4000,          Delivery Fee: 8
        "number_of_items": 13,              Item Fee    : 5,70
        "time": "2023-01-01T16:00:00Z"      Multiplier  : 1.2x
                                            Total       : 16.44 Euro
    :return:
            {"delivery_fee": 1500}
    """
    response = client.post('/delivery_fee', json={
        "cart_value": 7000,
        "delivery_distance": 4000,
        "number_of_items": 13,
        "time": "2023-01-27T16:00:00Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"delivery_fee": 1500}


