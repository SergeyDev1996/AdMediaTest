import os
import django
import random
from datetime import datetime, timedelta

# Setup Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdMediaTest.settings')
django.setup()

# Import your models here
from spend.models import SpendStatistic
from revenue.models import RevenueStatistic

# Clean up existing data
SpendStatistic.objects.all().delete()
RevenueStatistic.objects.all().delete()

# Create test data
for i in range(10):
    date = datetime.now() - timedelta(days=i)

    # Replace with the actual fields of your SpendStatistic model
    spend_stat = SpendStatistic(
        date=date,
        name=f"Spend Name {i}",
        spend=random.uniform(100, 1000),
        # ... other fields ...
    )
    spend_stat.save()

    # Replace with the actual fields of your RevenueStatistic model
    revenue_stat = RevenueStatistic(
        date=date,
        name=f"Revenue Name {i}",
        revenue=random.uniform(100, 1000),
        spend=spend_stat,
        # ... other fields ...
    )
    revenue_stat.save()
