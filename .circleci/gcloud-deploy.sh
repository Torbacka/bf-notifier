#!/bin/sh
set -x
DIR=$(dirname "$(readlink -f "$0")")

docker load -i /tmp/workspace/latest
. $DIR/transform_vars.sh

echo $ACCT_AUTH | base64 --decode -i > ${HOME}/account-auth.json ;
gcloud auth activate-service-account --key-file ${HOME}/account-auth.json ;
gcloud config set project $PROJECT_NAME ;
gcloud --quiet config set container/cluster $CLUSTER_NAME ;
gcloud config set compute/zone ${CLOUDSDK_COMPUTE_ZONE} ;
gcloud --quiet container clusters get-credentials $CLUSTER_NAME ;
curl https://kubernetes-helm.storage.googleapis.com/helm-v2.4.2-linux-amd64.tar.gz | tar xfz -
mv linux-amd64/helm .

docker ps -a
docker tag zensum/$ZENS_NAME:$CIRCLE_SHA1 gcr.io/zens-main/$ZENS_NAME:$CIRCLE_SHA1
docker tag zensum/$ZENS_NAME:$CIRCLE_SHA1 gcr.io/zens-main/$ZENS_NAME:latest
gcloud docker -- push gcr.io/zens-main/$ZENS_NAME:$CIRCLE_SHA1

./helm upgrade $HELM_NAME deploy/$ZENS_NAME/ --set image.tag=$CIRCLE_SHA1
