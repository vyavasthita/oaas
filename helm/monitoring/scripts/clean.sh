# Step 1: Uninstall helm chart
helm uninstall monitoring --namespace monitoring

# Step 2: Delete namespace
kubectl delete ns monitoring