#!/bin/bash

root_dir=$1

kubectl create namespace istio-system
kubectl create -f "${root_dir}/global-ressources/mesh/istio-manifest-files"


${root_dir}/global-ressources/mesh/istio-1.23.3/bin/istioctl install -y -f ${root_dir}/global-ressources/mesh/install_inbound_request_metric.yaml

kubectl label namespace default istio-injection=enabled

kubectl create -f ${root_dir}/global-ressources/mesh/istio-1.23.3/samples/addons/prometheus.yaml

for deployment in $(kubectl get deployments -n monitoring -o jsonpath='{.items[*].metadata.name}'); do
  kubectl rollout status deployment/$deployment -n monitoring
done
