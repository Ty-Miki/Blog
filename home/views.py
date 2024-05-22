from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

def post_list(request):

    post_list = Post.published.all()

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
                  {"posts": posts})

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
    
    return render(request,
           "blog/post/detail.html",
           {"post": post,
            "comments": comments,
            "form": form})

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
