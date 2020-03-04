import django
from django.contrib.auth.models import User
from django.db import models


class User(models.Model):
    auth_user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE,
                                  related_name='auth_user_id', null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    age = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    bio = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.full_name


class Entry(models.Model):
    entry_titel = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=200, blank=True)
    isdone = models.CharField(max_length=50, default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class TodoList(models.Model):
    name = models.CharField(max_length=15)
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='list_user', default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    def get_user(self):
        return self.user

class TodoListWithEntris(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)


class SharedListsWithUsers(models.Model):
    owner = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='owner')
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='user')

    def get_todolist(self):
        return self.todo_list

    def get_owner(self):
        return self.owner

    def get_user(self):
        return self.user
