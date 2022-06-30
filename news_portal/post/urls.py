from django.urls import path
from django_filters.views import FilterView

from .filters import PostFilter
from .views import ArticleCreateView
from .views import ArticleDeleteView
from .views import ArticleUpdateView

from .views import CategoriesListView
from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView
from .views import SubscribeToCategoryView

urlpatterns = [
    path("", PostListView.as_view()),
    path("search/", FilterView.as_view(filterset_class=PostFilter)),
    path("create/", PostCreateView.as_view()),
    path("<int:pk>/", PostDetailView.as_view()),
    path("<int:pk>/edit/", PostUpdateView.as_view()),
    path("<int:pk>/delete/", PostDeleteView.as_view()),

    path("create/", ArticleCreateView.as_view()),
    path("<int:pk>/edit/", ArticleUpdateView.as_view()),
    path("<int:pk>/delete/", ArticleDeleteView.as_view()),

    path("categories/", CategoriesListView.as_view()),
    path("categories/<int:category_id>/subscribe/", SubscribeToCategoryView.as_view()),
]
