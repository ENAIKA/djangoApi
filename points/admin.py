from django.contrib import admin
from .models import Project,UserProfile,Rates,NewsLetterRecipients
# Register your models here.

admin.site.register(Project)
admin.site.register(UserProfile)
admin.site.register(Rates)
admin.site.register(NewsLetterRecipients)
