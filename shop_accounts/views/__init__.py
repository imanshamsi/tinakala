from shop_accounts.views.views_address import *
from shop_accounts.views.views_comment import *
from shop_accounts.views.views_favorite import *
from shop_accounts.views.views_identity import *
from shop_accounts.views.views_order import *
from shop_accounts.views.views_profile import *
from shop_accounts.views.views_ticket import *
from shop_accounts.views.views_visited import *


def accounts_header(request, *args, **kwargs):
    context = {}
    return render(request, 'accounts/shared/AccountsHeader.html', context)


def accounts_footer(request, *args, **kwargs):
    site_info: SiteSetting = SiteSetting.objects.all().first()
    context = {
        'site_info': site_info
    }
    return render(request, 'accounts/shared/AccountsFooter.html', context)
