FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y procps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#mac dinh chay API, se override khi chay docker run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]