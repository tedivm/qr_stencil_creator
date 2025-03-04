ARG PYTHON_VERSION=3.12
FROM ghcr.io/multi-py/python-uvicorn:py${PYTHON_VERSION}-slim-LATEST

ENV APP_MODULE=qr_stencil.www:app

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./ /app
