from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import stockModel
from .serializers import StockSerializer


class StockListCreateView(APIView):

  def get(self, request):

    try:

      page = int(request.GET.get('page', 1))
      limit = int(request.GET.get('limit', 50))
      search = request.GET.get('search', '')

# ! search functionality
      stocks = stockModel.objects.all()
      if search:
        stocks = stocks.filter(
          Q(trade_code__icontains=search) |
          Q(date__icontains = search)
        )

#  ! pagination functionality
      paginator = Paginator(stocks, limit)
      try:
        stocks = paginator.page(page)
      except PageNotAnInteger:
        stocks = paginator.page(1)
      except EmptyPage:
        stocks = paginator.page(paginator.num_pages)

      serializer = StockSerializer(stocks, many=True)
      return Response({
        'success': True,
        'data': serializer.data,
        'total': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': stocks.number
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'success': False,
        'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def post(self, request):
    try:
      serializer = StockSerializer(data=request.data)
      if serializer.is_valid():
        stock = serializer.save()
        return Response({
          'success': True,
          'data': StockSerializer(stock).data
        }, status=status.HTTP_201_CREATED)
      else:
        return Response({
          'success': False,
          'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({
        'success': False,
        'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockDetailView(APIView):
  def get_stock(self, stock_id):
    try:
      return stockModel.objects.get(id=stock_id)
    except stockModel.DoesNotExist as e:
      return None

  def get(self, request, stock_id):
    try:
      stock = self.get_stock(stock_id)
      if not stock:
        return Response({
          'success': False,
          'error': 'Stock not found'
        }, status=status.HTTP_404_NOT_FOUND)

      return Response({
        'success': True,
        'data': StockSerializer(stock).data
      }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
        'success': False,
        'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def put(self, request, stock_id):
    try:
      stock = self.get_stock(stock_id)
      if not stock:
        return Response({
          'success': False,
          'error': 'Stock not found'
        }, status=status.HTTP_404_NOT_FOUND)

      serializer = StockSerializer(stock, data=request.data)
      if serializer.is_valid():
        stock = serializer.save()
        return Response({
          'success': True,
          'data': StockSerializer(stock).data
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          'success': False,
          'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
      return Response({
        'success': False,
        'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def delete(self, request, stock_id):
    try:
      stock = self.get_stock(stock_id)
      if not stock:
        return Response({
          'success': False,
          'error': 'Stock not found'
        }, status=status.HTTP_404_NOT_FOUND)

      stock.delete()
      return Response({
        'success': True,
        'message': 'Stock deleted successfully'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'success': False,
        'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
