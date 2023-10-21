# Use Python 3.6.8 as the base image
FROM python:3.6.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run extract.py with an argument
#CMD ["python", "extract.py"]
ENTRYPOINT ["python", "extract.py"]
