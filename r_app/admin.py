from django.contrib import admin

# Register your models here.
from .models import Users, Role, Action, RoleActionMapping, API,ApiUserMapping


admin.site.register(Users)
admin.site.register(Role)
admin.site.register(Action)
admin.site.register(RoleActionMapping)
admin.site.register(API)
admin.site.register(ApiUserMapping)