#!/bin/bash
export model_number=$(head /dev/urandom | LC_CTYPE=C tr -dc 0-9 | head -c 4 ; echo '')
export project_name=$1
export job_id=$2
export model_name=model-$model_number
export namespace="foundations-scheduler-test"

echo 'configuring config map for model package server'
envsubst < submission_config.yaml | kubectl apply -f -
echo 'Successfully configured config map for $job_id'

cat kubernetes-deployment.envsubst.yaml | envsubst | kubectl create -f -
kubectl apply -f model-serving-environment.yaml

echo "Preparing $model_name for serving"

model_pod=$(kubectl -n foundations-scheduler-test get po | grep $model_name | awk '{print $1}')

model_status () {
    echo $(kubectl -n foundations-scheduler-test get po | grep $model_name | awk '{print $3}')
}

echo "Waiting for $model_name to be ready"
while [ "Pending" == $(model_status) ] || [ "" == $(model_status) ] || [ "ContainerCreating" == $(model_status) ]
do 
    sleep 2
done

echo ''
echo Model $model_name in $project_name has started, please run:
echo -e '    ' foundations serve stop --project_name=$project_name $model_name 
echo if an error has occurred or you wish to stop the server
echo ''
kubectl logs -f -n foundations-scheduler-test $model_pod