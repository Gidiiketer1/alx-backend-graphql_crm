# CRM Celery Report Setup

## Requirements
- Redis
- Python dependencies from requirements.txt

## Setup Steps

1. Install Redis and start it on localhost:6379
2. Run migrations:
   python manage.py migrate
3. Start Celery worker:
   celery -A crm worker -l info
4. Start Celery Beat:
   celery -A crm beat -l info
5. Verify logs:
   /tmp/crm_report_log.txt
