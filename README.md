# ⚡ AgileOps: Autonomous & Zero-Trust Cloud Pipeline

[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazonaws)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python)](https://www.python.org/)

**Live System Endpoint:** [AgileOps Enterprise Control Center](http://agileops-alb-1111928547.us-east-1.elb.amazonaws.com) *(Note: Link may be inactive post-deployment demonstration)*

## Overview
AgileOps is a production-grade, fault-tolerant cloud architecture designed to eliminate manual deployment fragility. It implements a fully autonomous CI/CD pipeline, zero-trust secrets management, self-healing container orchestration, and a resilient Generative AI intelligence layer natively within AWS.

![AgileOps Architecture](Link-to-your-architecture-diagram-image-here)

## Core Capabilities

### 🚀 Zero-Touch CI/CD Automation
- Commits to the `main` branch automatically trigger **AWS CodePipeline**.
- **AWS CodeBuild** constructs multi-architecture Docker images and securely pushes them to **Amazon ECR**.
- Seamless rolling deployments ensure zero-downtime updates for active users.

### 🛡️ Self-Healing Compute & Orchestration
- Workloads are containerized and managed by **Amazon ECS** on an EC2-backed cluster.
- An **Application Load Balancer (ALB)** routes traffic and performs continuous health checks.
- If a container fails or crashes, ECS automatically terminates it and provisions a healthy replacement within seconds.

### 🔒 Zero-Trust Secrets Management
- No hardcoded credentials or local `.env` files exist in the source code.
- ECS tasks dynamically resolve database passwords and API keys directly from **AWS Systems Manager (SSM) Parameter Store** at runtime.
- Authentication is handled exclusively via passwordless, least-privilege **IAM Roles**.

### 🤖 Resilient GenAI Intelligence Layer
- Features an embedded cloud assistant powered by **Amazon Bedrock (Nova Micro)** via the Converse API.
- Engineered with an application-layer **circuit breaker** to gracefully intercept API rate limits (`ThrottlingException`).
- Activates an instant failover cache during upstream outages, guaranteeing 100% UI uptime without HTTP 500 errors.

### 📡 Event-Driven Observability
- **AWS CodeStar Notifications** and **Amazon EventBridge** monitor pipeline state changes.
- **Amazon SNS** dispatches real-time execution alerts (Success/Failure) directly to engineering inboxes.
- Centralized stdout telemetry and container logs are streamed to **Amazon CloudWatch**.

## Technology Stack
* **Cloud Infrastructure:** AWS ECS, EC2, ALB, ECR
* **CI/CD & Automation:** AWS CodePipeline, CodeBuild, CodeCommit
* **Security & IAM:** AWS SSM Parameter Store, IAM Instance Profiles
* **Observability:** Amazon SNS, EventBridge, CloudWatch
* **AI Integration:** Amazon Bedrock (Nova Micro)
* **Application Runtime:** Python, Flask, Docker, HTML/CSS

## Architecture Failure Modes Tested
1. **Container Crash:** Manually stopping the ECS task results in automated container replacement in < 15 seconds.
2. **Bad Deployment:** Failing health checks on a new deployment triggers the ECS Deployment Circuit Breaker, automatically rolling back to the previous stable revision.
3. **API Throttling:** Exceeding Bedrock token limits triggers the application's try-catch block, serving a cached UI response instead of crashing the server.
