from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(
            {'data':data,}
        )

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.data.get('page', 1) 
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message='Invalid page'
            )
            raise NotFound(msg)

        self.request = request
        return list(self.page)

