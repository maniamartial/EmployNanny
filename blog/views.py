from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Blog, Blogcomment, BlogCommentReply
from .forms import create_blogpost_form, comment_form, commentreply_form
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import get_token
from django.template.defaultfilters import timesince_filter

# Create your views here.

def blogpost_home(request):
    user = request.user
    prev_page = request.GET.get('HTTP_REFERER', None)
    #get search query
    query = request.GET.get('q') if request.GET.get('q') != None else ''

    Allblogs = Blog.objects.all().order_by('-date_published')
    recent_blogs = Blog.objects.all().order_by('-date_published')[:4]

    #apply search filters if exist
    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)
        )
        # check if filterd blogs exist if in return all
        if blogs:
            Allblogs = blogs
        else:
            Allblogs = Blog.objects.all().order_by('-date_published')
    #paginate allblogs
    page = request.GET.get('page')
    p = Paginator(Allblogs, 6)
    blogs = p.get_page(page)

    # create a new blogpost form
    form = create_blogpost_form(initial={'author': user})
    
    context = {
        'recent_blogs': recent_blogs,
        'blogs': blogs,
        'form': form
    }
    return render(request, 'blog/index.html', context)

def show_blogpost(request, pk):
    user = request.user
    #get all blogpost
    recent_blogs = Blog.objects.all().order_by('-date_published')[:4]
    blogs = Blog.objects.all()
    # get blog with_id pk 
    blog_post = Blog.objects.get(id=pk)

    
    # get comments of specific post
    comments = Blogcomment.objects.filter(blog=blog_post)
    #commentreply = BlogCommentReply.object.filter()
    # create a new blogpost and comment form
    form = create_blogpost_form(initial={'author': user})
    commentsForm = comment_form(initial={'author': user, 'blog': blog_post})
    commentreplyForm = commentreply_form(initial={'author': user})

    context = {
        'blog_post': blog_post,
        'recent_blogs': recent_blogs,
        'blogs': blogs,
        'form': form,
        'commentsForm': commentsForm,
        'commentreplyForm': commentreplyForm,
        'comments': comments
    }
    return render(request, 'blog/blog_post.html', context)

def show_authors_blogpost(request, pk):
    user = request.user.username

    # get blogposts of a specific author 
    blogs = Blog.objects.filter(author=pk)
    recent_blogs = Blog.objects.all().order_by('-date_published')[:4]
    p = Paginator(blogs, 6)
    page = request.GET.get('page')
    blogs = p.get_page(page)

    # create a new blogpost form
    form = create_blogpost_form(initial={'author': user})
    context = {
        'blogs': blogs,
        'recent_blogs': recent_blogs,
        'form': form
    }
    return render(request, 'blog/index.html', context)

@login_required(login_url='/auth/login/')
def create_blogpost(request):
    prev_page = request.META.get('HTTP_REFERER', None)

    # check if form is subbmited via POST method
    if request.method == 'POST':
        #bind data to the new blogpost form
        form = create_blogpost_form(request.POST, request.FILES)

        #check if form contains valid data
        if form.is_valid():
            #save blog to the database
            form.save()
            #success message if saved then redirect to the previous page
            messages.success(request, 'Posted')
            return redirect(prev_page)
        
@login_required(login_url='/auth/login/')
def save_comment(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        author = request.POST.get('author')
        text = request.POST.get('text')
        blog = request.POST.get('blog')
        csrf = request.POST.get('csrfmiddlewaretoken')
        user = request.user.username
        userId = request.user.id

        
        if request.method == 'POST':
            form = comment_form(request.POST)
            comment = form.save()
            commentId = {'id': comment.id}
            comments = Blogcomment.objects.filter(blog__id=blog)
            fcomments = [{'text': fcomment.text, 'author': fcomment.author.username,
                           'date_published': timesince_filter(fcomment.date_published), 
                           'token': get_token(request), 
                           'commentReplies': [{'text': commentReply.text, 'author': commentReply.author.username, 'publishedDate': timesince_filter(commentReply.date_published)} for commentReply in fcomment.blogcommentreply_set.all()], 'id': fcomment.id} for fcomment in comments]
            data = {'text': text,
                    'author': author, 
                    'blog': blog, 
                    'csrf': csrf, 
                    'commentId': commentId,
                    'user': user,
                    'userId': userId,
                    'fcomments': fcomments
                    }
            return JsonResponse(data)
    else:
        return JsonResponse({'err': 'seerver error'})
        


    # prev_page = request.META.get('HTTP_REFERER', None)
    # # check if form is subbmited via POST method
    # if request.method == 'POST':
    #      #bind data to the new comment form
    #     form = comment_form(request.POST)
    #     #check if form contains valid data
    #     if form.is_valid():
    #         # save comment to the database
    #         form.save()
    #         #redirect user to previous page
    #         return redirect(prev_page)
        
@login_required(login_url='/auth/login/')       
def save_commentreply(request, comment_pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment = Blogcomment.objects.get(id=comment_pk)
        commentReply = BlogCommentReply.objects.filter(blogcomment__id=comment_pk)
       
        if request.method == 'POST':
            text = request.POST.get('text')
            author = request.POST.get('author')
            form = commentreply_form(data={ 'blogcomment': comment, 'text': text, 'author': author})

            if form.is_valid():
                savedForm = form.save()
                fcommentReplies = [{'text': commentreply.text, 'author': commentreply.author.username, 'date_published': timesince_filter(commentreply.date_published)} for commentreply in commentReply]
                repDetails = {'author': request.user.username, 'text': savedForm.text, 'commentReplies': fcommentReplies}
                return JsonResponse({'data': repDetails})
            
        else:
            return JsonResponse({'error': 'errroorr'})



  
  
  
  
    # prev_page = request.META.get('HTTP_REFERER', None)
    # comment = Blogcomment.objects.get(id=comment_pk)
    # if request.method == 'POST':
    #     form = commentreply_form(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']
    #         author = form.cleaned_data['author']
    #         newReply = BlogCommentReply(text=text, author=author, blogcomment=comment)
    #         newReply.save()
    #         return redirect(prev_page)
            



