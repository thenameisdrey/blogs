from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField





fs = FileSystemStorage(location='/media/uploads')



class Course(models.Model):
	course_title = models.CharField(max_length = 200)

	def __str__(self):
		return self.course_title

class CourseTopic(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	topic =  models.CharField(max_length = 200)
	video = models.TextField()

	def __str__(self):
		return self.topic




class Lab(models.Model):
	#topic_id = models.ForeignKey(CourseTopic, on_delete = models.CASCADE)
	lab_title = models.CharField(max_length = 200)
	lab_number = models.IntegerField()


    # created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # updated_at = models.DateTimeField(auto_now=True, editable=False)
    # title = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255,unique=True) 

	def __str__(self):
		return self.lab_title

	class Meta:
		ordering = ('lab_number', )






class Grades(models.Model):
	grade = models.CharField(max_length = 20)

	def __str__(self):
		return self.grade

class GradesReport(models.Model):
	lab_id = models.ForeignKey(Lab, on_delete = models.CASCADE)
	grade_id = models.ForeignKey(Grades, on_delete = models.PROTECT)
	date = models.DateTimeField(default=timezone.now, null=False)
	user_id = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.user_id, self.lab_id, self.grade_id, self.date

class Document(models.Model):
	document = models.FileField(upload_to = 'uploads/')
	uploaded_at = models.DateTimeField(auto_now_add = True)

class MainModel(models.Model):
	title = models.CharField(max_length = 42)
	document = models.ForeignKey(Document, on_delete = models.CASCADE)


class LabTasks(models.Model):
	lab_id = models.ForeignKey(CourseTopic, on_delete = models.CASCADE)
	task_number = models.IntegerField()
	comment = models.TextField()
	note = models.TextField(null = True, blank = True)
	task = models.TextField()
	hint = models.TextField(null = True, blank = True)


	def __str__(self):
		return self.task

	class Meta:
		ordering = ('lab_id', 'task_number')


# Notes page

class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    image_one = models.FileField(blank=True, null=True)
    text_one = models.CharField(max_length=200, blank=True, null=True)
    image_two = models.FileField(blank=True, null=True)
    text_two = models.CharField(max_length=200, blank=True, null=True)
    image_three = models.FileField(blank=True, null=True)
    text_three = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=40, default='', blank=True)

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()

    def __str__(self):
        return self.title