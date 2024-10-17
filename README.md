# gcp-github-trigger
ML-OPS CICD with GCP

vague READEME file will update later

enable vertex ai api

enable cloud build api
create a host connection in cloud build with your github repo and select repository
then create a trigger in cloud build for commits to the main repo

create a gcr repo for docker images and update the name in the cloudbuild.yaml along with project id and region

create a service account for your cloud function to be able to run the pipeline trigger
go to cloud run functions and create a new function for updates in your gcs bucket - object finalization
in run time select python 3.8 and in entry point replace the placeholder with subscribe
replace the code with the cloudfunction.py with appropriate changes
and replace requirements.txt with 
google-api-python-client>=1.7.8,<2
google-cloud-aiplatform[pipelines]


now go to your github repo and commit with any changes
this should trigger a cloud build run which when completed triggers a cloud function which creates the pipeline

** wont work with free account
