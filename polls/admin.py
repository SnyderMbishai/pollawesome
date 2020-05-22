from django.contrib import admin

from .models import Question, Choice

# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInLine]    
    # fields = ['pub_date', 'question']
    list_display = ('question', 'pub_date', 'was_recently_published')
    list_filter = ['pub_date']
    search_fields = ['question']

admin.site.register(Question, QuestionAdmin)
