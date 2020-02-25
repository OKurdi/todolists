import django
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from .forms import RegisterForm
from .models import User, TodoList, Entry, TodoListWithEntris, SharedListsWithUsers, UserWithTodoLists
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def signup_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        register_form.email = request.POST['email']
        register_form.full_name = request.POST['full_name']
        new_user = User()
        new_user.full_name = request.POST['full_name']
        new_user.email = request.POST['email']
        new_user.age = request.POST['age']
        new_user.phone = request.POST['phone']
        # new_user.password = register_form.cleaned_data['password1']
        new_user.bio = request.POST['bio']
        if register_form.is_valid():
            auth_user = register_form.save()
            new_user.auth_user = auth_user
            new_user.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=register_form.cleaned_data['username'],
                                    password=register_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect("/polls/todolists")
            # return redirect('polls:login')
    elif request.method == 'GET':
        register_form = RegisterForm()
    return render(request, 'polls/signup.html', {'form': register_form})


def login_view(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password', '')
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            print('line41:// This line has been reached after login ')
            user_todo_lists = CombineUserAndSharedLists(request.user.id)
            return HttpResponseRedirect("/polls/todolists")

            # return render(request, 'polls/todolists.html', {'todo_lists': user_todo_lists}, )
        except:
            return render(request, 'polls/login.html')
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'polls/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('polls:login')


def TodoListView(request):
    if request.method == 'GET':
        # return redirect('polls/todolists.html')
        if len(CombineUserAndSharedLists(request.user.id)) == 0:
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'warningmessage': "You don't have any todo lists!"}, )
        else:
            return render(request, 'polls/todolists.html',
                          {'todo_lists': CombineUserAndSharedLists(request.user.id), }, )
    elif request.method == 'POST':
        # check whether the user is permited to delete the list(checking if the user_id in the list table is the same as the current user_id):
        if UserWithTodoLists.objects.get(todo_list_id=request.POST.get('list_id')).user_id == request.user.id:
            UserWithTodoLists.objects.filter(todo_list_id=request.POST['list_id']).delete()
            TodoList.objects.filter(id=request.POST['list_id']).delete()
            mapping_todo_list_with_entries = TodoListWithEntris.objects.filter(todo_list_id=request.POST.get('list_id'))
            entries_id = []
            for mapping_todo_list_with_entry in mapping_todo_list_with_entries:
                entries_id.append(mapping_todo_list_with_entry.entry_id)
            Entry.objects.filter(id__in=entries_id).delete()
            TodoListWithEntris.objects.filter(todo_list_id=request.POST.get('list_id')).delete()
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'message': "list has been successfuly deleted."}, )
        else:
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'warningmessage': "You are not allowed to delete this list, as you are not the owner of it! please contact your adminstrator for more details!"}, )


def ViewMyTodoLists(request):
    if request.method == 'GET':
        my_lists = FilterUserTodoLists(request.user.id)
        if my_lists.count() == 0:
            return render(request, 'polls/mytodolists.html', {'warningmessage': "You don't have lists!"}, )
        else:
            return render(request, 'polls/mytodolists.html',
                          {'todo_lists': my_lists, 'message': "Here is your lists:"}, )
    elif request.method == 'POST':
        UserWithTodoLists.objects.filter(todo_list_id=request.POST['list_id']).delete()
        TodoList.objects.filter(id=request.POST['list_id']).delete()
        mapping_todo_list_with_entries = TodoListWithEntris.objects.filter(todo_list_id=request.POST.get('list_id'))
        entries_id = []
        for mapping_todo_list_with_entry in mapping_todo_list_with_entries:
            entries_id.append(mapping_todo_list_with_entry.entry_id)
        Entry.objects.filter(id__in=entries_id).delete()
        TodoListWithEntris.objects.filter(todo_list_id=request.POST.get('list_id')).delete()
        return render(request, 'polls/mytodolists.html', {'todo_lists': FilterUserTodoLists(request.user.id),
                                                          'message': "list has been successfuly deleted."}, )


def ViewSharedTodoLists(request):
    if request.method == 'GET':
        # I want to get the object of the SharedListsWithUsers, so that I can mapp it with the user and owner details in the html page.
        # so here I am not using the TodoLists objects. Thus, I getting the object it self and managing the joining functionality depending
        # on the objects functionality in the model.
        # SharedTodoLists = FilterSharedTodoLists(user_id)
        shared_lists = SharedListsWithUsers.objects.filter(user_id=request.user.id)
        if shared_lists.count() == 0:
            return render(request, 'polls/sharedtodolists.html',
                          {'warningmessage': "You don't have any shared lists!"}, )
        else:
            return render(request, 'polls/sharedtodolists.html',
                          {'todo_lists': shared_lists, 'message': "Here is your shared lists:"}, )


