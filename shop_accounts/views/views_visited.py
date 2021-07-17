from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from pure_pagination import PaginationMixin

from shop_products.models import ProductVisit


class LastVisitedView(PaginationMixin, LoginRequiredMixin, ListView):
    template_name = 'accounts/SiteUserLastVisited.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductVisit.objects.get_product_by_user(user=self.request.user)[:8]

