# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory to the container
COPY . .

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the project dependencies
RUN pip install -r requirements.txt

# Download wait-for-it.sh script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expose the port that the Django app will be running on
EXPOSE 8000

# Run migrations and start the Django development server
CMD sh -c './wait-for-it.sh db:5432 -- python manage.py makemigrations && python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:8000'