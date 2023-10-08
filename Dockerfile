FROM python:3.9-slim

# Install libpq-dev
RUN apt-get update && apt-get install -y libpq-dev

# Work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy other project files
COPY . .

# Expose a port to Containers
EXPOSE 8080

# Command to run on server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]