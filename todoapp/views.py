from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.
class TodoListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'


class TodoDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'


class TodoUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail', kwargs={'pk': self.object.id})


class TodoDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')


def add(request):
    if request.user.is_authenticated:
        current_user = request.user
        tasks = Task.objects.all().filter(created_by=current_user.id)
    else:
        tasks = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        created_by = current_user.id
        task = Task(name=name, priority=priority, date=date, created_by=created_by)
        task.save()
    return render(request, 'home.html', {'tasks': tasks})


def delete(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        task.delete()
        return redirect('/todo/')


def update(request, id):
    task = Task.objects.get(id=id)
    current_user = request.user
    if request.method == 'POST':
        task.name = request.POST.get('task', '')
        task.priority = request.POST.get('priority', '')
        task.date = request.POST.get('date', '')
        task.created_by = current_user.id
        task.save()
        return redirect('/todo/')
    return render(request, 'edit.html', {'task': task})
