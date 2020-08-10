from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('categories/', views.update, name="update"),
    path('categories/<int:id>/', views.compose_get_by_id_response, name="get_by_id_response"),
]