FROM ubuntu:latest as builder

LABEL maintainer="Ariel Betti ariel.betti@gmail.com"
LABEL version="1.0"
LABEL description="EcoCode aims to minimize the impacts of global warming through a practical and sustainable approach."

# Install build dependencies if needed
RUN apt-get update \
	&& apt-get install -y build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Final stage
FROM ubuntu:latest

# Minimal installation, copying only necessary binaries or artifacts from the build stage
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /usr/bin/pip3 /usr/bin/pip3

# Install dependencies
RUN apt-get update \
	&& apt-get install -y libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Update pip and install dependencies
RUN pip3 install --upgrade pip \
	&& pip3 install --no-cache-dir -r requirements.txt

# Expose port to containers
EXPOSE 8080

# Command to run on the server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]