from django.contrib import admin

from example_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["lastUpdated", "text"]
