ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
        git \
        python3 \
        python3-pip \
        python3-venv \
        libpq-dev \
        postgresql \
        postgresql-contrib && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python3 -m venv /app/env && \
    /app/env/bin/pip install --upgrade pip && \
    /app/env/bin/pip install \
        psycopg2-binary \
        testresources \
        python-dotenv \
        psycopg2

# Clone the repository
RUN git clone https://github.com/rajeshmhaiskar/navigation_authentication_application.git /app/app

# Expose PostgreSQL port
EXPOSE 5432

# Expose your application port (replace PORT_NUMBER with the actual port number your application uses)
EXPOSE 8005

# Start PostgreSQL service
CMD service postgresql start && \
    /bin/bash

