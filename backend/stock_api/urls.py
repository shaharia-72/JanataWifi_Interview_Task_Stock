from django.urls import path

from .views import StockDetailView, StockListCreateView


urlpatterns = [
    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('stocks/<int:stock_id>/', StockDetailView.as_view(), name='stock-detail'),
]
