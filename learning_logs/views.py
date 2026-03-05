from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.contrib import messages 
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# --- CORE VIEWS ---

def index(request):
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show topics."""
    if request.user.is_authenticated:
        user_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
        public_topics = Topic.objects.filter(public=True).exclude(owner=request.user).order_by('date_added')
    else:
        user_topics = []
        public_topics = Topic.objects.filter(public=True).order_by('date_added')

    context = {'topics': user_topics, 'public_topics': public_topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and its entries."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Make sure the topic is public OR owned by the user
    if not topic.public:
        if not request.user.is_authenticated or topic.owner != request.user:
            raise Http404

    # Check if the logged-in user is the owner
    is_owner = request.user.is_authenticated and topic.owner == request.user

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'is_owner': is_owner}
    return render(request, 'learning_logs/topic.html', context)

def entry(request, entry_id):
    """Show a single entry (Full Text)."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Security check
    if not topic.public:
        if not request.user.is_authenticated or topic.owner != request.user:
            raise Http404

    is_owner = request.user.is_authenticated and topic.owner == request.user
    context = {'entry': entry, 'topic': topic, 'is_owner': is_owner}
    return render(request, 'learning_logs/entry.html', context)

# --- FORM VIEWS (Add/Edit) ---

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        return HttpResponseForbidden()

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return HttpResponseForbidden()

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:entry', entry_id=entry.id) # Redirect to the full entry view

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

# --- DELETE VIEWS ---

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        return redirect('learning_logs:topics')
    
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic_confirm.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return redirect('learning_logs:topic', topic_id=topic.id)

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry_confirm.html', context)

# --- FIX SITE TOOL ---
def fix_site(request):
    return HttpResponse("Fix site tool removed for security.")