# Docker and AWS Deployment Guide

## Local Docker Compose
This compose file is a development baseline. Before public deployment, use managed secrets, a non-debug configuration, HTTPS, backups, restricted network rules, and a production-grade application server.

```powershell
docker compose up --build
```

## AWS outline
1. Create an AWS account and a least-privilege IAM role.
2. Provision an RDS MySQL instance in private subnets; restrict its security group to the application only.
3. Store Django, database, Gemini and SMTP secrets in AWS Secrets Manager or Parameter Store.
4. Build the application image and push it to Amazon ECR.
5. Deploy to ECS Fargate behind an Application Load Balancer with HTTPS.
6. Run database migrations as a controlled release step.
7. Deploy Celery worker and Celery Beat as separate services.
8. Configure logs, health checks, alarms, database backups and restore testing.
9. Set `DEBUG=False`, configure allowed hosts, secure cookies, HTTPS redirects and CSRF trusted origins.
10. Test rollback, access controls and recovery before demonstrating production readiness.

No cloud resources are created by this guide; AWS deployment requires the owner's account and explicit configuration.
