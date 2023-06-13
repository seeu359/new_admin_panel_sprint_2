from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from .. import models
from . import mixins


class MoviesListApi(mixins.MoviesApiMixin, BaseListView):
    http_method_names = ('get',)
    paginate_by = 50
    model = models.Filmwork

    def get_context_data(self, *, object_list=None, **kwargs):
        movies_qs = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            movies_qs,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(mixins.MoviesApiMixin, BaseDetailView):

    def get_context_data(self, *, object_list=None, **kwargs):
        return {**kwargs['object']}
