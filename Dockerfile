FROM python:3.12-slim

WORKDIR /code

RUN pip install fastapi "uvicorn[standard]" requests datetime

COPY ./app /code/app

CMD ["uvicorn", "app.get:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]