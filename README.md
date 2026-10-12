# AI-Powered Business Automation System

A Django-template application for customer and lead management, AI-assisted inquiry analysis, human-approved email responses, follow-up scheduling, and operational analytics. Built from the workflow in the supplied project reference.

## Requirements
- Python 3.11 or 3.12
- MySQL 8.x
- Redis for scheduled background work
- Gemini API key for AI analysis
- SMTP account for sending emails

## Local setup (Windows PowerShell)
1. Install MySQL Server and create the database/user using `docs/SETUP.md`.
2. Create and activate a virtual environment:
   ```powershell
   py -3.11 -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`, then set real credentials. Never commit `.env`.
4. Run:
   ```powershell
   python manage.py check
   python manage.py makemigrations customers leads inquiries automations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/`; login and visit the public form at `/inquiries/new/`.

## Background follow-ups
Install and start Redis, then run in separate terminals:
```powershell
celery -A config worker --loglevel=INFO --pool=solo
celery -A config beat --loglevel=INFO
```
Follow-up jobs run when due. Configure SMTP before sending real emails.

## Email safety
AI replies are saved as drafts and require a logged-in user to approve sending. Do not enable unattended sending until business policies, recipient consent, rate limits, retries, and audit controls have been tested.

## Tests
```powershell
python manage.py test
```

## Deployment
See `docs/DEPLOYMENT.md`. This scaffold is a starting implementation, not a claim that external services or production deployment have been verified.


## Verification status
Python syntax compilation was checked when this scaffold was generated. The application has not been run against your local MySQL instance, Gemini credentials, SMTP provider, or Redis worker; those integrations must be configured and tested on your machine. Review and test all workflows before submission or production use.
