from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, View
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from .forms import NewsLetterForm, EmailPostForm
from . models import NewsLetter
import string

# Create your views here.

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            instance = form.save(commit=False) #we dont want to save just yet
            if NewsLetter.objects.filter(email=instance.email).exists():
                print('Thumbs up....you are on our mailing list')
            else:
                instance.save()
                print('your email has been submitted to our database')
                send_mail('Pytochi.com','Welcome Horse!!!','tochiswork@gmail.com',['instance.email'], fail_silently=False)
    else:
        form = NewsLetterForm()
    context = {'form':form}
    template = "blog/base.html"
    return render(request, template, context)

def post_list(request,hierarchy=None, tag_slug=None,):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in = [tag])

    category = None
    if hierarchy:
        category = get_object_or_404(Category, slug=hierarchy)
        object_list = object_list.filter(category__in = [category])

    paginator = Paginator(object_list, 3)   # 3 posts per page
    page = request.GET.get('page')
    #category = get_object_or_404(Category)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if the page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag, 'category':category})


def post_detail(request,year, month, day,post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    """
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    """

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts= similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    catego = post.category.get_ancestors(include_self=True)

    return render(request, 'blog/post/detail.html',{'post':post, 'similar_posts':similar_posts, 'catego':catego})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # .. send mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = 'Hello, {} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'tochiswork@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent,'cd':cd})


def show_category(request,hierarchy=None):
    object_list = Post.published.all()

    category = None
    if hierarchy:
        category = get_object_or_404(Category, slug=hierarchy)
        object_list = object_list.filter(category__in = [category])

    instance = object_list

    name = hierarchy.split('-')
    name = ' '.join(name)
    category_name = string.capwords(name)

    return render(request, 'blog/post/category/categories.html', {'instance': instance, 'category_name':category_name})

def base_template(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            instance = form.save(commit=False) #we dont want to save just yet
            if NewsLetter.objects.filter(email=instance.email).exists():
                print('Thumbs up....you are on our mailing list')
            else:
                instance.save()
                print('your email has been submitted to our database')
                send_mail('Pytochi.com','Welcome Horse!!!','tochiswork@gmail.com',['instance.email'], fail_silently=False)
    else:
        form = NewsLetterForm()
    context = {'form':form}
    template = "blog/base.html"
    return render(request, template, context)




