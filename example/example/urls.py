from django.conf.urls import url
from example.views import MyModelListView

urlpatterns = [
    url(r'^$', MyModelListView.as_view()),
]
