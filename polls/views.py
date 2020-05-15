from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Question

# Create your views here.
def index(request):
    questions = Question.objects.order_by('-pub_date')[:5]
    context = { 'questions': questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question Does Not exist')
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    response = "You are looking at results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You are voting on question %s." % question_id)