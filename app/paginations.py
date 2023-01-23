from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PersonFeedPagination(LimitOffsetPagination):
    def __init__(self, request):
        self.request = request
        self.limit = self.get_limit(self.request)
        self.offset = self.get_offset(self.request)

    def paginate_result(self, data):
        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')
        if offset:
            data = data[int(offset):]
        if limit:
            data = data[:int(limit)]
        return data

    def get_paginated_response(self, data):
        self.count = len(data)
        result = self.paginate_result(data)

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.count,
            'results': result
        })
