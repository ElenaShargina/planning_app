from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Plan, Task, FlashCardCollection, FlashCard
from .forms import PlanForm, TaskForm, FlashCardCollectionForm, FlashCardForm
from django.db.models import Count, Q


@login_required
def plan_list(request):
    plans = (
        Plan.objects.filter(user=request.user)
        .annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count('tasks', filter=Q(tasks__status='completed')),
            pending_tasks=Count(
                'tasks', filter=Q(tasks__status__in=['pending', 'in_progress'])
            ),
        )
        .order_by('-id')
    )
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

    return render(
        request, 'tasks/plan_detail.html', {'plan': plan, 'tasks': tasks, 'form': form}
    )


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


@login_required
def collection_list(request):
    collections = FlashCardCollection.objects.filter(user=request.user).order_by('-id')
    return render(request, 'tasks/collection_list.html', {'collections': collections})


@login_required
def collection_create(request):
    if request.method == 'POST':
        form = FlashCardCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return redirect('collection_list')
    else:
        form = FlashCardCollectionForm()
    return render(request, 'tasks/collection_create.html', {'form': form})


@login_required
def collection_detail(request, collection_id):
    collection = get_object_or_404(
        FlashCardCollection, id=collection_id, user=request.user
    )
    cards = collection.cards.all().order_by('-id')

    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.collection = collection
            card.save()
            return redirect('collection_detail', collection_id=collection.id)
    else:
        form = FlashCardForm()

    return render(
        request,
        'tasks/collection_detail.html',
        {'collection': collection, 'cards': cards, 'form': form},
    )


from .models import Timer
from .forms import TimerForm


@login_required
def timer_list(request):
    timers = Timer.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = TimerForm(request.POST)
        if form.is_valid():
            timer = form.save(commit=False)
            timer.user = request.user
            timer.save()
            return redirect('timer_list')
    else:
        form = TimerForm()

    return render(request, 'tasks/timer_list.html', {'timers': timers, 'form': form})


@login_required
def timer_stop(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, user=request.user)
    if timer.is_running:
        timer.completed_at = timezone.now()
        timer.save()
    return redirect('timer_list')
