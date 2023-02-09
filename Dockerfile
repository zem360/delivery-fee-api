FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Uvicorn will run on localhost port 80. If port changed, update in delivery_fee_calculator get("/") line 29.
# and adjust docker commands as necessary.
CMD ["uvicorn", "app.delivery_fee_calculator:app", "--host", "0.0.0.0", "--port", "80"]