from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


default_args = {
    'owner': 'coder2j',
    'start_date': datetime(2023, 1, 1),
    # Add other default args like retries, etc.
}

with DAG(
    dag_id='dag_ml_pipeline_docker_operator_v01',
    default_args=default_args,
    description='Run ML pipeline with docker operator in Airflow locally',
    schedule_interval=None,  # Set your desired schedule interval or use None for manual triggering
) as dag:
    
    dataset_creation_task = BashOperator(
        task_id="faked_dataset_creation_task",
        bash_command="""
echo "Hey the dataset is ready, let's trigger the training process"
"""
    )

    model_train_and_publish_task = DockerOperator(
        task_id='docker_model_train_and_publish_task',
        docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        api_version='auto',  # Use 'auto' to let Docker select the appropriate API version
        auto_remove=True,  # Remove the container when the task completes
        image='regression-training-image:v1.0',  # Replace with your Docker image and tag
        container_name="training_my_awesome_model",
        environment={
            'MINIO_ENDPOINT': 'host.docker.internal:9000',
            'MINIO_ACCESS_KEY_ID': 'nOmjo49pMf08zwZ4',
            'MINIO_SECRET_ACCESS_KEY': 'DjA2RQh85I6JtDO9Kho2667XNmMNzjfo',
            'MINIO_BUCKET_NAME': 'coder2j-awesome-ml-artifacts',
        },  # Set environment variables inside the contain
        command=['python', 'model_tuning.py'],  # Replace with the command you want to run inside the container
        # network_mode='bridge',  # Specify the network mode if needed
        # volumes=['/host/path:/container/path'],  # Mount volumes if needed
        dag=dag,
    )

    dataset_creation_task >> model_train_and_publish_task



