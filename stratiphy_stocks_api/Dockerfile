# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Expose the port that the Django app will be running on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
