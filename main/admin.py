from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Gallery)
admin.site.register(Action)
admin.site.register(Request_Table)
admin.site.register(Transctions)