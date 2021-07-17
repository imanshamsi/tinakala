from django.urls import path

from .views import (
    BlogsView,
    SearchBlogsView,
    BlogsViewByCategoriesOrTags,
    blog_detail_view,
)


app_name = 'blog'
urlpatterns = [
    path('', BlogsView.as_view(), name='show-blogs'),
    path('search/', SearchBlogsView.as_view(), name='show-blogs-by-search'),
    path('search/<slug>', BlogsViewByCategoriesOrTags.as_view(), name='show-blogs-by-query'),
    path('<blog_id>', blog_detail_view, name='show-blog-detail'),
]
