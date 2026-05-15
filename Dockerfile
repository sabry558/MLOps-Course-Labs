FROM python:3.12-slim

WORKDIR /project

COPY pyproject.toml README.md ./

COPY app/ app/

COPY data/ data/
COPY main.py .

RUN  pip install --default-timeout=100 --no-cache-dir .


EXPOSE 8000

CMD ["litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]