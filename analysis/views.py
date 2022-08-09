import math
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
	return render(request,  'analysis/user_register_completed_page.html')
 
 
#error page
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
