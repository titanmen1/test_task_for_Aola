import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from app.models import Note, Ad, Achievement
from app.tests.factories import UserFactory, AdFactory, NoteFactory, AchievementFactory


class TestPersonFeedAPIVew(TestCase):
    URL = '/person_feed/{user_id}'

    def test_result_with_ads(self):
        user1 = UserFactory(username='test1')
        user2 = UserFactory(username='test2')

        AdFactory(published=datetime.datetime.now())
        AdFactory()
        AdFactory(published=datetime.datetime.now() - datetime.timedelta(days=10))

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 2)
        self.assertEqual(response1.json()["results"][0]["post_type"], Ad.POST_TYPE)
        response2 = APIClient().get(path=self.URL.format(user_id=user2.pk))
        self.assertEqual(len(response2.json()["results"]), 2)

    def test_result_with_notes(self):
        user1 = UserFactory(username='test1')
        user2 = UserFactory(username='test2')

        NoteFactory(author=user1)
        NoteFactory(author=user1)
        NoteFactory(author=user2)

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 2)
        self.assertEqual(response1.json()["results"][0]["post_type"], Note.POST_TYPE)
        response2 = APIClient().get(path=self.URL.format(user_id=user2.pk))
        self.assertEqual(len(response2.json()["results"]), 1)

    def test_result_with_achievements(self):
        user1 = UserFactory(username='test1')
        user2 = UserFactory(username='test2')

        achi1 = AchievementFactory()
        achi2 = AchievementFactory()
        achi3 = AchievementFactory()

        user1.achievements.set([achi1, achi2])
        user2.achievements.set([achi3])

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 2)
        self.assertEqual(response1.json()["results"][0]["post_type"], Achievement.POST_TYPE)
        response2 = APIClient().get(path=self.URL.format(user_id=user2.pk))
        self.assertEqual(len(response2.json()["results"]), 1)

    def test_full_person_feed(self):
        user1 = UserFactory(username='test1')
        user2 = UserFactory(username='test2')

        AdFactory(published=datetime.datetime.now())
        AdFactory()
        AdFactory(published=datetime.datetime.now() - datetime.timedelta(days=10))

        NoteFactory(author=user2)
        NoteFactory(author=user1)
        NoteFactory(author=user2)

        achi1 = AchievementFactory()
        achi2 = AchievementFactory()
        achi3 = AchievementFactory()

        user1.achievements.set([achi2])
        user2.achievements.set([achi1, achi3])

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 4)
        response2 = APIClient().get(path=self.URL.format(user_id=user2.pk))
        self.assertEqual(len(response2.json()["results"]), 6)

    def test_ordering(self):
        user1 = UserFactory(username='test1')

        AdFactory(published=datetime.datetime.now())
        NoteFactory(author=user1)
        achi1 = AchievementFactory()
        AdFactory(published=datetime.datetime.now())

        user1.achievements.set([achi1])
        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 4)
        self.assertEqual(response1.json()["results"][0]["post_type"], Ad.POST_TYPE)
        self.assertEqual(response1.json()["results"][1]["post_type"], Achievement.POST_TYPE)
        self.assertEqual(response1.json()["results"][2]["post_type"], Note.POST_TYPE)
        self.assertEqual(response1.json()["results"][3]["post_type"], Ad.POST_TYPE)

    def test_search(self):
        user1 = UserFactory(username='test1')

        AdFactory(published=datetime.datetime.now(), title="Test Ad")
        NoteFactory(author=user1, title="Test Note")

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk) + "?search=ad")
        self.assertEqual(len(response1.json()["results"]), 1)
        response2 = APIClient().get(path=self.URL.format(user_id=user1.pk) + "?search=Text")
        self.assertEqual(len(response2.json()["results"]), 0)
        response3 = APIClient().get(path=self.URL.format(user_id=user1.pk) + "?search=Test")
        self.assertEqual(len(response3.json()["results"]), 2)
        response4 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response4.json()["results"]), 2)

    def test_filter(self):
        user1 = UserFactory(username='test1')

        AdFactory(published=datetime.datetime.now(), title="Test Ad")
        NoteFactory(author=user1, title="Test Note")
        achi1 = AchievementFactory()
        user1.achievements.set([achi1])

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk) + f"?filter={Note.POST_TYPE}")
        self.assertEqual(len(response1.json()["results"]), 2)
        self.assertEqual(response1.json()["results"][0]["post_type"], Note.POST_TYPE)
        self.assertEqual(response1.json()["results"][1]["post_type"], Ad.POST_TYPE)

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk) + f"?filter={Achievement.POST_TYPE}")
        self.assertEqual(len(response1.json()["results"]), 2)
        self.assertEqual(response1.json()["results"][0]["post_type"], Achievement.POST_TYPE)
        self.assertEqual(response1.json()["results"][1]["post_type"], Ad.POST_TYPE)

    def test_pagination(self):
        user1 = UserFactory(username='test1')

        AdFactory(published=datetime.datetime.now(), title="Test Ad")
        AdFactory(published=datetime.datetime.now(), title="Test Ad1")
        AdFactory(published=datetime.datetime.now(), title="Test Ad2")
        NoteFactory(author=user1, title="Test Note")
        achi1 = AchievementFactory()
        user1.achievements.set([achi1])

        response1 = APIClient().get(path=self.URL.format(user_id=user1.pk))
        self.assertEqual(len(response1.json()["results"]), 5)
        self.assertTrue(response1.json()["links"])
        self.assertTrue(response1.json()["links"]["next"])

        response2 = APIClient().get(path=response1.json()["links"]["next"])
        self.assertEqual(len(response2.json()["results"]), 2)
