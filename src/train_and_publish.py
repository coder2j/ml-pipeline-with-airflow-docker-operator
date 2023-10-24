import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from minio import Minio
from minio.error import S3Error

# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    os.environ.get('MINIO_ENDPOINT'),  # Replace with your MinIO server address and port
    access_key=os.environ.get('MINIO_ACCESS_KEY_ID'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,  # Set to True if using HTTPS
)

# Define the bucket name and object key for the data.csv file
bucket_name = os.environ.get('MINIO_BUCKET_NAME')
data_csv_key = "datasets/data.csv"

# Download the data.csv file from MinIO
try:
    minio_client.fget_object(bucket_name, data_csv_key, "data.csv")
    print(f"Downloaded data.csv from MinIO: s3://{bucket_name}/{data_csv_key}")
except S3Error as e:
    print(f"Error downloading data.csv from MinIO: {e}")

# Load your dataset from the downloaded CSV file
data = pd.read_csv("data.csv")

# Use the data for machine learning training
# (Rest of your machine learning code here)

# Train a regression model
X = data[['feature1', 'feature2']]
y = data['target']
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'regression_model.pkl')

# Define the object key for the trained model in MinIO
model_key = "models/regression_model.pkl"

# Upload the trained model to MinIO
try:
    minio_client.fput_object(bucket_name, model_key, "regression_model.pkl")
    print(f"Model uploaded to MinIO: s3://{bucket_name}/{model_key}")
except S3Error as e:
    print(f"Error uploading model to MinIO: {e}")
