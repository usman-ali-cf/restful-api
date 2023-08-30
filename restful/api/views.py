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
from rest_framework import viewsets


# Create your views here.
permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class SnippetList(APIView):
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


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlighted(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    permission_classes = permission_classes
    serializer_class = SnippetModelSerializer

    @action(detail=True, render_classes=[renderers.StaticHTMLRenderer])
    def highlightSnippet(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
