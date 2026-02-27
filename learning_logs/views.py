# learning_logs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    if request.user.is_authenticated:
        user_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
        public_topics_others = (Topic.objects
            .filter(public=True)
            .exclude(owner=request.user)
            .order_by('date_added'))
    else:
        user_topics = None
        public_topics_others = Topic.objects.filter(public=True).order_by('date_added')

    context = {'topics': user_topics, 'public_topics': public_topics_others}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic_obj = get_object_or_404(Topic, id=topic_id)

    if not topic_obj.public and (not request.user.is_authenticated or topic_obj.owner != request.user):
        raise Http404

    is_owner = request.user.is_authenticated and (request.user == topic_obj.owner)
    
    # Truncate entry text to 50 chars in the view
    entries_raw = topic_obj.entry_set.order_by('-date_added')
    entries = []
    for entry in entries_raw:
        entry.preview = entry.text[:50] + '...' if len(entry.text) > 50 else entry.text
        entries.append(entry)

    context = {'topic': topic_obj, 'entries': entries, 'is_owner': is_owner}
    return render(request, 'learning_logs/topic.html', context)

def check_strict_topic_owner(topic_obj, user):
    if topic_obj.owner != user:
        return HttpResponseForbidden("You do not have permission to modify this topic or its entries.")
    return None

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic_obj = form.save(commit=False)
            new_topic_obj.owner = request.user
            new_topic_obj.save()
            messages.success(request, "Topic added successfully!")
            return redirect('learning_logs:topics')
        else:
            messages.error(request, "Please correct the errors below.")
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic_obj = get_object_or_404(Topic, id=topic_id)
    permission_denied_response = check_strict_topic_owner(topic_obj, request.user)
    if permission_denied_response:
        return permission_denied_response

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_obj = form.save(commit=False)
            new_entry_obj.topic = topic_obj
            new_entry_obj.save()
            messages.success(request, "Entry added successfully!")
            return redirect('learning_logs:topic', topic_id=topic_obj.id)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {'topic': topic_obj, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic_obj = entry.topic
    permission_denied_response = check_strict_topic_owner(topic_obj, request.user)
    if permission_denied_response:
        return permission_denied_response

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated successfully!")
            return redirect('learning_logs:topic', topic_id=topic_obj.id)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {'entry': entry, 'topic': topic_obj, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    topic_obj = get_object_or_404(Topic, id=topic_id)
    if topic_obj.owner != request.user:
        messages.error(request, "You are not allowed to delete this topic.")
        return redirect('learning_logs:topics')

    if request.method == 'POST':
        topic_obj.delete()
        messages.success(request, f"Topic '{topic_obj.text}' and all its entries have been deleted.")
        return redirect('learning_logs:topics')

    context = {'topic': topic_obj}
    return render(request, 'learning_logs/delete_topic_confirm.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic_obj = entry.topic
    if topic_obj.owner != request.user:
        messages.error(request, "You are not allowed to delete this entry.")
        return redirect('learning_logs:topic', topic_id=topic_obj.id)

    if request.method == 'POST':
        entry_text_preview = entry.text[:30] + "..." if len(entry.text) > 30 else entry.text
        entry.delete()
        messages.success(request, f"Entry '{entry_text_preview}' has been deleted.")
        return redirect('learning_logs:topic', topic_id=topic_obj.id)

    context = {'entry': entry, 'topic': topic_obj}
    return render(request, 'learning_logs/delete_entry_confirm.html', context)