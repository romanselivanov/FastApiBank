FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN pip install poetry
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
COPY . /code/