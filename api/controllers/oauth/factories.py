import factory
from controllers.factories import registry
from controllers.oauth import models
from controllers.users.factories import UserFactory


@registry.register
class ApplicationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    redirect_uris = factory.Faker("url")
    client_type = models.Application.CLIENT_CONFIDENTIAL
    authorization_grant_type = models.Application.GRANT_PASSWORD
    scope = "read write read:check_oauth_token read:app read:parts write:parts"

    class Meta:
        model = "oauth.Application"


@registry.register
class GrantFactory(factory.django.DjangoModelFactory):
    application = factory.SubFactory(ApplicationFactory)
    scope = factory.SelfAttribute(".application.scope")
    redirect_uri = factory.SelfAttribute(".application.redirect_uris")
    user = factory.SubFactory(UserFactory)
    expires = factory.Faker("future_datetime", end_date="+15m")
    code = factory.Faker("uuid4")

    class Meta:
        model = "oauth.Grant"
