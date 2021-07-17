from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from pure_pagination.mixins import PaginationMixin

from shop_blog.models import BlogTag, BlogCategory, Blog, BlogView
from tinakala.utils import get_visitor_ip_address


class BlogsView(PaginationMixin, ListView):
    template_name = 'blog/SiteBlog.html'
    paginate_by = 8
    queryset = Blog.objects.all().order_by('-timestamp')


class SearchBlogsView(PaginationMixin, ListView):
    template_name = 'blog/SiteBlog.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query is not None:
            return Blog.objects.get_blog_by_search(query=query).order_by('-timestamp')
        else:
            return Blog.objects.all().order_by('-timestamp')


class BlogsViewByCategoriesOrTags(PaginationMixin, ListView):
    template_name = 'blog/SiteBlog.html'
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Blog.objects.get_blog_by_category_or_tag(query=slug).order_by('-timestamp')


def newest_blog_view(request, *args, **kwargs):
    newest_blogs = Blog.objects.all()[:5]
    context = {
        'newest_blogs': newest_blogs,
    }
    return render(request, 'blog/components/blog_newest_blog.html', context)


def categories_blog_view(request, *args, **kwargs):
    categories = BlogCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/components/blog_categories.html', context)


def tags_blog_view(request, *args, **kwargs):
    tags = BlogTag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'blog/components/blog_tags.html', context)


def blog_detail_view(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    categories = blog.categories.all()

    user = get_visitor_ip_address(request=request)
    if user['valid']:
        view = BlogView.objects.blog_view_by_user(user=user['ip'], blog=blog)
        if not view:
            view = BlogView.objects.create(blog=blog, user=user['ip'])
            view.save()

    views = BlogView.objects.blog_view_counts(blog=blog)

    context = {
        'blog': blog,
        'categories': categories,
        'views': views,
    }
    return render(request, 'blog/SiteBlogDetail.html', context)
