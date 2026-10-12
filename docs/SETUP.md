# Setup and Database Notes

## MySQL
```sql
CREATE DATABASE ai_business_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ai_business_user'@'localhost' IDENTIFIED BY 'replace-with-a-strong-password';
GRANT ALL PRIVILEGES ON ai_business_db.* TO 'ai_business_user'@'localhost';
FLUSH PRIVILEGES;
```

Set matching `DB_*` variables in `.env`. Keep `.env` out of version control.

## First run
```powershell
python manage.py check
python manage.py makemigrations customers leads inquiries automations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Gemini and SMTP
Set `GEMINI_API_KEY` to a valid key and confirm model access. Set SMTP host, port, username, app password, and sender address. Use provider-specific app passwords where required. Do not put credentials into source files.

## Common issues
- `Access denied`: verify MySQL user, password, host and grants.
- Connection refused: ensure MySQL is running and `DB_PORT` matches.
- `mysqlclient` build failure: use Python 3.11/3.12 and follow the driver error output.
- AI unavailable: verify the key, selected model access, network and API quota.
- Email failure: verify SMTP credentials, TLS and sender permissions.
