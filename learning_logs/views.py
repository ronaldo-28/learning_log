# learning_logs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# from . import views # THIS LINE IS INCORRECT AND SHOULD BE REMOVED if present

# --- CORE VIEWS ---
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all of the current user's topics, and public topics that belong
    to other users.
    """
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

def topic(request, topic_id): # This is the corrected version from your previous input
    """Show a single topic and all its entries."""
    topic_obj = get_object_or_404(Topic, id=topic_id)

    if not topic_obj.public and (not request.user.is_authenticated or topic_obj.owner != request.user):
        raise Http404

    is_owner = request.user.is_authenticated and (request.user == topic_obj.owner)
    entries = topic_obj.entry_set.order_by('-date_added')
    context = {'topic': topic_obj, 'entries': entries, 'is_owner': is_owner}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic_obj = form.save(commit=False)
            new_topic_obj.owner = request.user
            new_topic_obj.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

# --- HELPER FUNCTIONS FOR OWNERSHIP ---
def check_strict_topic_owner(topic_obj, user): # Renamed 'topic' to 'topic_obj' for clarity
    """Ensure the currently logged-in user strictly owns the topic."""
    if topic_obj.owner != user:
        # raise Http404
        return HttpResponseForbidden("You are not the owner of this topic.")


# --- UPDATED VIEWS (new_entry, edit_entry) ---
@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic_obj = get_object_or_404(Topic, id=topic_id) # Renamed 'topic' to 'topic_obj'
    # Use strict check. If check_strict_topic_owner returns a response, we should return that.
    owner_check_response = check_strict_topic_owner(topic_obj, request.user)
    if owner_check_response: # If it returned an HttpResponseForbidden
        return owner_check_response

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_obj = form.save(commit=False)
            new_entry_obj.topic = topic_obj
            new_entry_obj.save()
            return redirect('learning_logs:topic', topic_id=topic_obj.id)

    context = {'topic': topic_obj, 'form': form} # Keep 'topic' in context for template
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic_obj = entry.topic # Renamed 'topic' to 'topic_obj'
    # Use strict check
    owner_check_response = check_strict_topic_owner(topic_obj, request.user)
    if owner_check_response:
        return owner_check_response

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_obj.id)

    context = {'entry': entry, 'topic': topic_obj, 'form': form} # Keep 'topic' in context for template
    return render(request, 'learning_logs/edit_entry.html', context)


# --- NEW DELETE VIEWS ---
@login_required
def delete_topic(request, topic_id):
    """Delete an existing topic and all its entries."""
    topic_obj = get_object_or_404(Topic, id=topic_id) # Renamed 'topic' to 'topic_obj'

    if topic_obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this topic.")

    if request.method == 'POST':
        topic_obj.delete()
        return redirect('learning_logs:topics')

    context = {'topic': topic_obj} # Keep 'topic' in context for template
    return render(request, 'learning_logs/delete_topic_confirm.html', context)

@login_required
def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic_obj = entry.topic # Renamed 'topic' to 'topic_obj'

    if topic_obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this entry.")

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic_obj.id)

    context = {'entry': entry, 'topic': topic_obj} # Keep 'topic' in context for template
    return render(request, 'learning_logs/delete_entry_confirm.html', context)

# Removed old `check_topic_owner` if it's fully replaced by logic in topic view
# and `check_strict_topic_owner`