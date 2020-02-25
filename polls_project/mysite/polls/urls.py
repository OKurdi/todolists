from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('todolists/', views.TodoListView, name='todolists'),
    path('createtodolist/', views.CreateTodoList, name='createtodolist'),
    path('entries/', views.EntriesView, name='entries'),
    path('createentry/', views.CreateEntry, name='createentry'),
    path('target/', views.TargetViewFunction, name='target'),
    path('addmember/', views.AddMember, name='addmember'),
    path('mytodolists/', views.ViewMyTodoLists, name='mytodolists'),
    path('sharedtodolists/', views.ViewSharedTodoLists, name='sharedtodolists'),
    path('profile/', views.ViewProfile, name='profile'),
    path('base/', views.logout_view, name='logout'),
    path('renamelist/', views.RenameListView, name='renamelist'),
    path('editprofile/', views.EditProfile, name='editprofile'),

]
