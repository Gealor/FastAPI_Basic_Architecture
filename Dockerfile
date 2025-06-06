# попробовать multi-stage сборку?
FROM python:3.11.12-slim
WORKDIR /app

# Устанавливаем Poetry и отключаем виртуальное окружение
ENV POETRY_VERSION=1.8.2
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}


COPY pyproject.toml poetry.lock ./ 
RUN poetry install --no-root  

COPY src .

CMD ["python", "main.py"]
# ENTRYPOINT ["python", "main.py"]



