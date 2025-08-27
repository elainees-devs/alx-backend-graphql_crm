# crm/settings.py
from alx_backend_graphql.settings import *

# Ensure INSTALLED_APPS includes 'django_crontab'
INSTALLED_APPS += [
    'django_crontab',
]

# Add CRONJOBS
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

