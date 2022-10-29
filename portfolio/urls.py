# portfolio/urls.py

# Django
from django.urls import path

# local
from . import views

app_name = "portfolio"

urlpatterns = [
  # Portfolio
  path('portfolio/home/'  , views.home_portfolio, name="home-portfolio"), # portfolio static
  path('portfolio/index/'               , views.IndexView.as_view(), name="index-portfolio"), 
	path('portfolio/contact/'             , views.ContactView.as_view(), name="contact"),
	path('portfolio/portfolios/'          , views.PortfolioView.as_view(), name="portfolios"),
	path('portfolio/portfolio/<slug:slug>', views.PortfolioDetailView.as_view(), name="portfolio-detail"),
	path('portfolio/blog/'                , views.BlogView.as_view(), name="blogs"),
	path('portfolio/blog/<slug:slug>'     , views.BlogDetailView.as_view(), name="blog-detail"),
  # Meteo
  path('meteo/'       , views.index_meteo, name="index-meteo"),
  path('meteo/getij/' , views.getij, name="getij"),
  path('meteo/weer/'  , views.weer, name="weer"),
]

