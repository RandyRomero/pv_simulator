FROM python:3.11.2-alpine3.17 as builder

COPY poetry.lock pyproject.toml ./

RUN pip install -U pip \
    && pip install poetry \
    && poetry export --without-hashes --format=requirements.txt > requirements.txt \
	&& mkdir /wheels \
    && pip wheel -r requirements.txt --wheel-dir /wheels

FROM python:3.11.2-alpine3.17

WORKDIR src/

COPY --from=builder /wheels /wheels
RUN  pip install /wheels/*

COPY . .

RUN pip install --editable .

ENV RABBIT_HOST=localhost \
	RABBIT_PORT=5672 \
	RABBIT_LOGIN=guest

CMD ["python", "pv_simulator"]


