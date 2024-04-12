from django.views.generic import TemplateView

from menu.models import Menu


# Create your views here.
class IndexView(TemplateView):
    template_name = 'menu/index.html'
    extra_context = {
        'menus':  Menu.objects.filter(parent__isnull=True)
    }
