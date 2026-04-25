from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Plan, Task
from .forms import PlanForm, TaskForm

@login_required
def plan_list(request):
    plans = Plan.objects.filter(user=request.user).order_by('-id')
    return render(request, 'tasks/plan_list.html', {'plans': plans})

@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('plan_list')
    else:
        form = PlanForm()
    return render(request, 'tasks/create_plan.html', {'form': form})

@login_required
def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    tasks = plan.tasks.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.plan = plan
            if task.status == 'completed' and not task.completed_at:
                task.completed_at = timezone.now()
            elif task.status != 'completed':
                task.completed_at = None
            task.save()
            return redirect('plan_detail', plan_id=plan.id)
    else:
        form = TaskForm()
        
    return render(request, 'tasks/plan_detail.html', {'plan': plan, 'tasks': tasks, 'form': form})

@login_required
def task_toggle_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, plan__user=request.user)
    if task.status == 'completed':
        task.status = 'pending'
        task.completed_at = None
    else:
        task.status = 'completed'
        task.completed_at = timezone.now()
    task.save()
    return redirect('plan_detail', plan_id=task.plan.id)