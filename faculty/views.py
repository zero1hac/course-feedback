from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as lgin
from django.shortcuts import render,redirect
from django.contrib.auth import logout as lgout
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.core.mail import send_mail
import smtplib

from feedback.models import Question, Department, Faculty, Courses, Student, Feedback, FeedStatus

class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, receivers,subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + self.email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            receivers,
            headers + "\r\n\r\n" + body)

def register(request):
	user = User.objects.create_user(request.POST.get('username'),
							email = request.POST.get('email'),
							password = request.POST.get('password'),
							first_name = request.POST.get('name'))
	Faculty(dept_id = request.POST.get('dept'),user = user,name=request.POST.get('name')).save()
	return HttpResponseRedirect(reverse('faculty:index'))

def index(request):

	if request.user.is_authenticated():
		if request.session['username']!=request.user.username or request.session['password']!=request.user.password:
			logout(request)
			return HttpResponseRedirect('/faculty/login')
		if request.method == "POST" and request.POST.get('id'):
			faculty = Faculty.objects.get(user=request.user)
			faculty.question.remove(Question.objects.get(id=request.POST['id']))
			faculty.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		faculty = Faculty.objects.get(user=request.user)
		faculty.save()
		if request.GET.get('course_id') is not None:
			faculty = Faculty.objects.get(user = request.user)
			feedback = Feedback.objects.filter(course_id = request.GET.get('course_id'),
												faculty = faculty)
			subject_temp = Courses.objects.filter(id = request.GET.get('course_id'))
			subject = ''
			for s in subject_temp:
				subject = s
			count = [0] * 5
			average = 0
			for f in feedback:
				try:
					count[int(f.feedback)-1]+=1
					average += int(f.feedback)
				except:
					temp=5
			if len(feedback)>0:
				average = average*1.0/len(feedback)
			else:
				average = 0
			average = "%.2f"%(average)
			context = RequestContext(request,{
				'courses': faculty.courses.all(),
				'course_id':request.GET.get('course_id'),
				'subject': subject,
				'feedback':feedback,
				'questions':Question.objects.all(),
				'my_questions':faculty.question.all(),
				'count': count,
				'average': average
			})
		else:
			context = RequestContext(request,{
					'courses': faculty.courses.all(),
					'my_questions':faculty.question.all(),
					'questions':Question.objects.all(),
				})
		template = loader.get_template('home_fac.html')
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect("/faculty/login/")

def logout(request):
	lgout(request)
	return redirect('faculty:index')

def otp(request):
	context_dict = {}
	#password = User.objects.make_random_password()
	try:
		user = User.objects.get(username=request.POST['username'])
		# user.set_password(password)
		# user.save()
		# send_mail('OTP login','Your OTP Password is :' + password,'gmits30@gmail.com',[str(user.email)])
		context_dict['username']=user.username
		context_dict['message']='Your one time password has been sent to the registered email. Use it to login.'
		return render(request, 'login_fac.html', context_dict)
	except:
		context_dict['message']='Your one time password could not be sent to the registered user.'
		return render(request, 'login_fac.html', context_dict)

def login(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			return HttpResponseRedirect('/faculty/')
		else:
			logout(request)
			context = RequestContext(request,{
				'depts': Department.objects.all(),'message': ""
				})
			template = loader.get_template('login_fac.html')
			return HttpResponse(template.render(context))

	if request.POST.get('forgotpassword'):
		user = User.objects.get(username = request.POST['username'])
		if not user:
			return HttpResponse('/Error no user//')	
		password = User.objects.make_random_password()
		send_mail('OTP login','Your OTP Password is :' + password,'gmits30@gmail.com',[str(User.objects.get(username = request.POST['username']).email)])
		user.set_password(password)
		user.save()		
		context = RequestContext(request,{
				'depts': Department.objects.all(),
				'message': "An Email has beem sent."
				})
		template = loader.get_template('login_fac.html')
		return HttpResponse(template.render(context))

	user = authenticate(username = request.POST['username'], password = request.POST['password'])      
	if user is not None:
		print user.is_active
		if user.is_active:
			usr = User.objects.get(username = request.POST['username'])
			lgin(request, user)
			request.session['username']=user.username
			request.session['password']=user.password
			return HttpResponseRedirect('/faculty/')
	else:
		context = RequestContext(request,{
				'depts': Department.objects.all(),'message': "Error, user donot exists."
				})
		template = loader.get_template('login_fac.html')
		return HttpResponse(template.render(context))

def newPass(request):
	user = User.objects.get(username = request.POST['username'])
	password = User.objects.make_random_password()
	user.set_password(password)
	user.save()
	gm= Gmail('gmits30@gmail.com', '9478743873')
	gm.send_message([user.email], 'Password', 'Your Password Is' + password)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def addQuestion(request):
	faculty = Faculty.objects.get(user=request.user)
	faculty.question.add(Question.objects.get(id=request.POST.get('question_id')))
	faculty.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


