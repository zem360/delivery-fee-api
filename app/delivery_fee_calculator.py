from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .helper import helper_functions

MAX_DELIVERY_FEE = 1500
MIN_DELIVERY_FEE = 0

app = FastAPI()


class DeliveryData(BaseModel):
    """
    Request Body initialized with default values.
    """
    cart_value: int = 790
    delivery_distance: int = 2235
    number_of_items: int = 4
    time: str = "2021-10-12T13:00:00Z"


@app.get("/")
async def root():
    """
    API root endpoint that displays message to redirect to Open API docs.
    :return:
            JSON: A JSON message body.
    """
    # Redirects to Open API Docs to test API.
    return {"message": "redirect to url: http://127.0.0.1:80/docs"}


@app.post("/delivery_fee")
async def delivery_calculator(data: DeliveryData):
    """
    API endpoint to calculate the delivery fee based on the information in the request payload (JSON).

    :param data: DeliveryData (JSON) The JSON request payload:
    :return:
            JSON: {"delivery_fee": int}
    """
    try:
        cart_fee, free_delivery_check = helper_functions.cart_value_fee(data.cart_value)
        distance_fee = helper_functions.delivery_distance_fee(data.delivery_distance)

        items_fee = helper_functions.number_of_items_fee(data.number_of_items)
        sum_of_fees = cart_fee + distance_fee + items_fee
        delivery_fee = helper_functions.delivery_fee_multiplier(sum_of_fees, data.time)

        if free_delivery_check:
            return {"delivery_fee": MIN_DELIVERY_FEE}
        elif delivery_fee > MAX_DELIVERY_FEE:
            return {"delivery_fee": MAX_DELIVERY_FEE}
        else:
            return {"delivery_fee": delivery_fee}
    except ValueError as e:
        # Exception blocks handles value error if time in request body in wrong format.
        raise HTTPException(
            status_code=400,
            detail=f"Exception: {e}"
        )
