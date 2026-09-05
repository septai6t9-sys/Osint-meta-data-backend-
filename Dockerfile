FROM python:3.10-slim

# System level par exiftool install karna
RUN apt-get update && apt-get install -y exiftool && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki sara code copy karna
COPY . .

EXPOSE 5000

# Server chalu karne ke liye command
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
