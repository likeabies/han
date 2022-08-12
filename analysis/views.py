import math
from django.db.models import Count
from django.shortcuts import render, redirect
from analysis.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic import DetailView


# Create your views here.

def main_page(request):
    return render(request, 'analysis/main.html')


# User Page
def user_register_page(request):
    return render(request, 'analysis/user_register.html')


def user_register_idcheck(request):
    if request.method == "POST":
        username = request.POST['username']
    else:
        username = ''

    idObject = User.objects.filter(username__exact=username)
    idCount = idObject.count()

    if idCount > 0:
        msg = "<font color='red'>already existing ID.</font><input type='hidden' name='IDCheckResult' id='IDCheckResult' value=0 />"
    else:
        msg = "<font color='blue'>available ID.</font><input type='hidden' name='IDCheckResult' id='IDCheckResult' value=1 />"

    return HttpResponse(msg)


def user_register_result(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        birth_year = int(request.POST['birth_year'])
        birth_month = int(request.POST['birth_month'])
        birth_day = int(request.POST['birth_day'])
        date_of_birth = datetime(birth_year, birth_month, birth_day)

    try:
        if username and User.objects.filter(username__exact=username).count() == 0:
            date_of_birth = datetime(birth_year, birth_month, birth_day)
            user = User.objects.create_user(
                username, password, name, email, phone, date_of_birth
            )

            redirection_page = '/user_register_completed/'
        else:
            redirection_page = '/error/'
    except:
        redirection_page = '/error/'

    return redirect(redirection_page)


def user_register_completed(request):
    return render(request, 'analysis/user_register_completed_page.html')


# error page
def error_page(request):
    return render(request, 'analysis/error.html')


# Notice Page
def notice_list_page(request, category=''):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    articles = Notices.objects.all()
    list_count = 10

    if search_text:
        articles = articles.filter(title__contains=search_text)

    paginator = Paginator(articles, list_count)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    articles = paginator.get_page(page)

    page_count = 10
    page_list = []
    first_page = (math.ceil(page / page_count) - 1) * page_count + 1
    last_page = min([math.ceil(page / page_count) * page_count, paginator.num_pages])
    for i in range(first_page, last_page + 1):
        page_list.append(i)

    args = {}
    args.update({"articles": articles})
    args.update({"search_text": search_text})
    args.update({"page_list": page_list})

    return render(request, 'analysis/notice_list.html', args)


class NoticeView(DetailView):
    model = Notices
    template_name = 'analysis/notice_view.html'

    def dispatch(self, request, pk):
        obj = self.get_object()
        if request.user != obj.user:
            obj.view_count = obj.view_count + 1
            obj.save()

        return render(request, self.template_name, {"object": obj})


# login required error page
def login_required_page(request):
    return render(request, 'analysis/login_required_page.html')


# QnA Page (very long)
# QnA list
@login_required(login_url='/login/')
def QnA_list_page(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

        articles = Qna.objects.all()
        list_count = 10

    if search_text:
        articles = articles.filter(title__contains=search_text)

    articles = articles.annotate(reply_count=Count('qnareplies', distinct=True)).order_by('-id')
    if request.user.is_superuser or request.user.is_staff:
        articles=articles
    else:
        articles=articles.filter(user=request.user)

    paginator = Paginator(articles, list_count)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    articles = paginator.get_page(page)

    page_count = 10
    page_list = []
    first_page = (math.ceil(page / page_count) - 1) * page_count + 1
    last_page = min([math.ceil(page / page_count) * page_count, paginator.num_pages])
    for i in range(first_page, last_page + 1):
        page_list.append(i)

    args = {}
    args.update({"articles": articles})
    args.update({"search_text": search_text})
    args.update({"page_list": page_list})
  
    return render(request, 'analysis/QnA_list.html', args)


# QnA view
class QnAView(DetailView):
    model = Qna
    template_name = 'analysis/QnA_view.html'

    def dispatch(self, request, pk):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save()
        if request.user == obj.user or request.user.is_superuser or request.user.is_staff:
            return render(request, self.template_name, {"object": obj})
        else:
            return redirect('/no_authority/')

# QnA write
@login_required
def QnA_write_page(request):
    args = {}

    return render(request, 'analysis/QnA_write.html', args)


@login_required
def QnA_write_result(request):
	if request.method == "POST":
		title = request.POST['title']
		content = request.POST['content']
		try:
			img_file = request.FILES['img_file']
		except:
			img_file = None
	else:
		title = None

	args = {}

	if request.user and title and content:
		article = Qna(user=request.user, title=title, content=content, image=img_file)
		article.save()

		redirection_page = '/QnA/'

	else:
		redirection_page = '/error/'

	return redirect(redirection_page)


# no authority error page
def no_authority_page(request):
    return render(request, 'analysis/no_authority.html')


# QnA delete
@login_required
def QnA_delete_result(request):
    if request.method == "POST":
        article_id = request.POST['article_id']
    else:
        article_id = -1

    args = {}

    article = Qna.objects.get(id=article_id)

    if request.user == article.user:
        article.delete()
        redirection_page = '/QnA/'
    else:
        redirection_page = '/no_authority/'

    return redirect(redirection_page)


# QnA modify
class QnAModifyView(DetailView):
    model = Qna

    template_name = 'analysis/QnA_modify.html'


@login_required
def QnA_modify_result(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        article_id = request.POST['id']
        try:
            img_file = request.FILES['img_file']
        except:
            img_file = None
    else:
        title = None

    args = {}

    try:
        article = Qna.objects.get(id=article_id)
        if request.user and title and content and article_id:

            if article.user != request.user:
                redirection_page = '/no_authority/'
            else:
                article.title = title
                article.content = content
                article.last_update_date = timezone.now()

                if img_file:
                    article.image = img_file
                article.save()
                redirection_page = '/QnA_view/' + article_id + '/'
        else:
            redirection_page = '/error/'
    except:
        redirection_page = '/error/'

    return redirect(redirection_page)
    

# Reply page
@login_required
def reply_write_result(request):
	if request.method == "POST":
		content = request.POST['content']
		id = request.POST['id']
	else:
		content = None

	args={}

	if request.user and content and id:
		article = Qna.objects.get(id=id)
		reply = QnaReplies(article=article, user=request.user, content=content)
		reply.save()
		reply.reference_reply_id=reply.id
		reply.save()
		redirection_page = '/reply_list/' + id + '/'

	else:
		redirection_page = '/error/'

	return redirect(redirection_page)
 

def reply_list(request, article):
	replies = QnaReplies.objects.filter(article__id=article).order_by('reference_reply_id','id')
	args = {}
	args.update({"replies":replies})
	return render(request, 'analysis/reply_list.html', args)
 

class ReplyModifyView(DetailView):
	model = QnaReplies

	template_name = 'analysis/reply_modify.html'


@login_required
def reply_modify_result(request):
	if request.method == "POST":
		content = request.POST['content']
		reply_id = request.POST['id']
	else:
		content = None

	try:
		if request.user and content and reply_id:
			reply = QnaReplies.objects.get(id=reply_id)
			reply.content = content
			reply.save()
			
			redirection_page = '/reply_list/' + str(reply.article.id) + '/'

		else:
			redirection_page = '/error/'
	except:
		redirection_page = '/error/'

	return redirect(redirection_page)
 

@login_required
def reply_delete_result(request):
	if request.method == "POST":
		reply_id = request.POST['reply_id']
	else:
		reply_id = -1

	reply = QnaReplies.objects.get(id=reply_id)

	if request.user == reply.user:
		reply.delete();
		redirection_page = '/reply_list/' + str(reply.article.id) + '/'

	else:
		redirection_page = '/error/'

	return redirect(redirection_page)
 

#CV analysis page
@login_required(login_url='/login/')
def CV_list_page(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

        CVs = Cv.objects.all()
        list_count = 10

    if search_text:
        CVs = CVs.filter(title__contains=search_text)
        
    if request.user.is_superuser or request.user.is_staff:
        CVs=CVs
    else:
        CVs=CVs.filter(user=request.user)

    paginator = Paginator(CVs, list_count)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    articles = paginator.get_page(page)

    page_count = 10
    page_list = []
    first_page = (math.ceil(page / page_count) - 1) * page_count + 1
    last_page = min([math.ceil(page / page_count) * page_count, paginator.num_pages])
    for i in range(first_page, last_page + 1):
        page_list.append(i)

    args = {}
    args.update({"CVs": CVs})
    args.update({"search_text": search_text})
    args.update({"page_list": page_list})
  
    return render(request, 'analysis/CV_list.html', args)


@login_required(login_url='/login/')
def CV_write_page(request):
    args = {}

    return render(request, 'analysis/CV_write.html', args)


@login_required
def CV_write_result(request):
	if request.method == "POST":
		title = request.POST['title']
		job = request.POST['job']
		ability = request.POST['ability']
		content = request.POST['content']

	else:
		title = None

	args = {}

	if request.user and title and content and job:
		CV = Cv(user=request.user, title=title, job=job, ability=ability, content=content)
		CV.save()
    
		redirection_page = '/CV/'

	else:
		redirection_page = '/error/'

	return redirect(redirection_page)


class CvView(DetailView):
    model = Cv
    template_name = 'analysis/CV_view.html'

    def dispatch(self, request, pk):
        obj = self.get_object()
        if request.user == obj.user or request.user.is_superuser or request.user.is_staff:
            return render(request, self.template_name, {"object": obj})
        else:
            return redirect('/no_authority/')


@login_required
def CV_delete_result(request):
    if request.method == "POST":
        CV_id = request.POST['CV_id']
    else:
        CV_id = -1

    args = {}

    CV = Cv.objects.get(id=CV_id)

    if request.user == CV.user:
        CV.delete()
        redirection_page = '/CV/'
    else:
        redirection_page = '/no_authority/'

    return redirect(redirection_page)