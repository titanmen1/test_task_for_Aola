from django.urls import path

from app import views

urlpatterns = [
    path("person_feed/<int:user_id>", views.PersonFeedAPIView.as_view(), name='person_feed'),
]
