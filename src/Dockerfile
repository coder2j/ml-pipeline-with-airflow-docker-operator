# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for AWS credentials (replace with your credentials)
ENV MINIO_ACCESS_KEY_ID=your_access_key
ENV MINIO_SECRET_ACCESS_KEY=your_secret_key
ENV MINIO_ENDPOINT=your_minio_endpoint
ENV MINIO_BUCKET_NAME=your_bucket_name

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the training and model publishing script
CMD ["python", "train_and_publish.py"]
