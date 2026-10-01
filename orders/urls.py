from django.urls import path

from .views import (
    OrderCreateView,
    MyOrdersView,
    OrderDeleteView,
)


urlpatterns = [
    path('', OrderCreateView.as_view()),
    path('my/', MyOrdersView.as_view()),
    path('<int:pk>/', OrderDeleteView.as_view()),
]
