from django.contrib import admin
from .models import Blog, Blogcomment, BlogCommentReply

# Register your models here.

admin.site.register(Blog)
admin.site.register(Blogcomment)
admin.site.register(BlogCommentReply)


