# iioy
"Is It Out Yet?" - the age old question right before going to see a movie

# Running

## Backend
```bash
docker-compose up --build
```

## Frontend
```bash
cd iioy-frontend && yarn start
```

# Deploying frontend to S3/cloudfront
```bash
UPLOAD_BUCKET=iioy-testing DISTRIBUTION_ID=xxxxxxxxxxxxxx bin/deploy_frontend.sh
```
