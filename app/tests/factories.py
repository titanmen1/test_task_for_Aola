import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.User"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.Ad"


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.Note"


class AchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.Achievement"
