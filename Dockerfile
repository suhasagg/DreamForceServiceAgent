FROM python:3.12-slim
RUN useradd -r -u 10001 app
WORKDIR /app
COPY pyproject.toml .
COPY src ./src
RUN pip install --no-cache-dir .
USER 10001
EXPOSE 8000
CMD ["uvicorn","service_agent.api.main:app","--host=0.0.0.0","--port=8000"]
