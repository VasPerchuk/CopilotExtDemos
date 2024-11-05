FROM python:3.9

WORKDIR /service

COPY ./requirements.txt /service/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /service/requirements.txt

COPY ./src /service

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]