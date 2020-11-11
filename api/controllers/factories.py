import factory
import persisting_theory
import random
from faker.providers import internet as internet_provider


class FactoriesRegistry(persisting_theory.Registry):
    look_into = "factories"

    def prepare_name(self, data, name=None):
        return name or data._meta.model._meta.label


registry = FactoriesRegistry()


class StockazIOProvider(internet_provider.Provider):
    """
    Our own faker data generator, since built-in ones are sometimes
    not random enough
    """

    def user_name(self):
        u = super().user_name()
        return "{}{}".format(u, random.randint(10, 999))


factory.Faker.add_provider(StockazIOProvider)
