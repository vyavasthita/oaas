# Step 1: Install kube-prometheus-stack
echo "Step 1: Installing kube-prometheus-stack"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
echo "****************************************************************"
echo "Installing kube-prometheus-stack... Done"
echo "****************************************************************"

# Step 2: Deploy the chart into a new namespace "monitoring"
echo "Step 2: Deploy the chart into a new namespace 'monitoring'"
kubectl create ns monitoring
echo "****************************************************************"
echo "Deploy the chart into a new namespace... Done"
echo "****************************************************************"

# Step 3: Install monitoring chart
echo "Step 3: Installing monitoring chart"
cd helm/monitoring/scripts && \
helm install monitoring prometheus-community/kube-prometheus-stack \
-n monitoring \
-f ../custom_kube_prometheus_stack.yml && \
cd ../../..
echo "****************************************************************"
echo "Installing monitoring chart... Done"
echo "****************************************************************"

# Step 4: Verify the Installation
echo "Step 4: Verifying the installation..."
kubectl get all -n monitoring
echo "****************************************************************"
echo "Installation verification... Done"

sleep 10

# Step 5: Prometheus UI: Port Forwarding
echo "Step 5: Port forwarding Prometheus UI to http://localhost:9090"
kubectl port-forward service/prometheus-operated -n monitoring 9090:9090 &
echo "****************************************************************"

# Step 6: Grafana UI: Port Forwarding
echo "Step 6: Port forwarding Grafana UI to http://localhost:8080"
kubectl port-forward service/monitoring-grafana -n monitoring 8080:80 &
echo "****************************************************************"

# Step 7: Alert Manager UI: Port Forwarding
echo "Step 7: Port forwarding Alert Manager UI to http://localhost:9093"
kubectl port-forward service/alertmanager-operated -n monitoring 9093:9093 &
echo "****************************************************************"

echo "****************************************************************"
echo "**************************** DONE ************************************"
echo "****************************************************************"