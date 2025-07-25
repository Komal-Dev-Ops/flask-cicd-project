# Flask CI/CD Pipeline on AWS EC2..

A complete CI/CD pipeline for deploying a Flask web application on AWS EC2 using GitHub Actions, Terraform, Ansible, and Docker.

## 🚀 Architecture

- **Flask**: Python web framework
- **Docker**: Containerization
- **AWS EC2**: Cloud hosting
- **Terraform**: Infrastructure as Code
- **Ansible**: Configuration Management
- **GitHub Actions**: CI/CD Pipeline

## 📋 Prerequisites

Before setting up this project, ensure you have:

### 1. AWS Account & CLI
- AWS account with programmatic access
- AWS CLI configured with appropriate permissions
- EC2, VPC, and IAM permissions

### 2. SSH Key Pair
```bash
# Generate SSH key pair for EC2 access
ssh-keygen -t rsa -b 4096 -f ~/.ssh/flask-cicd-key
```

### 3. Docker Hub Account
- Docker Hub account for image storage
- Create repository: `your-username/flask-cicd`

### 4. Local Tools
```bash
# Install required tools
pip install ansible
curl -LO https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
unzip terraform_1.5.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

## 🛠️ Setup Instructions

### Step 1: Clone and Prepare Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd flask-cicd-project

# Initialize git if needed
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions, and add:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `EC2_PUBLIC_KEY` | Contents of `~/.ssh/flask-cicd-key.pub` | `ssh-rsa AAAAB3NzaC1yc2E...` |
| `EC2_PRIVATE_KEY` | Contents of `~/.ssh/flask-cicd-key` | `-----BEGIN RSA PRIVATE KEY-----...` |
| `DOCKER_USERNAME` | Docker Hub username | `your-dockerhub-username` |
| `DOCKER_PASSWORD` | Docker Hub password/token | `your-dockerhub-password` |

### Step 3: Manual Infrastructure Deployment (First Time)

```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Create terraform.tfvars file
cat > terraform.tfvars << EOF
aws_region = "us-east-1"
project_name = "flask-cicd"
instance_type = "t3.micro"
public_key = "$(cat ~/.ssh/flask-cicd-key.pub)"
EOF

# Plan and apply infrastructure
terraform plan
terraform apply

# Note the output values
terraform output
```

### Step 4: Manual Deployment with Ansible (First Time)

```bash
# Get EC2 public IP from Terraform output
EC2_IP=$(cd terraform && terraform output -raw instance_ip)

# Update Ansible inventory
sed -i "s/YOUR_EC2_PUBLIC_IP/$EC2_IP/g" ansible/inventory.ini

# Deploy application
cd ansible
ansible-playbook -i inventory.ini deploy.yml
```

### Step 5: Verify Deployment

```bash
# Check application health
curl http://$EC2_IP:5000/health

# Visit in browser
echo "Application URL: http://$EC2_IP:5000"
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Test Stage**: Runs linting and unit tests
2. **Build Stage**: Creates and pushes Docker image
3. **Deploy Stage**: 
   - Provisions/updates AWS infrastructure with Terraform
   - Deploys application using Ansible
   - Performs health checks

### Pipeline Triggers

- **Push to main**: Full CI/CD pipeline
- **Push to develop**: Test and build only
- **Pull Request**: Test only

## 📁 Project Structure

```
flask-cicd-project/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Local development
├── templates/
│   └── index.html             # HTML template
├── tests/
│   └── test_app.py            # Unit tests
├── terraform/                  # Infrastructure as Code
│   ├── main.tf                # Main Terraform config
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Output values
│   └── user_data.sh          # EC2 initialization
├── ansible/                    # Configuration Management
│   ├── deploy.yml             # Deployment playbook
│   ├── inventory.ini          # Server inventory
│   └── ansible.cfg           # Ansible configuration
└── .github/workflows/
    └── ci-cd.yml              # GitHub Actions pipeline
```

## 🧪 Local Development

### Run Locally with Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Run Locally with Docker

```bash
# Build and run container
docker build -t flask-cicd .
docker run -p 5000:5000 flask-cicd

# Or use Docker Compose
docker-compose up --build
```

### Run Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Application port | `5000` |

### AWS Configuration

- **Region**: us-east-1 (configurable)
- **Instance Type**: t3.micro (free tier eligible)
- **AMI**: Ubuntu 22.04 LTS
- **Storage**: 20GB encrypted EBS

### Security Groups

- **Port 22**: SSH access
- **Port 80**: HTTP access  
- **Port 5000**: Flask application

## 📊 Monitoring & Health Checks

### Health Endpoints

- `GET /health` - Application health status
- `GET /api/info` - Application information

### GitHub Actions Health Checks

The pipeline includes automated health checks:
- Container health check in Docker Compose
- HTTP health check after deployment
- Application response validation

## 🚨 Troubleshooting

### Common Issues

#### 1. SSH Connection Failed
```bash
# Check security group allows SSH (port 22)
# Verify private key permissions
chmod 600 ~/.ssh/flask-cicd-key

# Test SSH connection
ssh -i ~/.ssh/flask-cicd-key ubuntu@$EC2_IP
```

#### 2. Docker Build Failed
```bash
# Check Dockerfile syntax
docker build -t flask-cicd .

# View build logs
docker build --no-cache -t flask-cicd .
```

#### 3. Terraform Apply Failed
```bash
# Check AWS credentials
aws sts get-caller-identity

# Validate Terraform files
terraform validate

# Check state
terraform show
```

#### 4. Ansible Deployment Failed
```bash
# Test connectivity
ansible -i inventory.ini flask_servers -m ping

# Run with verbose output
ansible-playbook -i inventory.ini deploy.yml -vvv
```

### Logs and Debugging

```bash
# View application logs
ssh -i ~/.ssh/flask-cicd-key ubuntu@$EC2_IP
docker logs $(docker ps -q)

# View system logs
sudo journalctl -u docker

# Check disk space
df -h
```

## 🔐 Security Best Practices

### Implemented Security Measures

- ✅ Encrypted EBS volumes
- ✅ Security groups with minimal required access
- ✅ SSH key-based authentication
- ✅ No hardcoded secrets in code
- ✅ GitHub secrets for sensitive data
- ✅ Docker non-root user (recommended)

### Additional Recommendations

- Enable AWS CloudTrail for audit logging
- Set up AWS Config for compliance monitoring
- Use AWS Systems Manager for secure instance access
- Implement container scanning in CI/CD pipeline
- Set up monitoring with CloudWatch

## 💰 Cost Optimization

### AWS Free Tier Usage

- **EC2 t3.micro**: 750 hours/month (free tier)
- **EBS**: 30GB storage/month (free tier)
- **Data Transfer**: 1GB/month (free tier)

### Cost Management

```bash
# Use smaller instance types for testing
# Clean up resources when not needed
terraform destroy

# Monitor usage in AWS Cost Explorer
# Set up billing alerts
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Ansible Documentation](https://docs.ansible.com/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Deploying! 🚀**
