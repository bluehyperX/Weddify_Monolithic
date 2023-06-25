# Base image with Python and dependencies
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /Weddify

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . .

# Expose the port on which Django runs (default is 8000)
EXPOSE 8000

# Run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
