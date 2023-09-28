from django.urls import path
from .views import RevenueStatisticListView

urlpatterns = [
    path('revenue-statistic/', RevenueStatisticListView.as_view(), name='revenue-statistic-view'),
]
