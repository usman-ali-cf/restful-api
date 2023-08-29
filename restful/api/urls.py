from django.urls import path
from .views import snippet_details, snippet_list

urlpatterns = [
    path('snippets/', snippet_list),
    path('snippets/<int:snippet_id>/', snippet_details),
]