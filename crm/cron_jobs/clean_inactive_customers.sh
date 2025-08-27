#!/bin/bash

# File: crm/cron_jobs/clean_inactive_customers.sh
# Description: Deletes customers with no orders in the past year and logs the number deleted

# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Run Django shell command
DELETED_COUNT=$(python3 manage.py shell -c "
from crm.models import Customer
from datetime import datetime, timedelta
one_year_ago = datetime.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__date__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the number of deleted customers
echo \"$TIMESTAMP - Deleted $DELETED_COUNT customers\" >> /tmp/customer_cleanup_log.txt
