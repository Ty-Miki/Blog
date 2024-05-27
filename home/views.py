from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

from taggit.models import Tag
from django.db.models import Count

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def post_list(request, tag_slug=None):

    post_list = Post.published.all()
    tag = None
    form = SearchForm()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Paginator with 5 posts per page.
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    # Get the posts at page_number.
    try:
        posts = paginator.page(page_number)
    # Get the first page for non-integer page searches.
    except PageNotAnInteger:
        posts = paginator.page(1)
    # Get the last page for empty pages
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  "blog/post/list.html",
                  {"posts": posts,
                   "tag": tag,
                   "form": form})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # List of all active comments
    comments = post.comments.filter(active=True)
    # Form to add new comments
    form = CommentForm()

    # List of similar posts.
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:4]
    
    return render(request,
           "blog/post/detail.html",
           {"post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts})

def  post_share(request, post_id):
    # Retrieve post by ID.
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    # Get form inputs and send data for POST requests.
    if request.method == "POST":
        # Form was submitted.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields pass validation.
            cd = form.cleaned_data
            
            # Send_email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} suggest you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments\n\t{cd['comments']}"
            send_mail(subject, message, cd["email"], [cd['to']])
            sent = True
        
        
    # Get empty for fields for other requests (GET and PUT).
    else:
        form = EmailPostForm()

    # Render post and form to a template.
    return render(request, "blog/post/share.html", {"post": post,
                                                        "form": form,
                                                        "sent": sent})
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # A comment is posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to database
        comment = form.save(commit=False)
        # Assign post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    
    return render(request, "blog/post/comment.html", {"post": post,
                                                      "form": form,
                                                      "comment": comment})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector('title', weight="A") + SearchVector('body', weight="B")
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by("-rank")
        
    return render(request, "blog/post/search.html", {"form": form,
                                                     "query": query,
                                                     "results": results})