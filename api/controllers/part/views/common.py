from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView
from controllers import __version__
from controllers.categories.models import Category


def add_common_context(request):
    ctx = {"VERSION": __version__, "categories": Category.objects.all()}
    return ctx


class CBVDetailView(DetailView):
    pass


class CBVDeleteView(SuccessMessageMixin, DeleteView):
    success_message = "Deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CBVDeleteView, self).delete(request, *args, **kwargs)
