from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.urls import reverse

from .models import Question
# Create your views here.

def index(request):
    latest_ql = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_ql': latest_ql,}
    return render(request, 'pages/index.html', context)

def detail(request, question_id):
    q = get_object_or_404(Question, pk= question_id)
    return render(request, 'pages/details.html', {'question': q})

def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'pages/results.html', {'question': q})

def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pages/detail.html', {'question': q, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('pages:results', args=(question.id,)))
