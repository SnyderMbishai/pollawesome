from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# generic views
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        chosen = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #form
        return render(request,'polls/detail.html',{
            'question': question,
            'error_message': "You did not select a choice."
            })
    else:
        chosen.votes += 1
        chosen.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# OLD
# # Create your views here.
# def index(request):
#     questions = Question.objects.order_by('-pub_date')[:5]
#     context = { 'questions': questions}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question Does Not exist')
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html' , {'question':question})

#     # response = "You are looking at results of question %s."
#     # return HttpResponse(response % question_id)

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         chosen = question.choice_set.get(pk=request.POST['choice'])
#     except(KeyError, Choice.DoesNotExist):
#         #form
#         return render(request,'polls/detail.html',{
#             'question': question,
#             'error_message': "You did not select a choice."
#             })
#     else:
#         chosen.votes += 1
#         chosen.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#     # return HttpResponse("You are voting on question %s." % question_id)