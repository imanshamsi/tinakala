from django.shortcuts import render

from shop_settings.models import SiteSetting


def site_privacy_rules(request):
    site_privacy: SiteSetting = SiteSetting.objects.all().first()
    context = {
        'site_privacy': site_privacy,
    }
    return render(request, 'settings/SitePrivacy.html', context)
