FROM python:3.10-alpine3.18

WORKDIR /app

COPY pyproject.toml ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]