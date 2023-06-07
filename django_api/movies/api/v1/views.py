from enum import Enum

from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Case, When
from django.core.paginator import EmptyPage

from ... import models


class RoleType(Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'


def array_agg_role_filter(role: RoleType):
    return ArrayAgg(
                Case(
                    When(
                        personfilmwork__role__isnull=False,
                        personfilmwork__role=role.value,
                        then='person__full_name',
                    )
                ),
                distinct=True,
            )


class MoviesListApi(ListView):
    http_method_names = ('get',)
    paginate_by = 50

    def get_queryset(self):
        return models.Filmwork.objects.prefetch_related(
            'genres', 'person', 'personfilmwork',
        ).values(
            'id', 'title', 'description', 'creation_date', 'type', 'rating'
        ).annotate(
            film_genres=ArrayAgg('genres__name', distinct=True),
            actors=array_agg_role_filter(RoleType.ACTOR),
            directors=array_agg_role_filter(RoleType.DIRECTOR),
            writers=array_agg_role_filter(RoleType.WRITER),
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        qs = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            qs,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'prev': page.previous_page_number() if page.has_previous() else 1,
            'next': page.next_page_number() if page.has_next() else paginator.num_pages,
            'total_pages': paginator.num_pages,
            'results': list(queryset),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MovieApi(DetailView):
    http_method_names = ('get',)

    def get_queryset(self):
        return models.Filmwork.person_set.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context

    def _filmwork_to_dict(self, movie: models.Filmwork):
        return {
            'title': movie.title,
            'description': movie.description,
            'rating': movie.rating
        }
