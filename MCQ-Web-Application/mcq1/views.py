from django.shortcuts import render
from . import forms
from django.forms import ValidationError
from mcq1.forms import UserForm, FormName
from .models import Usr, Quiz, Question
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    quizzes = Quiz.objects.all()
    return render(request, 'mcq1/index.html', {'quizzes':quizzes})

def about(request):
    return render(request, 'mcq1/about.html')

def register(request):
    form1 = forms.UserForm()
    form2 = forms.FormName()

    if request.method =="POST":
        form1 = UserForm(data=request.POST)
        form2 = FormName(data=request.POST)

        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            profile=form2.save(commit=False)
            profile.user=user
            profile.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'mcq1/register.html', {'form1':form1, 'form2':form2})

def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("Invalid Login Details!!!")
    else:
        return render(request, 'mcq1/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def create_quiz(request):
    user = request.user
    usr=Usr.objects.get(user=user)
    naam = user.username
    if usr.is_teacher == True:
        if request.method == 'POST':
            name = request.POST.get('name')
            quis=Quiz.objects.all()
            for qui in quis:
                if qui.quiz_name == name:
                    return HttpResponse("<h1>This name has already been taken....try another one</h1>")
            topic = request.POST.get('topic')
            no_ques = request.POST.get('no_ques')
            request.session['counter']=int(no_ques)
            request.session['qnaam']=name
            quizz=Quiz(quiz_name=name, no_ques=no_ques, topic=topic)
            usr1=User.objects.get(username=naam)
            usr2=Usr.objects.get(user=usr1)
            quizz.author=usr2
            quizz.save()
            return HttpResponseRedirect(reverse('add_question'))


        return render(request,'mcq1/create_quiz.html',{})
    else:
        return HttpResponse("<h1>You need to be a teacher, my boy!!!</h1>")

@login_required
def add_question(request):
    counter=request.session['counter']
    qnaam = request.session['qnaam']
    if request.method == 'POST':
        ques = request.POST.get('question')
        c1 = request.POST.get('choice1')
        c2 = request.POST.get('choice2')
        c3 = request.POST.get('choice3')
        c4 = request.POST.get('choice4')
        cc = request.POST.get('cor_choice')
        pos = request.POST.get('mrks_cor')
        neg = request.POST.get('neg_mrks')
        ques=Question(
            question=ques,
            choice1=c1,
            choice2=c2,
            choice3=c3,
            choice4=c4,
            cor_choice=cc,
            mrk_correct=pos,
            neg_mrk=neg,
        )
        quizz=Quiz.objects.get(quiz_name=qnaam)
        ques.quiz=quizz
        ques.save()
        counter=counter-1
        request.session['counter'] = counter
        if counter>0:
            return HttpResponseRedirect(reverse('add_question'))
        else:
            return HttpResponseRedirect(reverse('index'))


    return render(request, 'mcq1/add_question.html',{'counter':counter})

def take_quiz(request, pk):
    if request.user.is_authenticated:
        quiz = Quiz.objects.get(pk=pk)
        total = 0
        questions = []
        score = 0
        for ques in Question.objects.all():
            if ques.quiz==quiz:
                total+=ques.mrk_correct
        request.session['total']=total
        request.session['counter']=0
        request.session['score']=score
        # request.session['questions'] = questions
        # return render(request, 'mcq1/take_quiz.html', {'quiz':quiz, 'ques':ques})
        return HttpResponseRedirect(reverse('attempt_ques', kwargs={'pk': pk}))
    else:
        return HttpResponse('<h1>Login required to take the quiz bro!!</h1>')


def attempt_ques(request,pk):
    counter = request.session['counter']
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for ques in Question.objects.all():
        if ques.quiz == quiz:
            questions.append(ques)
    ques = questions[counter]
    total = request.session['total']
    flg=0
    if counter<=len(questions)-2:
        flg=1
    score = request.session['score']
    if request.method == 'POST':
        marked = request.POST.get('marked')
        if marked == ques.cor_choice:
            score = score + ques.mrk_correct
        else:
            score = score + ques.neg_mrk
        request.session['score']=score
        counter=counter+1
        request.session['counter']=counter
        if counter<len(questions):
            return HttpResponseRedirect(reverse('attempt_ques', kwargs={'pk': pk}))
        else:
            return HttpResponseRedirect(reverse('show_score'))
    return render(request, 'mcq1/attempt_ques.html', {'counter': counter, 'ques':ques, 'flg':flg, 'pk':pk, 'score':score})

def show_score(request):
    score = request.session['score']
    total = request.session['total']
    if request.method=='POST':
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'mcq1/take_quiz.html', {'score':score, 'total':total})

#@login_required
def profile(request, pk):
    user1=User.objects.get(pk=pk)
    usr=Usr.objects.get(user=user1)
    return render(request, 'mcq1/profile.html', {'user1':user1, 'usr':usr})

@login_required
def edit_quiz(request):
    user = request.user
    usr = Usr.objects.get(user=user)
    quis = usr.quiz_set.all()
    return render(request, 'mcq1/edit_quiz.html', {'quis':quis, 'usr':usr})

@login_required
def edit_quiz_pk(request, pk):
    quiz=Quiz.objects.get(pk=pk)
    return render(request, 'mcq1/edit_quiz_pk.html', {'quiz':quiz})
