from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializer import SnippetSerializer
from .serializer import SnippetModelSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@csrf_exempt
def snippet_list(request):
    """

    :param request: a HTTP request
    :return: JSON Response
    """
    if request.method == 'GET':
        data = Snippet.objects.all()
        serialized = SnippetModelSerializer(data, many=True)
        return JsonResponse(data=serialized.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_details(request, snippet_id):

    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist as e:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(data=serializer.data, status=200, safe=False)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)
