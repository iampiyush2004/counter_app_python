# Instruction Manual: Kubernetes-based Counting System

## Overview
This system consists of a **Flask-based WebSocket server** and **two clients** that send number spellings sequentially. The system runs in **Docker containers** and is deployed on a **Kubernetes cluster (kind)** with self-healing capabilities and persistent storage.

## 1. Prerequisites
Ensure you have the following installed:
- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Kubernetes (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Kind (Kubernetes in Docker)](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Socket.IO](https://socket.io/)
- [Flask](https://flask.palletsprojects.com/)

## 2. System Components
### **1. Flask Server (`server.py`)**
- Handles WebSocket connections using **Flask-SocketIO**.
- Assigns roles (`client1` and `client2`).
- Stores counted numbers in `numbers.txt` using a **Persistent Volume**.

### **2. Clients (`client1.py` and `client2.py`)**
- Connect to the server via WebSockets.
- `client1` sends odd numbers, `client2` sends even numbers.
- Resume counting from the last saved number.

## 3. Setup Instructions
### **Step 1: Clone the Repository**
```sh
git clone https://github.com/iampiyush2004/counter_app_python.git

```

### **Step 2: Build Docker Images**
```sh
docker build -t flask-server -f server/Dockerfile .
docker build -t client1 -f client/Dockerfile .
docker build -t client2 -f client/Dockerfile .
```

### **Step 3: Create a Kind Cluster**
```sh
kind create cluster --name counting-cluster
```

### **Step 4: Load Docker Images into the Cluster**
```sh
kind load docker-image flask-server --name counting-cluster
kind load docker-image client1 --name counting-cluster
kind load docker-image client2 --name counting-cluster
```

### **Step 5: Deploy to Kubernetes**
```sh
kubectl apply -f k8s-deployments.yaml
```

### **Step 6: Verify Deployment**
```sh
kubectl get pods
```
All pods should be running. If any pod crashes, Kubernetes will restart it automatically.

### **Step 7: Check Logs**
To monitor server and client activity:
```sh
kubectl logs -l app=flask-server
kubectl logs -l app=client1
kubectl logs -l app=client2
```

## 4. How It Works
1. **Clients connect to the Flask WebSocket server.**
2. **Server assigns `client1` and `client2`.**
3. **Counting starts once both clients are connected.**
4. **Each client sends numbers alternately (odd/even).**
5. **Numbers are stored in `numbers.txt` (Persistent Volume).**
6. **If a client or server crashes, Kubernetes restarts the affected pod, and counting resumes.**

## 5. Failure Handling & Troubleshooting
### **Check Pod Status**
```sh
kubectl get pods
```
If a pod is stuck in **CrashLoopBackOff**, check logs:
```sh
kubectl logs <pod-name>
```

### **Manually Restart a Pod**
```sh
kubectl delete pod <pod-name>
```
Kubernetes will automatically restart it.

### **Test Cluster Resilience**
Kill a pod and see if Kubernetes restarts it:
```sh
kubectl delete pod -l app=client1
```
Client1 should reconnect automatically.

## 6. Stopping and Cleaning Up
### **Stop the System**
```sh
kubectl delete -f k8s-deployments.yaml
```

### **Delete the Cluster**
```sh
kind delete cluster --name counting-cluster
```

## 7. Conclusion
This system demonstrates **WebSocket-based real-time communication**, **Kubernetes self-healing**, and **state persistence with Persistent Volumes**. It ensures **fault tolerance** and can recover from pod failures while continuing the counting sequence.

**Next Steps:** Extend the system with a frontend to visualize the counting process in real time.

