# 🚀 Deployment Guide

Multiple ways to deploy the Iceberg Table Creator for different use cases.

## 🖥️ Local Development

### **Quick Start**
```bash
git clone https://github.com/your-username/iceberg-table-creator.git
cd iceberg-table-creator
./install.sh
./run.sh
```

### **Manual Setup**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run Iceberg_Table_Creator.py
```

## 🐳 Docker Deployment

### **Using Docker Compose (Recommended)**
```bash
# Clone the repository
git clone https://github.com/your-username/iceberg-table-creator.git
cd iceberg-table-creator

# Make sure your credentials are in place
ls ~/.aws/credentials
ls ~/.snowflake/connections.toml

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### **Using Docker directly**
```bash
# Build the image
docker build -t iceberg-table-creator .

# Run with mounted credentials
docker run -d \
  --name iceberg-app \
  -p 8501:8501 \
  -v ~/.aws:/root/.aws:ro \
  -v ~/.snowflake:/root/.snowflake:ro \
  iceberg-table-creator

# View logs
docker logs -f iceberg-app
```

## ☁️ Cloud Deployment

### **AWS ECS (Fargate)**

1. **Push to ECR**:
```bash
# Build and tag
docker build -t iceberg-table-creator .
docker tag iceberg-table-creator:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/iceberg-table-creator:latest

# Push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/iceberg-table-creator:latest
```

2. **ECS Task Definition**:
```json
{
  "family": "iceberg-table-creator",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/icebergTableCreatorRole",
  "containerDefinitions": [
    {
      "name": "iceberg-app",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/iceberg-table-creator:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_HEADLESS",
          "value": "true"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/iceberg-table-creator",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### **Google Cloud Run**

```bash
# Build and push to GCR
docker build -t iceberg-table-creator .
docker tag iceberg-table-creator gcr.io/your-project/iceberg-table-creator
docker push gcr.io/your-project/iceberg-table-creator

# Deploy to Cloud Run
gcloud run deploy iceberg-table-creator \
  --image gcr.io/your-project/iceberg-table-creator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 1Gi \
  --cpu 1
```

### **Azure Container Instances**

```bash
# Create resource group
az group create --name iceberg-rg --location eastus

# Deploy container
az container create \
  --resource-group iceberg-rg \
  --name iceberg-app \
  --image your-registry/iceberg-table-creator:latest \
  --ports 8501 \
  --dns-name-label iceberg-table-creator \
  --memory 1 \
  --cpu 1
```

## 🌐 Streamlit Cloud

1. **Fork the repository** on GitHub
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select the forked repository
   - Set main file: `Iceberg_Table_Creator.py`

3. **Add secrets** in Streamlit Cloud dashboard:
   - AWS credentials
   - Snowflake connection details

## 🔧 Environment Variables

### **Required for Cloud Deployment**

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-west-2

# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

### **Streamlit Configuration**

```bash
# Server settings
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Theme (optional)
STREAMLIT_THEME_PRIMARY_COLOR=#FF6B6B
STREAMLIT_THEME_BACKGROUND_COLOR=#FFFFFF
STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#F0F2F6
STREAMLIT_THEME_TEXT_COLOR=#262730
```

## 🔒 Security Considerations

### **Credentials Management**

1. **Never commit credentials** to version control
2. **Use environment variables** in production
3. **Rotate keys regularly**
4. **Use IAM roles** when possible (AWS ECS, Lambda)
5. **Enable MFA** on cloud accounts

### **Network Security**

1. **Use HTTPS** in production
2. **Restrict access** with security groups/firewalls
3. **Use VPN** for internal deployments
4. **Enable logging** for audit trails

### **Application Security**

```python
# Add to your deployment
import streamlit as st

# Password protection (simple)
def check_password():
    def password_entered():
        if st.session_state["password"] == "your_secure_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", 
                     on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", 
                     on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()
```

## 📊 Monitoring & Logging

### **Health Checks**

```python
# Add to your app
import streamlit as st
import datetime

# Health check endpoint
if st.query_params.get("health") == "check":
    st.json({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0"
    })
    st.stop()
```

### **Logging Setup**

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)
```

## 🚀 Production Checklist

- [ ] **Credentials**: Secure credential management
- [ ] **HTTPS**: SSL/TLS enabled
- [ ] **Monitoring**: Health checks and logging
- [ ] **Backup**: Configuration and data backup
- [ ] **Scaling**: Auto-scaling configured
- [ ] **Updates**: Update strategy defined
- [ ] **Documentation**: Runbooks created
- [ ] **Testing**: Load testing completed
- [ ] **Security**: Security review done
- [ ] **Compliance**: Regulatory requirements met

## 🔄 CI/CD Pipeline

### **GitHub Actions Example**

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Build and push Docker image
      run: |
        docker build -t iceberg-table-creator .
        docker tag iceberg-table-creator:latest $ECR_REGISTRY/iceberg-table-creator:latest
        docker push $ECR_REGISTRY/iceberg-table-creator:latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster production --service iceberg-table-creator --force-new-deployment
```

---

**Choose the deployment method that best fits your infrastructure and security requirements!** 🚀
