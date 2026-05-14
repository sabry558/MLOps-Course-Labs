FROM python:3.14-slim

WORKDIR /project

COPY pyproject.toml README.md ./

# Copy the app/ directory BEFORE we pip install . 
COPY app/ app/

RUN pip install --upgrade pip && \
    pip install .

COPY data/ data/
COPY main.py .

EXPOSE 8000

CMD ["litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]