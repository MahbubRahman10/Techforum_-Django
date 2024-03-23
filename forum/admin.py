from django.contrib import admin

# Register your models here.

from .models import Category, forum, Reply, Userlike

admin.site.register(Category)
admin.site.register(forum)
admin.site.register(Reply)
admin.site.register(Userlike)