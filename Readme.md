### setup

### Infrastructure
Build-infra.yml
Terraform components
1 vpc 
2 gke clusters
1 workload fed identity pool
1 workload fed provider id
1 artifact regsitry



### CICD
deploy-to-dev.yml
#### push -> dev branch
Code chechkout

code tests

build docker image 

push to registry

deploy to dev gke cluster 

#### push -> prod branch
deploy-to-prod.yml
code checkout 
gcloud login
deploy to prod cluster GKE
