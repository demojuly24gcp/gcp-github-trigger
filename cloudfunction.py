import base64
import json
from google.cloud import aiplatform

PROJECT_ID = 'your-project-id'                     # <---CHANGE THIS
REGION = 'your-region'                             # <---CHANGE THIS
PIPELINE_ROOT = 'your-cloud-storage-pipeline-root'  # <---CHANGE THIS

def subscribe(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    # Extract the file that was uploaded
    file_name = event['name']
    bucket_name = event['bucket']
    
    # Optionally, you can check the file type to ensure it's a YAML or JSON
    if file_name.endswith('.yaml') or file_name.endswith('.json'):
        pipeline_spec_uri = f'gs://{bucket_name}/{file_name}'
        
        # Create payload JSON with just the pipeline_spec_uri
        payload_json = {
            "pipeline_spec_uri": pipeline_spec_uri
            # If your pipeline takes parameters, you can add them here
            # "parameter_values": {
            #    "greet_name": "Hello"
            # }
        }
        
        # Trigger the pipeline run with the file path as the spec
        trigger_pipeline_run(payload_json)

def trigger_pipeline_run(payload_json):
    """Triggers a pipeline run.
    Args:
          payload_json: expected in the following format:
            {
              "pipeline_spec_uri": "<path-to-your-compiled-pipeline>"
            }
    """
    pipeline_spec_uri = payload_json['pipeline_spec_uri']
    
    # Initialize the Vertex AI SDK
    aiplatform.init(
        project=PROJECT_ID,
        location=REGION,
    )
    
    # Create a PipelineJob with the specified pipeline YAML or JSON file
    job = aiplatform.PipelineJob(
        display_name='gcs-upload-triggered-pipeline',
        template_path=pipeline_spec_uri,
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
        # If your pipeline has parameters, you can add parameter_values here
        # parameter_values=parameter_values
    )
    
    # Submit the job
    job.submit()
