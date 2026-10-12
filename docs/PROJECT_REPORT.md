# AI-Powered Business Automation System Using Artificial Intelligence

## Abstract
This project proposes a web-based business automation platform that centralizes customer records, tracks sales leads, analyzes inquiries with a generative AI service, prepares draft responses, and supports controlled email and follow-up workflows. A Django application renders the interface and enforces authentication and business rules. MySQL stores persistent records. A scheduled worker processes due follow-ups, while the dashboard presents operational indicators.

## Problem Statement
Small businesses often manage inquiries through disconnected email threads and spreadsheets. Manual triage, delayed replies, inconsistent record keeping and missed follow-ups can reduce operational efficiency. The proposed system centralizes these activities and uses AI assistance while preserving human approval for outbound responses.

## Objectives
- Maintain customer and lead records in one application.
- Receive and persist customer inquiries.
- Use AI to classify inquiry intent and draft a response.
- Require human approval before sending AI-generated email.
- Schedule follow-ups and record activity.
- Display counts, pipeline value and inquiry trends.
- Apply authentication, validation, audit logging and tests.

## Scope
The core version includes Django templates, MySQL models, a Gemini integration, SMTP email approval, Celery/Redis scheduling, and a dashboard. Voice, WhatsApp and calendar integration are optional future extensions.

## Methodology
Requirements analysis → architecture and schema design → module implementation → integration → test execution → deployment preparation → documentation.

## System Modules
1. Authentication and access control.
2. Customer management.
3. Lead pipeline management.
4. Public and internal inquiry intake.
5. AI analysis and draft generation.
6. Email approval and delivery.
7. Scheduled follow-up processing.
8. Activity logging and analytics.

## Database Design
- Customer: name, email, phone, company, timestamps.
- Lead: customer foreign key, title, description, status, priority, source, estimated value.
- Inquiry: customer foreign key, optional lead foreign key, original message, AI intent, summary, draft response and status.
- EmailApproval: inquiry foreign key, recipient, subject, body, approval status, approver and sent timestamp.
- FollowUp: inquiry foreign key, due time, status and sent timestamp.
- ActivityLog: optional inquiry foreign key, event, details and timestamp.

## Security and Privacy
The application uses Django authentication, CSRF protection, ORM-based database access, environment-based secrets and human approval for generated outbound emails. Production deployment must use HTTPS, secure cookies, restricted database networking, least-privilege accounts, log redaction, data retention rules and tested backups. AI output is not trusted without validation.

## Testing
Run `python manage.py test`. Record actual results for login restrictions, customer and lead CRUD, inquiry intake, AI error handling, email approval, follow-up scheduling, and dashboard metrics. Do not claim test results until the commands have been executed in the target environment.

## Limitations
AI output quality depends on prompt design and model availability. Email sending depends on SMTP provider rules. Scheduled jobs require Redis and active worker/beat processes. This initial version requires configuration and environment-specific validation.

## Future Enhancements
Multilingual and voice interfaces, WhatsApp integration, calendar scheduling, richer lead-scoring models, role-based approval policies, observability, and production deployment on AWS.

## Conclusion
The project demonstrates an integrated web workflow for customer inquiry handling, AI-assisted response preparation, lead management, controlled communication, and follow-up automation. Evaluation should be based on tested workflows and documented measurements.
