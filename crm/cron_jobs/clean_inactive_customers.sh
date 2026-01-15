#!/bin/bash

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED_COUNT=$(python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
count, _ = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
).delete()

print(count)
EOF
)

echo "$TIMESTAMP Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
