# stocks/views.py

# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

# Local
from .forms  import  StockForm
from .models import Stock

# Python packages
import os

# Stockvalues view
def stockvalues(request):
  import requests
  import json

  title = 'Aandeelkoersen'
  iexcloud_apikey = os.getenv('IEXCLOUD_APIKEY')

  tickers = Stock.objects.all()
  output = []
  for ticker_item in tickers:
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) + "/quote?token=" + iexcloud_apikey)
    try:
      api_result_table = json.loads(api_request.content)
      output.append(api_result_table)
    except Exception as e:
      api_result = "Error..."  

  if request.method == "POST":
    ticker_name        = request.POST['ticker_name']
    ticker_description = request.POST['ticker_description']
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker_name + "/quote?token=" + iexcloud_apikey)
    try:
      api_result = json.loads(api_request.content)
    except Exception as e:
      api_result = "Error..."
    
    add_stock_form = StockForm(request.POST or None)

    if add_stock_form.is_valid():
      add_stock_form.save()
      messages.success(request, ("Aandeel " + ticker_name + " ; " + ticker_description + " is aan de tabel toegevoegd"))
      return redirect('stockvalues')
    else:
      messages.success(request, ("Error in form ..."))

    # render page after POST
    return render(request, 'stocks/stockvalues.html', {'api_result': api_result, 'output': output, 'title': title})
  else:
    # render page after GET
    return render(request, 'stocks/stockvalues.html', {'output': output, 'title': title})

# all stocks view
def all_stocks(request):
  title     = 'Aandelen'
  tickers   = Stock.objects.all().order_by('ticker_name')
  ticker_count = tickers.count()
  
  if request.method == "POST":
    ticker_name        = request.POST['ticker_name']
    ticker_description = request.POST['ticker_description']
    add_stock_form     = StockForm(request.POST or None)
    # process formulier
    if add_stock_form.is_valid():
      add_stock_form.save()
      messages.success(request, ("Aandeel " + ticker_name + " ; " + ticker_description + " is aan de tabel toegevoegd"))
      return redirect('all_stocks')
    else:
      messages.success(request, ("Error in formulier ..."))

  paginator    = Paginator(tickers, 2) # Show 2 stocks per page.
  page_number  = request.GET.get('page')
  page_obj     = paginator.get_page(page_number)
  page_count   = "a" * page_obj.paginator.num_pages
  is_paginated = page_obj.has_other_pages
  context = {
    'title'        : title,
    'aantal'       : ticker_count,
    'page_obj'     : page_obj,
    'is_paginated' : is_paginated,
    'page_count'   : page_count
  }
  return render(request, 'stocks/all_stocks.html', context)
  
# edit stock view
def edit_stock(request, stock_id):
  if request.method == 'POST':
    item = Stock.objects.get(pk=stock_id)
    form = StockForm(request.POST or None, instance=item)
    if form.is_valid():
      form.save()
      messages.success(request, ('Item updated'))
      return redirect('all_stocks')
  else:
    item = Stock.objects.get(pk=stock_id)
    return render(request, 'stocks/edit_stock.html', {'item': item})

# delete stock view
def delete_stock(request, stock_id):
  item = Stock.objects.get(pk=stock_id)
  ticker_name   = item.ticker_name
  ticker_description = item.ticker_description
  item.delete()
  messages.success(request, ("Aandeel " + ticker_name + " ; " + ticker_description + " has been deleted!"))
  return redirect(all_stocks)
