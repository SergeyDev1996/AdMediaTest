from django.urls import path
from .views import SpendStatisticListView

urlpatterns = [
    path('spend-statistic/', SpendStatisticListView.as_view(), name='spend-statistic-view'),
]
