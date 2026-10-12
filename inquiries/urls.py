from django.urls import path
from . import views
urlpatterns = [
    path("new/", views.public_inquiry, name="public_inquiry"),
    path("manage/", views.inquiry_list, name="inquiry_list"),
    path("manage/new/", views.inquiry_create, name="inquiry_create"),
    path("manage/<int:pk>/", views.inquiry_detail, name="inquiry_detail"),
    path("approvals/<int:approval_id>/send/", views.approve_email, name="approve_email"),
]
