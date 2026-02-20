# Basic Dockerfile for a Django application

FROM python:3.13-bookworm

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# create and set working directory
WORKDIR /app

# copy dependency file first to leverage caching
COPY requirements.txt /app/

# install python deps
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY . /app/

# expose port 8000 for Django
EXPOSE 8000

# default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
