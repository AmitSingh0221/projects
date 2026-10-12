from django.contrib import admin
from .models import EmailApproval, FollowUp, ActivityLog
admin.site.register(EmailApproval)
admin.site.register(FollowUp)
admin.site.register(ActivityLog)
