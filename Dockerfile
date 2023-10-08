FROM ubuntu:latest

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install libpq-dev
RUN apt-get install -y libpq-dev

# Work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy other project files
COPY . .

# Expose a port to Containers
EXPOSE 8080

# Command to run on server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