def CreateTodoList(request):
    if request.method == 'POST':
        if UserWithTodoLists.objects.filter(user_id=request.user.id).count() <= 9:
            user_with_todo_lists = UserWithTodoLists.objects.filter(user_id=request.user.id)
            todo_lists_id = []
            for x in user_with_todo_lists:
                todo_lists_id.append(x.todo_list_id)
            todo_lists = TodoList.objects.filter(id__in=todo_lists_id)
            is_list_name_exist = False
            for list in todo_lists:
                if list.name == request.POST.get('listName'):
                    is_list_name_exist = True
            if not is_list_name_exist:
                new_todo_list = TodoList()
                new_todo_list.name = request.POST.get('listName')
                new_todo_list.save()
                HandelCreationOfNewList(request, new_todo_list)
                # 'todo_lists': CombineUserAndSharedLists(request.user.id),
                # return HttpResponseRedirect("/polls/todolists", message='List has been created successfuly!')
                if request.POST.get('pagename') == 'mytodolists':
                    print('reached mytodolists create a new list')
                    return redirect('http://127.0.0.1:8000/polls/mytodolists', message='List has been created successfuly!')
                elif request.POST.get('pagename') == 'todolists':
                    return redirect('http://127.0.0.1:8000/polls/todolists', message='List has been created successfuly!')
                '''return render(request, 'polls/todolists.html',
                              {'todo_lists': CombineUserAndSharedLists(request.user.id),
                               'message': 'List has been created successfuly!'}, )
                '''
                # return redirect('polls:todolists')
            else:
                return render(request, 'polls/createtodolist.html', {
                    'warningmessage': 'List Name is already exist, please choose different name or delete duplicated list!'}, )
        else:
            return render(request, 'polls/todolists.html',
                          {'todo_lists': CombineUserAndSharedLists(request.user.id),
                           'warningmessage': "number of lists is 10, please remove unnecessary lists and try again."}, )
            # return redirect('polls:todolists')
    elif request.method == 'GET':
        return render(request, 'polls/createtodolist.html', {'pagename': request.GET.get('pagename')})


def HandelCreationOfNewList(request, NewTodoList):
    newUserWithTodoList = UserWithTodoLists()
    newUserWithTodoList.user = request.user
    newUserWithTodoList.todo_list = NewTodoList
    newUserWithTodoList.save()


def RenameListView(request):
    if request.method == 'POST':
        if UserWithTodoLists.objects.get(todo_list_id=request.POST['list_id']).user_id == request.user.id:
            list_id = request.POST.get('list_id')
            todo_list = TodoList.objects.get(id=list_id)
            todo_list.name = request.POST.get('list_name')
            todo_list.save()
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'message': "List has been successfully renamed !."}, )
        else:
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'message': "You don't have permission to rename this list!"}, )

    elif request.method == 'GET':
        return render(request, 'polls/renamelist.html', {'list_id': request.GET.get('list_id'),
                                                         'list_name': TodoList.objects.get(
                                                             id=request.GET.get('list_id')), }, )


def CreateEntry(request):
    if request.method == 'POST':
        if TodoListWithEntris.objects.filter(todo_list_id=request.POST.get('list_id')).count() <= 99:
            new_entry = Entry()
            new_entry.entry_titel = request.POST.get('task')
            new_entry.description = request.POST.get('description')
            new_entry.save()
            HandelCreationOfNewEntry(request, new_entry)
            return ReturnEntriesViewResponse(request, FilterEntries(request.POST.get('list_id')),
                                             request.POST.get('list_id'))
        else:
            return ReturnEntriesViewResponse(request, FilterEntries(request.POST.get('list_id')),
                                             request.POST.get('list_id'))
    elif request.method == 'GET':
        return render(request, 'polls/createentry.html', {'list_id': request.GET.get('list_id')}, )


def HandelCreationOfNewEntry(request, new_entry):
    todo_list_with_entry = TodoListWithEntris()
    todo_list_with_entry.todo_list_id = request.POST.get('list_id')
    todo_list_with_entry.entry_id = new_entry.id
    todo_list_with_entry.save()


def CombineUserAndSharedLists(user_id):
    user_lists = FilterUserTodoLists(user_id)
    shared_lists = FilterSharedTodoLists(user_id)
    combined_lists = []
    for user_list in user_lists:
        combined_lists.append(user_list)
    for shared_list in shared_lists:
        combined_lists.append(shared_list)
    return combined_lists


# this function returns the todo_lists created by the user him/her-self
def FilterUserTodoLists(user_id):
    mapping_user_with_todo_lists = UserWithTodoLists.objects.filter(user_id=user_id)
    todo_lists_id = []
    for mapping_user_with_todo_list in mapping_user_with_todo_lists:
        todo_lists_id.append(mapping_user_with_todo_list.todo_list_id)
    user_todo_lists = TodoList.objects.filter(id__in=todo_lists_id)
    return user_todo_lists


