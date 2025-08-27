# CRM Celery Report Setup

## 1. Installation

Install Redis and Python dependencies:

```bash
sudo apt install redis-server
pip install -r requirements.txt

```
## 2. Apply Django migrations:

python manage.py migrate


### 3. Start Celery worker:

celery -A crm worker -l info


## 4. Start Celery Beat:

celery -A crm beat -l info


## 5. Verify logs:

cat /tmp/crm_report_log.txt


---
