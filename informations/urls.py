from django.urls import path
from . import views

app_name = "info"
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:company_pk>/detail/', views.detail, name="detail"),
    path('gongos/', views.gongos, name="gongos"),
    path('gongos/<int:gongo_pk>/', views.gongo_detail, name="gongo_detail"),
    path('<int:gongo_pk>/bookmark/', views.bookmark, name="bookmark"),
]
