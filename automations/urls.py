from django.urls import path
from . import views
urlpatterns = [path("follow-ups/", views.followup_list, name="followup_list")]
