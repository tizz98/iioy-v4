#!/usr/bin/env bash

set -eufx -o pipefail

if [ -z ${UPLOAD_BUCKET+x} ]; then
    echo "UPLOAD_BUCKET env var must be set"
    exit 1;
fi
if [ -z ${DISTRIBUTION_ID+x} ]; then
    echo "DISTRIBUTION_ID env var must be set"
    exit 1;
fi

cd iioy-frontend
yarn build
aws s3 sync build/ s3://$UPLOAD_BUCKET --acl public-read --exclude '*.DS_Store*'
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths '/*'
