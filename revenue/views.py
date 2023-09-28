from itertools import chain

from django.db.models import Sum, F, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.response import Response

from spend.models import SpendStatistic
from .models import RevenueStatistic
from .serializers import RevenueStatisticSerializer

# The task wasn't really clear, so I made a few options:


# FIRST It aggregates using the ForeignKey relation and aggregate the related values.
class RevenueStatisticListView(generics.ListAPIView):
    serializer_class = RevenueStatisticSerializer
    def get_queryset(self):
        # Perform a join on RevenueStatistic and SpendStatistic using the foreign key relationship.
        # Then, group by 'date' and 'name' and perform the aggregation on both tables.
        queryset = RevenueStatistic.objects.select_related('spend').values('date', 'name').annotate(
            total_revenue=Sum('revenue', output_field=DecimalField(max_digits=9, decimal_places=2)),
            total_spend=Sum(Coalesce('spend__spend', 0), output_field=DecimalField(max_digits=10, decimal_places=2)),
            total_impressions=Coalesce(Sum('spend__impressions', output_field=IntegerField()), 0),
            total_clicks=Coalesce(Sum('spend__clicks', output_field=IntegerField()), 0),
            total_conversion=Coalesce(Sum('spend__conversion', output_field=IntegerField()), 0)
        ).order_by('date', 'name')
        return queryset


# SECOND It aggregates by the date not looking for the relations.
# class RevenueStatisticListView(generics.ListAPIView):
#     def get_queryset(self):
#         # Getting all unique dates and names from both RevenueStatistic and SpendStatistic
#         revenue_dates_names = RevenueStatistic.objects.all().values_list('date', 'name')
#         spend_dates_names = SpendStatistic.objects.all().values_list('date', 'name')
#
#         # Combining and de-duplicating dates and names
#         all_dates_names = set(chain(revenue_dates_names, spend_dates_names))
#         return all_dates_names
#
#     def list(self, request, *args, **kwargs):
#         all_dates_names = self.get_queryset()
#         result = []
#         for date, name in all_dates_names:
#             # Aggregating total revenue for the current date and name
#             total_revenue = RevenueStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('revenue', output_field=DecimalField(max_digits=9, decimal_places=2))
#             )['total'] or 0
#             # Aggregating total values from SpendStatistic for the current date and name
#             total_spend = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('spend', output_field=DecimalField(max_digits=10, decimal_places=2))
#             )['total'] or 0
#             total_impressions = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('impressions', output_field=IntegerField())
#             )['total'] or 0
#             total_clicks = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('clicks', output_field=IntegerField())
#             )['total'] or 0
#             total_conversion = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('conversion', output_field=IntegerField())
#             )['total'] or 0
#             # Appending aggregated data to the result list
#             result.append({
#                 'date': date,
#                 'name': name,
#                 'total_revenue': total_revenue,
#                 'total_spend': total_spend,
#                 'total_impressions': total_impressions,
#                 'total_clicks': total_clicks,
#                 'total_conversion': total_conversion
#             })
#         # Sorting result list by date and name
#         result = sorted(result, key=lambda x: (x['date'], x['name']))
#         return Response(result)
