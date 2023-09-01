from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SnippetDetails, SnippetList, SnippetListMixin, SnippetDetailMixin
from .views import UserList, UserDetails
from .views import SnippetGenericView, SnippetGenericUpdateDeleteView
from rest_framework import routers
from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'usersets', UserViewSet, basename='userset')


urlpatterns = [
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:snippet_id>/', SnippetDetails.as_view(), name='snippet-detail'),
    path('users/', UserList.as_view(), name='users'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('mix-snippets/', SnippetListMixin.as_view()),
    path('mix-snippets/<int:pk>/', SnippetDetailMixin.as_view()),
    path('generic-snippets/', SnippetGenericView.as_view(), name='generic-snippet-list'),
    path('generic-snippets/<int:id>/', SnippetGenericUpdateDeleteView.as_view(), name='generic-snippet')
]

urlpatterns += router.urls


# urlpatterns = format_suffix_patterns(urlpatterns)
