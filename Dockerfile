FROM python:3.11.6

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt /code/
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /code/

# Expose the port that the Django development server will run on
# EXPOSE 8000

# # Run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
