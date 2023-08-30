from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SnippetDetails, SnippetList, SnippetListMixin, SnippetDetailMixin
from .views import api_root, UserList, UserDetails, SnippetHighlighted
from .views import SnippetViewSet
from rest_framework import renderers

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
snippet_details = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
    'patch': 'partial_update',
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = SnippetViewSet.as_view({
    'get': 'list',
})
user_details = SnippetViewSet.as_view({
    'get': 'retrieve',
})


urlpatterns = [
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:snippet_id>/', SnippetDetails.as_view(), name='snippet-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('', api_root),

    path('mix-snippets/', SnippetListMixin.as_view()),
    path('mix-snippets/<int:pk>/', SnippetDetailMixin.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
