from . import views
from django.urls import path

app_name = 'saiten'

urlpatterns = [
    path('',views.TestView.as_view(),name='post_saiten'),
    path('saiten/',views.ajax_saiten,name='ajax_saiten')
]