def FilterSharedTodoLists(user_id):
    mapping_shared_todo_lists = SharedListsWithUsers.objects.filter(user_id=user_id)
    todo_lists_id = []
    for mapping_shared_todo_list in mapping_shared_todo_lists:
        todo_lists_id.append(mapping_shared_todo_list.todo_list_id)
    shared_todo_lists = TodoList.objects.filter(id__in=todo_lists_id)
    return shared_todo_lists


def EntriesView(request):
    if request.method == 'GET':
        if request.GET.get('list_id') != None:
            return ReturnEntriesViewResponse(request, FilterEntries(request.GET.get('list_id')),
                                             request.GET.get('list_id'))
        else:
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'warningmessage': 'Please select a List to view the tasks!'}, )
    elif request.method == 'POST':
        # delete_entry:
        TodoListWithEntris.objects.filter(entry_id=request.POST.get('entry')).delete()
        Entry.objects.filter(id=request.POST.get('entry')).delete()
        return ReturnEntriesViewResponse(request, FilterEntries(request.POST['list_id']), request.POST.get('list_id'))
    elif request.method == 'PUT':
        checked_entry = Entry.objects.get(id=request.PUT['entry'])
        checked_entry.selected = True
        checked_entry.save()


def FilterEntries(list_id):
    entries_id = []
    for mapping_todo_lists_with_entrie in TodoListWithEntris.objects.filter(todo_list_id=list_id):
        entries_id.append(mapping_todo_lists_with_entrie.entry_id)
    return Entry.objects.filter(id__in=entries_id)


def ReturnEntriesViewResponse(request, entries, list_id):
    if entries.count() == 0:
        return render(request, 'polls/entries.html',
                      {'entries': entries, 'list_id': list_id,
                       'warningmessage': "You don't have tasks in this list!", }, )
    else:
        return render(request, 'polls/entries.html',
                      {'entries': entries, 'list_id': list_id, 'message': "Here is your tasks:"}, )


def AddMember(request):
    if request.method == 'GET':
        return render(request, 'polls/addmember.html',
                      {'users_list': django.contrib.auth.models.User.objects.exclude(id=request.user.id).exclude(
                          id=UserWithTodoLists.objects.get(todo_list_id=request.GET.get('list_id')).user_id),
                          'list_id': request.GET.get('list_id')}, )
    elif request.method == 'POST':
        if UserWithTodoLists.objects.get(todo_list_id=request.POST['list_id']).user_id == request.user.id:
            is_permited = SharedListsWithUsers.objects.filter(user_id=request.POST.get('user_id')).filter(
                todo_list_id=request.POST.get('list_id')).count() == 0
            if is_permited:
                new_shared_lists_with_users = SharedListsWithUsers()
                new_shared_lists_with_users.user = django.contrib.auth.models.User.objects.get(
                    id=request.POST.get('user_id'))
                new_shared_lists_with_users.owner = request.user
                new_shared_lists_with_users.todo_list = TodoList.objects.get(id=request.POST.get('list_id'))
                new_shared_lists_with_users.save()
                return render(request, 'polls/todolists.html',
                              {'todo_lists': CombineUserAndSharedLists(request.user.id),
                               'message': 'the member can view the list now.', }, )
            else:
                return render(request, 'polls/todolists.html',
                              {'todo_lists': CombineUserAndSharedLists(request.user.id),
                               'message': 'the member is already has permission to view this list.', }, )
        else:
            return render(request, 'polls/todolists.html', {'todo_lists': CombineUserAndSharedLists(request.user.id),
                                                            'message': "You can't add a member to this list, as you are not the owner of it.", }, )


def ViewProfile(request):
    if request.method == 'GET':
        return render(request, 'polls/profile.html',
                      {'pollsuserinfo': User.objects.get(auth_user_id=request.user.id),
                       'authuserinfo': request.user, }, )
    elif request.method == 'POST':
        return render(request, 'polls/profile.html')


def EditProfile(request):
    if request.method == 'GET':
        return render(request, 'polls/editprofile.html',
                      {'pollsuserinfo': User.objects.get(auth_user_id=request.user.id),
                       'authuserinfo': request.user, }, )
    elif request.method == 'POST':
        polls_user = User.objects.get(auth_user_id=request.user.id)
        auth_user = request.user
        polls_user.full_name = request.POST.get('full_name')
        polls_user.email = request.POST.get('email')
        polls_user.age = request.POST.get('age')
        polls_user.phone = request.POST.get('phone')
        polls_user.bio = request.POST.get('bio')
        auth_user.username = request.POST.get('username')
        auth_user.password = request.POST.get('password')
        auth_user.email = request.POST.get('email')
        polls_user.save()
        auth_user.save()
        return render(request, 'polls/profile.html',
                      {'pollsuserinfo': User.objects.get(auth_user_id=request.user.id),
                       'authuserinfo': request.user, }, )


def TargetViewFunction(request):
    return render(request, 'polls/target.html')


def IndexView(request):
    if request.method == 'GET':
        return render(request, 'polls/index.html')
