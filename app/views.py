from rest_framework import generics
from rest_framework import filters

from app.models import Note, Ad, Achievement
from app.paginations import PersonFeedPagination
from app.serializers import AchievementSerializer, NoteSerializer, AdSerializer


class PersonFeedAPIView(generics.GenericAPIView):
    pagination_class = PersonFeedPagination
    search_filter = filters.SearchFilter()
    search_fields = ['title']

    def get(self, request, user_id):
        notes = Note.objects.filter(author_id=user_id)
        ads = Ad.objects.filter(published__isnull=False)
        achievements = Achievement.objects.filter(user=user_id)

        search_str = self.request.query_params.get('search')
        if search_str:
            notes = self.search_filter.filter_queryset(request, notes, self)
            ads = self.search_filter.filter_queryset(request, ads, self)
            achievements = self.search_filter.filter_queryset(request, achievements, self)

        achievements_data = AchievementSerializer(achievements, many=True).data
        notes_data = NoteSerializer(notes, many=True).data
        ads_data = AdSerializer(ads, many=True).data
        res = achievements_data + notes_data + ads_data

        filter_str = self.request.query_params.get('filter')
        if filter_str:
            res = list(filter(lambda item: item["post_type"] == filter_str or item["post_type"] == Ad.POST_TYPE, res))

        res = list(reversed(sorted(res, key=lambda item: item["created"])))

        return self.pagination_class(request).get_paginated_response(res)
