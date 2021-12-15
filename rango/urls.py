from django.urls import path
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:slug_category_name>', views.show_category, name="show_category")
]