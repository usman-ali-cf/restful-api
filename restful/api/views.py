from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from rest_framework.decorators import api_view
from .serializer import SnippetSerializer
from rest_framework import status
from .serializer import SnippetModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

# Create your views here.
permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ViewSet):
    """
    a simple viewset to list and retrieve users
    """
    permission_classes = []

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        users = User.objects.all()
        user = get_object_or_404(users, pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    @action(detail=True, permission_classes=permission_classes)
    def get_permissions(self):
        if self.action == "list":
            permission_class_list = []
        else:
            permission_class_list = []

        return [permission() for permission in permission_class_list]

    def create(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    @action(detail=False)
    def recent_user(self, request):
        recent_users = User.objects.all().order_by("-last_login")[0]
        serializer = UserSerializer(recent_users)
        return JsonResponse(serializer.data)








class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SnippetGenericView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    permission_classes = permission_classes
    serializer_class = SnippetSerializer

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = SnippetModelSerializer(query_set, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetGenericUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Snippet.objects.all()
    permission_classes = permission_classes
    serializer_class = SnippetSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        snippet = self.get_object()
        serialized = SnippetModelSerializer(snippet)
        return JsonResponse(serialized.data)

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        snippet.delete()
        serialized = SnippetModelSerializer(snippet)
        return JsonResponse(serialized.data)

    def update(self, request, *args, **kwargs):
        snippet = self.get_object()
        data = JSONParser().parse(request)
        serialized = SnippetModelSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_200_OK)
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        snippet = self.get_object()
        data = JSONParser().parse(request)
        serialized = SnippetModelSerializer(snippet, data=data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_200_OK)
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetList(mixins.CreateModelMixin, APIView):
    permission_classes = permission_classes

    def get(self, request, format=None):
        data = Snippet.objects.all()
        serialized = SnippetModelSerializer(data, many=True)
        return JsonResponse(data=serialized.data, safe=False)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetails(APIView):
    permission_classes = permission_classes

    def get_object(self, snippet_id):
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except ObjectDoesNotExist as e:
            return HttpResponse(status=404)

    def delete(self, request, snippet_id, format=None):
        snippet = self.get_object(snippet_id)
        snippet.delete()
        return HttpResponse(status=status.HTTP_200_OK)

    def get(self, request, snippet_id, format=None):
        snippet = self.get_object(snippet_id)
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    def put(self, request, snippet_id, format=None):
        snippet = self.get_object(snippet_id)
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetListMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = permission_classes

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


def get_object(self, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        return snippet
    except ObjectDoesNotExist as e:
        return HttpResponse(status=404)


class SnippetDetailMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = permission_classes

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
