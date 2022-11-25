from django.contrib import admin
from .models import Tour, Types, Entry, Comment, Category, Like

admin.site.register(Tour)
admin.site.register(Types)
admin.site.register(Entry)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Like)
