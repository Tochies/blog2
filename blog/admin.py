from django.contrib import admin
from .models import Post, Category, User, NewsLetter
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from mptt.admin import MPTTModelAdmin

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status','created', 'publish', 'author')
    prepopulated_fields = {'slug':('title', )}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
admin.site.register(Post, PostAdmin)



admin.site.register(Category, MPTTModelAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username']
admin.site.register(User, CustomUserAdmin)


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_added')
admin.site.register(NewsLetter, NewsLetterAdmin)



