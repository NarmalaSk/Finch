### Finch service

Python fastapi service runs on port 8080 with endpoints
```
http://service/health
http://service/api
...
```
### CI/CD Flow
<img width="1235" height="501" alt="image" src="https://github.com/user-attachments/assets/5a5f0874-7b41-4f57-9053-8956851a6367" />


### Workload Federation Pool and Provider

Just create a workload federation id using service impersonation or direct access
Docs for Creating WIF gihtub[https://github.com/google-github-actions/auth]

Just replace the Principal id and service acc email in build infra.yml file


### Infrastructure

Intro Finch is a sample fast api runs using unicorn I have deployed the api in Google kubernetes engine 
Infrastructure I have used is 2 Google Kubernetes Clusters

To create Infra just run

spin-infra workflow 
- It creates Two gke clusters for Development and Production in us-central1-a region


### CICD

The github action workflow basically buils docker image and deploys to app to gke and exposes as service

Replace this creds in the deploy-dev and deploy-prod workflows 
```
regsitry url
cluster name
region
service account 
principal id
```

### Run dev&prod Pipeline

Create a dev Branch ,commit a small change dev pipeline runs
same for prod make commit in main branch
