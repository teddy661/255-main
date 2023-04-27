#!/bin/bash
IMAGE_NAME=lab3
APP_NAME=lab3
NAMESPACE=w255

# minikube start --kubernetes-version=v1.21.7 --memory 4096 --cpus 4
# minikube addons enable metrics-server

# rebuild and run the new image
cd ${APP_NAME}
docker build -t ${IMAGE_NAME} .

# apply yamls for building environment
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f yamls/namespaces.yaml
sleep 5
kubectl apply -f yamls
sleep 5
kubectl port-forward -n ${NAMESPACE} svc/${APP_NAME} 8000:8000 &
export PORT_FORWARD_PID=$!

# wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 5
    fi
done

# output and tail the logs for the api deployment
kubectl logs -n ${NAMESPACE} -l app=${APP_NAME}

# cleanup
kubectl delete -f yamls
kill $PORT_FORWARD_PID
