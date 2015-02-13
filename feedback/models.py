from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	def __unicode__(self):
	    return self.question
	question = models.CharField(max_length=200)

class Pass(models.Model):
	user = models.OneToOneField(User)
	password = models.CharField(max_length=100)

class Department(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=50)

class Courses(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=50)
	dept = models.ForeignKey(Department)

class Faculty(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=50)
	dept = models.ForeignKey(Department)
	user = models.OneToOneField(User)
	question = models.ManyToManyField(Question)
	courses = models.ManyToManyField(Courses)
	image = models.FileField(upload_to='/images/', default="/images/noImage.jpg")

class Student(models.Model):
	def __unicode__(self):
		return self.user.username
	dept = models.ForeignKey(Department)
	user = models.OneToOneField(User)
	courses = models.ManyToManyField(Courses)

class Feedback(models.Model):
	def __unicode__(self):
		return self.feedback
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Courses)
	faculty = models.ForeignKey(Faculty)
	question = models.ForeignKey(Question)
	feedback = models.CharField(default = "0", max_length=2)

class FeedStatus(models.Model):
	def __unicode__(self):
		return self.status
	student = models.ForeignKey(Student)
	faculty = models.ForeignKey(Faculty)
	course = models.ForeignKey(Courses)
	status = models.FloatField(default=0.0)