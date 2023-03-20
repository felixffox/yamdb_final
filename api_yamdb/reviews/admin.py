from django.contrib import admin

# Register your models here.
from .models import Category, Comment, Genre, GenreTitle, Review, Title

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
