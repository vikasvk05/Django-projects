#from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import render,get_object_or_404
from .models import Question,Choice

# Create your views here.
# ************** Here we create the generic view *******************

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'q_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select the choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

# ***** This is the normal view *******

# def index(request):
#     q_list = Question.objects.order_by('pub_date')[:5]
#     context ={
#         "q_list":q_list
#     }
#     return render(request,'polls/index.html',context)

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})

# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})

# def vote(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError,Choice.DoesNotExist):
#         return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select the choice"})
#     else:
#         selected_choice.vote += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
#     #return HttpResponse("You'r are voting on questions %s."%question_id)
