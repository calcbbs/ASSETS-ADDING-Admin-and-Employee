from django.contrib import admin
from .models import Login_Table,Assets_Table,Assets_Employee_Table,Employee_Table

# Register your models here.
admin.site.register(Login_Table)
admin.site.register(Assets_Table)
admin.site.register(Assets_Employee_Table)
admin.site.register(Employee_Table)
