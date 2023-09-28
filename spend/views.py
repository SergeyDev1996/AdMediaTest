from django.db.models import Sum, DecimalField, IntegerField, F
from itertools import chain

from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.response import Response
from .models import SpendStatistic
from revenue.models import RevenueStatistic
from .serializers import SpendStatisticSerializer


# FIRST It aggregates using the ForeignKey relation and aggregate the related values.
class SpendStatisticListView(generics.ListAPIView):
    serializer_class = SpendStatisticSerializer

    def get_queryset(self):
        # Perform a join on SpendStatistic and RevenueStatistic using the foreign key relationship.
        # Then, group by 'date' and 'name' and perform the aggregation on both tables.
        queryset = SpendStatistic.objects.values('date', 'name').annotate(
            total_spend=Sum(F('spend'), output_field=DecimalField(max_digits=10, decimal_places=2)),
            total_impressions=Coalesce(Sum('impressions', output_field=IntegerField()), 0),
            total_clicks=Coalesce(Sum('clicks', output_field=IntegerField()), 0),
            total_conversion=Coalesce(Sum('conversion', output_field=IntegerField()), 0),
            total_revenue=Coalesce(Sum('revenuestatistic__revenue', output_field=DecimalField(max_digits=9, decimal_places=2)), 0)
        ).order_by('date', 'name')
        return queryset

# class SpendStatisticListView(generics.ListAPIView):
#
#     def get_queryset(self):
#         # Getting all unique dates and names from both SpendStatistic and RevenueStatistic
#         spend_dates_names = SpendStatistic.objects.all().values_list('date', 'name')
#         revenue_dates_names = RevenueStatistic.objects.all().values_list('date', 'name')
#
#         # Combining and de-duplicating dates and names
#         all_dates_names = set(chain(spend_dates_names, revenue_dates_names))
#         return all_dates_names
#
#     def list(self, request, *args, **kwargs):
#         all_dates_names = self.get_queryset()
#         result = []
#
#         for date, name in all_dates_names:
#             # Aggregating total values from SpendStatistic for the current date and name
#             total_spend = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('spend', output_field=DecimalField(max_digits=10, decimal_places=2))
#             )['total'] or 0
#
#             total_impressions = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('impressions', output_field=IntegerField())
#             )['total'] or 0
#
#             total_clicks = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('clicks', output_field=IntegerField())
#             )['total'] or 0
#
#             total_conversion = SpendStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('conversion', output_field=IntegerField())
#             )['total'] or 0
#
#             # Aggregating total revenue for the current date and name
#             total_revenue = RevenueStatistic.objects.filter(date=date, name=name).aggregate(
#                 total=Sum('revenue', output_field=DecimalField(max_digits=9, decimal_places=2))
#             )['total'] or 0
#
#             # Appending aggregated data to the result list
#             result.append({
#                 'date': date,
#                 'name': name,
#                 'total_spend': total_spend,
#                 'total_impressions': total_impressions,
#                 'total_clicks': total_clicks,
#                 'total_conversion': total_conversion,
#                 'total_revenue': total_revenue
#             })
#
#         # Sorting result list by date and name
#         result = sorted(result, key=lambda x: (x['date'], x['name']))
#         return Response(result)
