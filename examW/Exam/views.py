from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Answers
from django.views.decorators.csrf import csrf_exempt

import os
from datetime import datetime
from subprocess import Popen, PIPE
# Create your views here.
QCOUNT=1
quc=[0]*QCOUNT

def redir(request):
    return redirect('home')

def execJS(request):
    if request.method != 'POST':
        return HttpResponse()
    else:
        code=request.POST.get('code')
        sout, serr=Popen('echo "{0}" | nodejs'.format(code), shell=True, stdout=PIPE, stderr=PIPE).communicate()
        if len(serr)>0:
            try:
                serr=serr.decode('utf8')
            except UnicodeDecodeError:
                serr=serr.decode('cp949')
            return HttpResponse('<div style="color:red;">'+serr+'</div>')
        else:
            try:
                sout=sout.decode('utf8')
            except UnicodeDecodeError:
                sout=sout.decode('cp949')
            return HttpResponse(sout)

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

def home(request):
    uip=getIP(request)
    f=open('./uiplog.txt','a')
    f.write(uip+'\n')
    f.write(str(datetime.now())+'\n')
    f.close()
    return render(request, 'Exam/index.html', {'qus':quc})

def question(request, qno):
    uip=getIP(request)
    htmdir=os.scandir('./Exam/templates/Exam')
    quc=len([_ for _ in htmdir])-2
    if qno<0 or qno>quc:
        return HttpResponse('<script type="text/javascript">alert("없는 번호입니다.");</script>')
    if request.method=='GET':
        return render(request, 'Exam/q{0}.html'.format(qno), )
    elif request.method=='POST':
        Answers(uip=uip, q=qno, a=str(request.POST.get('answer'))).save()
        return

