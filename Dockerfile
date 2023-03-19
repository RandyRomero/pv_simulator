FROM python:3.11.2-alpine3.17

WORKDIR /src

COPY poetry.lock pyproject.toml /src/

RUN pip install -U pip && \
    pip install poetry && \
    poetry export --without-hashes --format=requirements.txt > requirements.txt && \
    yes | pip uninstall poetry && \
    pip install -r requirements.txt

COPY . .

RUN pip install --editable .

ENV RABBIT_HOST=localhost \
	RABBIT_PORT=5672 \
	RABBIT_LOGIN=guest \
	RABBIT_PASSWORD=guest

CMD ["python", "pv_simulator"]

