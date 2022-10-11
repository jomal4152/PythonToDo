from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView


# Create your views here.

# CLASS VIEWS

class TaskListView(ListView):
    model = Task
    template_name = 'todoapp/home.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todoapp/details.html'
    context_object_name = 'task'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'todoapp/update.html'
    context_object_name = 'task'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todoapp/delete.html'
    success_url = reverse_lazy('cbvhome')


# FUNCTION VIEWS

def home(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    if request.method == 'POST':
        name = request.POST.get('name', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task = Task(name=name, priority=priority, date=date)
        task.save()
    return render(request, 'todoapp/home.html', context)


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'todoapp/delete.html')


def update(request, taskid):
    task = Task.objects.get(id=taskid)
    print('task', task.id, task.name, task.priority)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'todoapp/update.html', {'form': form, 'task': task})
