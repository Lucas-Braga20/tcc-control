"""
Mixins for the tcc control project.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DisablePaginationMixin:
    def paginate_queryset(self, queryset):
        if 'pagination' in self.request.query_params:
            pagination_enabled = self.request.query_params.get('pagination').lower() == 'true'
            if not pagination_enabled:
                return None

        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        if data is None:
            return Response(data)

        return super().get_paginated_response(data)
