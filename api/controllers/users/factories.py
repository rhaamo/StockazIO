import factory

from controllers.factories import registry


class PasswordSetter(factory.PostGenerationMethodCall):
    def call(self, instance, step, context):
        if context.value_provided and context.value is None:
            # disable setting the password, it's set by hand outside of the factory
            return

        return super().call(instance, step, context)


@registry.register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = password = PasswordSetter("set_password", "test")

    class Meta:
        model = "users.User"
        django_get_or_create = ("username",)
