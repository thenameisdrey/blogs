import os


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#################################################
#	IMPORTS FROM WITHIN Linuxjobber APPLICATION  #

from Courses.models import LabTasks, Lab, Course, CourseTopic, Post
from Courses.forms import DocumentUploadForm
from Courses.utils.djangolabsutils import handle_lab2_uploaded_file, handle_lab3_uploaded_file, handle_lab4_uploaded_file, handle_lab5_uploaded_file

#################################################

from django import template


register = template.Library()



def courses(request):
	courses = Course.objects.all()
	context ={
			'courses': courses		
			}
	return render(request, 'courses/courses.html', context)

class ListCourseTopicView(generic.ListView):
	template_name = 'courses/topics.html'
	context_object_name = 'all_course_topics'

	def get_queryset(self):
		return CourseTopic.objects.filter(course = self.kwargs.get('course_id'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['course'] = Course.objects.get(id = self.kwargs.get('course_id'))
		print(context)
		return context


class DetailCourseTopicView(generic.DetailView):
	template_name = 'courses/topic_detail.html'
	model = CourseTopic
	form_class = DocumentUploadForm

	def get_context_data(self, **kwargs):
		list_topic_view_instance = ListCourseTopicView()

		context = super().get_context_data(**kwargs)

		context['form'] = DocumentUploadForm()

		#get topic details
		topicid = CourseTopic.objects.get(id = self.kwargs.get('pk'))

		context['course'] = Course.objects.get(id = topicid.course_id)

		#query labs		
		context['labs_pk'] =  context['course'].coursetopic_set.all()


		# context['lab'] = Lab.objects.filter(topic_id = topicid)
		print(context)
		return context


def labdetails(request, lab_id):
	labtask = LabTasks.objects.filter(lab_id_id = lab_id)
	topic = CourseTopic.objects.get(id = lab_id)
	course = Course.objects.get(id = topic.id)
	context ={
			'course': course,
			'topic': topic,
			'labtask': labtask,
			'form' : DocumentUploadForm()
			}
	return render(request, 'courses/labdetail.html', context)

class ListLabsView(generic.ListView,):
	template_name = 'courses/labs.html'
	context_object_name = 'all_django_labs'
	paginate_by = 5

	def get_queryset(self):
		return Course.objects.filter(id = self.kwargs.get('course_id'))
	


class DetailLabView(generic.DetailView):
	model = LabTasks
	template_name = 'labs/detail.html'
	form_class = DocumentUploadForm
	labtasks_paginate_by = 5


	def post(self, request, *args, **kwargs):
		object = super().get_object()
		form = DocumentUploadForm(request.POST, request.FILES)
		form.save()
		if form.is_valid() and str(object.lab_number) == '2':
			#<process form cleaned data>
			output = handle_lab2_uploaded_file(request.FILES['document'], request.POST.get("username"))
			return HttpResponse('Out of 100% Your Lab 2 score is: ' + str(output))
		elif form.is_valid() and str(object.lab_number) == '3':
			#<process form cleaned data>
			output = handle_lab3_uploaded_file(request.FILES['document'])
			return HttpResponse('Out of 100% Your Lab 3 score is: ' + str(output))
		elif form.is_valid() and str(object.lab_number) == '4':
			#<process form cleaned data>
			output = handle_lab4_uploaded_file(request.FILES['document'])
			return HttpResponse('Out of 100% Your Lab 4 score is: ' + str(output))
		elif form.is_valid() and str(object.lab_number) == '5':
			#<process form cleaned data>
			output = handle_lab5_uploaded_file(request.FILES['document'])
			return HttpResponse('Out of 100% Your Lab 5 score is: ' + str(output))
		else:
			# pass
			return HttpResponse('Test not passed')





	def get_context_data(self, **kwargs):
		list_labs_view_instance = ListLabsView()

        # Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		#Add document upload form to template
		context['form'] = DocumentUploadForm()
		#query labs		
		context['labs_pk'] = list_labs_view_instance.get_queryset()
		#get total number of labs
		context['number_of_all_labs'] = list_labs_view_instance.get_queryset().count()

		#set pagination
		# paginator = Paginator(labs_list, 1)
		# page =  self.request.GET.get('page')
		# context['page'] = page
		# context['labs_list'] = Paginator(labs_list, 1)
		# paginate page here
		labs_list = list_labs_view_instance.get_queryset()
		paginator = Paginator(labs_list, 1)
		page = self.request.GET.get('page', 1)


		context['lab_tasks'] =  paginator.page(page)

		return context

# notes page views

def details(request):
    posts = Post.objects.all()
    return render(request, 'courses/index.html', {'posts': posts}) 

def notes(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'courses/home.html', {'post': post})