# Dockerfile

FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app
