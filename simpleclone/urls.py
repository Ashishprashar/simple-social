
from django.contrib import admin
from django.urls import path,include
from .  import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls'),name= 'accounts'),
    path('posts/',include('posts.urls'),name= 'posts'),
    path('groups/',include('groups.urls'),name= 'groups'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.HomePage.as_view(),name='home'),
    path('test/',views.TestPage.as_view(),name='test'),
    path('thanks/',views.ThanksPage.as_view(),name='thanks'),

]
