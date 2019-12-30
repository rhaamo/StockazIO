from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView
from controllers import __version__
from controllers.categories.models import Category
from django.db import models
from django.contrib.admin.utils import NestedObjects
from django.utils.text import capfirst
from django.utils.encoding import force_text
from urllib.parse import urlencode, quote_plus
from django.urls import reverse


def add_common_context(request):
    ctx = {"VERSION": __version__, "categories": Category.objects.all().annotate(parts_count=models.Count("part"))}
    return ctx


class CBVDetailView(DetailView):
    pass


class CBVDeleteView(SuccessMessageMixin, DeleteView):
    template_name = "delete_object.html"
    success_message = "Deleted successfully"

    # Inject deletable objects tree into context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        context["success_url"] = self.success_url
        context["model_name"] = self.object._meta.model_name
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CBVDeleteView, self).delete(request, *args, **kwargs)


def get_deleted_objects(objs):
    collector = NestedObjects(using="default")
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        no_edit_link = "%s: %s" % (capfirst(opts.verbose_name), force_text(obj))
        return no_edit_link

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}

    return to_delete, model_count, protected


def query_reverse(*args, **kwargs):
    query = kwargs.pop("query", {})
    url = reverse(*args, **kwargs)
    return url + "?" + urlencode(query, quote_via=quote_plus)
