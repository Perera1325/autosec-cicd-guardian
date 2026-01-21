FROM python:3.12-slim

WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose dashboard port
EXPOSE 5000

# Run dashboard with Gunicorn (production)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "dashboard.app:app"]
