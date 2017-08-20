from django.contrib import admin
from home.models import Post, Friend, Retweets
# Register your models here.

admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(Retweets)
