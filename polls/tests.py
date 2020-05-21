import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.

def create_question(question, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question=question,pub_date=time)

class QuestionModelTests(TestCase):
    def test_published_in_future(self):
        """
        Questions published in future should not appear in the recent list, return false.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date = time)
        self.assertIs(question.was_recently_published(), False)

    def test_published_with_old_question(self):
        """
        False for Old questions.
        """
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        question = Question(pub_date = time)
        self.assertIs(question.was_recently_published(), False)

    def test_published_recently_with_recent_question(self):
        """
        True for recently published ones.
        """
        time = timezone.now()
        question = Question(pub_date=time)
        self.assertIs(question.was_recently_published(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        Return an appropriate message when there are no questions.
        """
        res = self.client.get(reverse('polls:index'))
        print(res)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No polls are Available")
        self.assertQuerysetEqual(res.context['questions'],[])

    def test_past_questions(self):
        """
        Displays past published questions.
        """
        create_question(question="past question", days=-30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['questions'], 
            ['<Question: past question>']
        )

    def test_future_question(self):
        """
        Future questions should not appear
        """
        create_question("Future Question", 30)
        res = self.client.get(reverse('polls:index'))
        self.assertContains(res, "No polls are Available")
        self.assertQuerysetEqual(
            res.context['questions'],
            []
        )

    def test_future_and_past_questions(self):
        """
        Should return only past questions
        """
        create_question("Past question.", -30)
        create_question("Future question", 30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['questions'],
            ['<Question: Past question.>']
        )
        
    def test_two_past_questions(self):
        """
        Should show all the questions
        """
        create_question("First Question", -30)
        create_question("Second Question", -30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['questions'],
            ['<Question: Second Question>', '<Question: First Question>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        return 404
        """
        question = create_question("Future question.", 30)
        res = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(res.status_code, 404)

    def test_past_question(self):
        """
        Should show past questions
        """
        question = create_question("Past Question", -30)
        res = self.client.get(reverse('polls:detail', args=(question.id,)))        
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, question.question)
