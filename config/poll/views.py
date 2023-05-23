from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Question, Choice, Vote
from .serializer import QuestionSerializer, ChoiceSerializer
from buildings.custom_permission_classes import IsManager

# Create your views here.

class QuestionView(APIView):
    permission_classes = [IsAuthenticated,IsManager]

    def get(self,request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self,request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors':serializer.errors})


class ChoiceView(APIView):
    permission_classes = [IsAuthenticated,IsManager]
    def post(self,request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors':serializer.errors})

    def get(self,request):
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class VoteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,qid):
        question = get_object_or_404(Question, pk=qid)
        try :
            selected_choice = question.choice_set.filter(pk=request.POST.get('choice'))[0]
        except(KeyError,Choice.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        else :
            selected_choice.votes += 1
            selected_choice.save()
            vote = {
                'question':question, 'choice':selected_choice, 'user':request.user
            }
            Vote.objects.create(**vote)
            return Response(status=status.HTTP_200_OK)


class ResultView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,qid):
        choice = Choice.objects.filter(question=qid)
        serializer = ChoiceSerializer(choice, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)