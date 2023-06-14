from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q

from .. import models
from .. import mixins


class MoviesApiMixin:
    http_method_names = ('get',)
    paginate_by = 50
    model = models.Filmwork

    @staticmethod
    def _filter_and_aggregate_roles(role: mixins.RoleType) -> ArrayAgg:
        return ArrayAgg(
            'person__full_name',
            distinct=True,
            filter=Q(personfilmwork__role=role.value)
        )

    def get_queryset(self):
        return super().get_queryset(
        ).prefetch_related(
            'genres',
            'person',
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'type',
            'rating',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self._filter_and_aggregate_roles(mixins.RoleType.ACTOR),
            directors=self._filter_and_aggregate_roles(mixins.RoleType.DIRECTOR),
            writers=self._filter_and_aggregate_roles(mixins.RoleType.WRITER),
        ).order_by('title')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
