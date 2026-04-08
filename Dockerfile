FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir pydantic openenv-core

ENV API_BASE_URL="https://router.huggingface.co/v1"
ENV MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.3"
ENV PORT=7860

EXPOSE 7860

CMD ["python", "app.py"]