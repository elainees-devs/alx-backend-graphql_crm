# CRM Celery Report Setup

This document explains how to set up and run the weekly CRM report using Celery and Celery Beat in the CRM application.

```bash
## 1. Install Redis and Python Dependencies
sudo apt install redis-server
pip install -r requirements.txt

## 2. Apply Django Migrations
python manage.py migrate

## 3. Configure Celery in Django
### - Ensure crm/celery.py initializes Celery with Redis broker
### - Ensure crm/__init__.py loads the Celery app
### - Ensure crm/settings.py includes 'django_celery_beat' in INSTALLED_APPS
###   and defines CELERY_BEAT_SCHEDULE for generate_crm_report

## 4. Start Celery Worker
celery -A crm worker -l info

## 5. Start Celery Beat
celery -A crm beat -l info

## 6. Verify Logs
cat /tmp/crm_report_log.txt
### Expected log format:
### YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue

## 7. Notes
### - The `generate_crm_report` task runs every Monday at 06:00 by default.
### - Ensure the GraphQL server is running at http://localhost:8000/graphql.
### - Any errors during task execution are logged in /tmp/crm_report_log.txt.
