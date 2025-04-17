FROM python:3.11.12-slim
WORKDIR /app

# Устанавливаем Poetry и отключаем виртуальное окружение
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock . 
RUN poetry install --no-root  

COPY src .

CMD ["python", "main.py"]
# ENTRYPOINT ["python", "main.py"]



