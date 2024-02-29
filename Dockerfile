# Use a Python 3.10 base image
FROM python:3.10

# Update package lists and upgrade installed packages
RUN apt-get update && \
    apt-get upgrade -y

# Install git
RUN apt-get install -y git

# Clone the repository
RUN git clone https://github.com/rajeshmhaiskar/navigation_authentication_application.git

# Install Python virtual environment
RUN apt-get install -y python3.10-venv

# Create and activate virtual environment
RUN python3 -m venv env
ENV PATH="/env/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install psycopg2-binary testresources python-dotenv

# Install PostgreSQL and its dependencies
RUN apt-get install -y postgresql postgresql-contrib libpq-dev

# Start PostgreSQL service
RUN service postgresql start

# Expose PostgreSQL port
EXPOSE 5432

# Restart PostgreSQL service
RUN service postgresql restart
