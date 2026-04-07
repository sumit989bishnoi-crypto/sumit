FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces port
EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
