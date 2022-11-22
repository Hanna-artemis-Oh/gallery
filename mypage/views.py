from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
from django.contrib import auth
from .forms import UserForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from salon.models import ArtUploadModel, ArtKeywordModel, KeywordModel
from django.core.mail.message import EmailMessage


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'mypage/signup.html', {'form':form})


def check_id(request):
    try:
        user = User.objects.get(username=request.GET['username'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data' : "not exist" if user is None else "exist"
    }
    print(result)
    return JsonResponse(result)


def check_email(request):
    # subject = "DALLE에 가입하신 것을 환영합니다."
    # from_email = "dalle@gmail.com"
    # email_ok = False
    try:
        email_addr = request.GET['email']
        user = User.objects.get(email=email_addr)
    except Exception as e:
        user = None
        # to = [email_addr]
        # message = "DALLE로 바로가기"
        # email_ok =  EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
    
    result = {
        'result':'success',
        'data' : "not exist" if user is None else "exist",
        # 'email_ok' : email_ok
    }
    print(result)
    return JsonResponse(result)


# 로그인 # auth
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'mypage/login.html', {'form': form})


# 로그아웃 # auth
def logout(request):
    auth.logout(request)
    return redirect('index')


### user name으로 구현
# 타인 접속 or 로그인 하지 않았을 때, opage.html 화면 보여줌
# current_user 현재 사용하고 있는 유저, exist_user = 존재하는 유저 네임
def mypage(request, user_name):
    # current_user = request.user
    print(user_name)
    try:
        exist_user = User.objects.get(username=user_name)
        images = ArtUploadModel.objects.filter(user=exist_user, kind=1)
        context = {'userid':exist_user.username, 'images':images}
        return render(request, 'mypage/mypage.html', context)
    
    except Exception as e:
        exist_user = None
        print(e)
        return HttpResponse("error 404")
    
def delete_item(request, user_name):
    json_data = json.loads( request.body )
    img_id = json_data['del_item']
    try:
        del_item = ArtUploadModel.objects.get(pk=img_id)
        print(del_item)
        ArtKeywordModel.objects.filter(art=del_item).delete()
        del_item.delete()
    except Exception as e:
        print(e)
        print("not deleted")
    data = {'result':'successful'}
    return JsonResponse(data)




def setting(request):
    return render(request, 'mypage/setting.html', {})


def find_id(request):
    subject = "DALLE에 가입하신 정보입니다."
    from_email = "dalle@gmail.com"
    error_msg = []
    email_ok = False
    if request.method == "POST":
        signed_email = request.POST.get('signed-email')
        try:
            user_id = User.objects.get(email=signed_email).username
            to = [signed_email]
            message = "DALLE에 가입하신 아이디는 [ " + user_id + " ] 입니다."
            print(user_id)
            email_ok =  EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        except:
            error_msg = ["이메일이 바르게 입력되지 않았거나 가입된 정보가 없습니다."]

    return render(request, 'mypage/find_id.html', {'error_msg':error_msg, 'email_ok':email_ok})
