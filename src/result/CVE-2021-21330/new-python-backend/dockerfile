FROM python:3.10 as compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./root-certs.crt /app/root-certs.crt
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.10 as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/

CMD [ "python", "app/main.py" ]
