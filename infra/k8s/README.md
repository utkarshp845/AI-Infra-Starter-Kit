# Kubernetes

The Kubernetes manifests are starter material for Week 3 of the roadmap.

They are not required for Day 1.

## Important Note

The local Docker Compose version uses a shared file for logs. In production Kubernetes, logs should usually flow to a logging backend instead of being shared through a file volume.

The starter manifests use a shared PersistentVolumeClaim to keep the learning model close to Docker Compose. Your cluster storage class must support the access mode you choose.

## Apply

```bash
kubectl apply -f infra/k8s/demo-service.yaml
kubectl apply -f infra/k8s/ai-sre-assistant.yaml
```

## Production Topics To Add Later

- ConfigMaps and Secrets.
- Resource requests and limits.
- Probes tuned to real startup behavior.
- Horizontal autoscaling.
- Log collection with OpenTelemetry or a platform agent.

