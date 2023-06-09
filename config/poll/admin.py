from django.contrib import admin
from .models import Question, Choice, Vote
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'pub_date', 'created_date']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'choice_text', 'votes', 'question']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote)