from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import AddTaskForm1, AddTaskForm2, EditTaskForm
from .models import Task
from scholarships.views import scholarships_table


@login_required
def tasks(request):
    '''Show all tasks'''
    tasks = Task.objects.filter(owner=request.user)
    context = {
        'tasks': tasks,
        }

    return render(request, 'tasks/tasks.html', context)


@login_required
def add_task1a(request):
    if request.method != 'POST':
        form = AddTaskForm1()
    else:
        form = AddTaskForm1(data=request.POST)
        if form.is_valid():
            add_task = form.save(commit=False)
            add_task.owner = request.user
            add_task.save()
            return redirect('tasks:add_task1b')

    tasks = Task.objects.all()
    tooltip = "You can choose a fixed amount to retain a minimum value, e.g, inputting 45 ensures to you a minimum amount of 45 SLP's.(only for this field)"

    context = {
        'form': form, 
        'tasks': tasks,
        'tooltip': tooltip,
        }
    
    return render(request, 'tasks/add_task1a.html', context)

@login_required
def add_task1b(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:add_task12a')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task1b.html', context)


@login_required
def add_task12a(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:add_task12b')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task12a.html', context)


@login_required
def add_task12b(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:add_task123a')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task12b.html', context)


@login_required
def add_task123a(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:add_task123b')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task123a.html', context)


@login_required
def add_task123b(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:add_task1234a')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task123b.html', context)


@login_required
def add_task1234a(request):
    task = Task.objects.filter(owner=request.user).last()
    name = Task.objects.get(id=task.id)
    
    if request.method != 'POST':
        form = AddTaskForm2(instance=name)
    else:
        form = AddTaskForm2(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/add_task1234a.html', context)


@login_required
def edit_task(request, name_id):
    name = Task.objects.get(id=name_id)

    if request.method != 'POST':
        form = EditTaskForm(instance=name)
    else:
        form = EditTaskForm(instance=name, data=request.POST)
        if form.is_valid():
            form.save()
            scholarships_table(request)
            return redirect('tasks:tasks')

    context = {'name': name, 'form': form}

    return render(request, 'tasks/edit_task.html', context)


@login_required
def remove_task(request, task_id):
    task = Task.objects.filter(owner=request.user).get(id=task_id)

    if request.method=='POST':
        task.delete()

        return HttpResponseRedirect('/tasks')
    
    context = {'task': task}

    return render(request, 'tasks/remove_task.html', context)


@login_required
def help_task(request):

    return render(request, 'tasks/help_task.html')



