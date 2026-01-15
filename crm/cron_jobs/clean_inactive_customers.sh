#!/bin/bash

cd /path/to/alx-backend-graphql_crm || exit 1

DELETED_COUNT=$(python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT" >> /tmp/customer_cleanup_log.txt
