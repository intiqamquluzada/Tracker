from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Avg, Max, Min
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.tracking.models import PriceHistory

@api_view(['GET'])
def stock_performance(request, symbol, start_date, end_date):
    data = PriceHistory.objects.filter(stock__symbol=symbol, date__range=[start_date, end_date])
    avg_price = data.aggregate(Avg('price'))
    max_price = data.aggregate(Max('price'))
    min_price = data.aggregate(Min('price'))
    return Response({"avg_price": avg_price, "max_price": max_price, "min_price": min_price})
