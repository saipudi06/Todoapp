from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('register', views.register, name='register'),
    path('login_req', views.login_req, name='login_req'),
    path("logout", views.logout_request, name= "logout"),
    path('index', views.index, name='index'),
    path('add', views.add, name='add'),
    path('submit', views.submit, name='submit'),
    path('delete<int:id>', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path('sort', views.sort, name='sort'),
    path('sortdata', views.sortdata, name='sortdata'),
    path('edit<int:id>', views.edit, name='edit'),
    path('update<int:id>', views.update, name='update'),
    path('completed<int:id>', views.completed, name='completed'),
    path('done', views.done, name='done'),
    path("password_reset", views.password_reset_request, name="password_reset")
    # path('home', views.home, name='home'),

]
