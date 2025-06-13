from django.urls import path
from . import views
app_name = 'plan'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/plans/', views.PlanListCreateView.as_view(), name='list-create'),
    path('api/plans/<int:id>/', views.PlanUpdateDeleteView.as_view(), name='update-delete'),
]