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
	Student(dept_id = request.POST.get('dept'),user = user).save()
	return HttpResponseRedirect(reverse('feedback:index'))

def index(request):
	if request.user.is_authenticated():
		if request.session['username']!=request.user.username or request.session['password']!=request.user.password:
			logout(request)
			return HttpResponseRedirect('/login')
		name = request.user.first_name + request.user.last_name
		if 'course_id' in request.GET.keys() :
			student = Student.objects.get(user=request.user)
			context = RequestContext(request,{
					'selected_course':Courses.objects.get(id=request.GET['course_id']),
					'courses': Courses.objects.filter(dept=student.dept),
					'selected' : student.courses.all(),
					'name' : name,
					'faculty' : Faculty.objects.filter(dept=student.dept,
							courses=Courses.objects.get(id=request.GET['course_id']))
				})
			template = loader.get_template('home.html')
			return HttpResponse(template.render(context))
		else:
			student = Student.objects.get(user=request.user)
			context = RequestContext(request,{
					'courses': Courses.objects.filter(dept=student.dept),
					'selected' : student.courses.all(),
					'name' : name,
					'faculty' : Faculty.objects.filter(dept=student.dept)
				})
			template = loader.get_template('home.html')
			return HttpResponse(template.render(context))

	else:
		#return HttpResponse("YYGTYs")
		return HttpResponseRedirect("/login/")

def logout(request):
	lgout(request)
	return redirect('feedback:login')

def otp(request):
	context_dict = {}
	#password = User.objects.make_random_password()
	try:
		user = User.objects.get(username=request.POST['username'])
		#user.set_password(password)
		#user.save()
		#send_mail('OTP login','Your OTP Password is : ' + password,'gmits30@gmail.com',[str(user.email)])
		context_dict['username']=user.username
		context_dict['message']='Your one time password has been sent to the registered email. Use it to login.'
		return render(request, 'login.html', context_dict)
	except:
		context_dict['message']='Your one time password could not be sent to the registered user.'
		return render(request, 'login.html', context_dict)

def login(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			return index(request)
		else:
			context = RequestContext(request,{
				'depts': Department.objects.all()
				})
			template = loader.get_template('login.html')
			return HttpResponse(template.render(context))

	if request.POST.get('forgotpassword'):
		user = User.objects.get(username = request.POST['username'])
		if not user:
			return HttpResponse('/Error no user//')	
		password = User.objects.make_random_password()
		send_mail('OTP login','Your OTP Password is : ' + password,'gmits30@gmail.com',[str(User.objects.get(username = request.POST['username']).email)])
		user.set_password(password)
		user.save()		
		return HttpResponseRedirect('/login/')

	user = authenticate(username = request.POST['username'], password = request.POST['password'])      
	if user is not None:
		print user.is_active
		if user.is_active:
			usr = User.objects.get(username = request.POST['username'])
			lgin(request, user)
			request.session['username']=user.username
			request.session['password']=user.password
			return HttpResponseRedirect('/')
		else:
			context = RequestContext(request,{
				'depts': Department.objects.all(),
				'message': "Error, User is not active."
				})
			template = loader.get_template('login.html')
			return HttpResponse(template.render(context))
	else:
		context = RequestContext(request,{
				'depts': Department.objects.all(),
				'message': "Error, User donot exists."
				})
		template = loader.get_template('login.html')
		return HttpResponse(template.render(context))

def newPass(request):
	user = User.objects.get(username = request.POST['username'])
	password = User.objects.make_random_password()
	user.set_password(password)
	user.save()
	gm= Gmail('gmits30@gmail.com', '9478743873')
	gm.send_message([user.email], 'Password', 'Your Password Is' + password)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addCourse(request):
	student = Student.objects.get(user=request.user)
	student.courses.add(Courses.objects.get(id=request.POST.get('course_id')))
	student.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def feedback(request):
	feed = Feedback.objects.filter(course = request.POST.get('course_id'),student=Student.objects.get(user=request.user), faculty=Faculty.objects.get(id=request.POST.get('faculty_id')))
	name = request.user.first_name + request.user.last_name
	if len(feed): 
		context = RequestContext(request,{
			'depts': Department.objects.all(),'message': "You have already submitted feedback for the concerned course and the faculty.",
			'name' : name
			})
		template = loader.get_template('return.html')
		return HttpResponse(template.render(context))
	else:
		student = Student.objects.get(user=request.user)
		faculty = Faculty.objects.get(id=request.POST.get('faculty_id'))
		print request.POST
		context = RequestContext(request,{
				'course_id': request.POST.get('course_id'),
				'faculty_id' : request.POST.get('faculty_id'),
				'question' : faculty.question.all(),
				'name' : name
			})
		template = loader.get_template('feedback.html')
		return HttpResponse(template.render(context))

def addFeedback(request):
	if request.method=='GET':
		return index(request)

	fac=Faculty.objects.get(id=request.POST.get('faculty_id'))
	question = fac.question.all()
	print question

	for each_item in question:
		print each_item.id
		print each_item
		feedbackForQuestion = request.POST.get(str(each_item.id))
		print type(feedbackForQuestion)
		print feedbackForQuestion
		Feedback(student=Student.objects.get(user=request.user),
				 course = Courses.objects.get(id = int(request.POST['course_id'])),
				 faculty=Faculty.objects.get(id=request.POST.get('faculty_id')), 
				 question=each_item, 
				 feedback= feedbackForQuestion).save()
	return HttpResponseRedirect(reverse('feedback:index'))
