# pylint: disable=C0114,C0116

from delpinos.core.factories.factory import Factory
from delpinos.api.core.factories.api_factory_abstract import ApiFactoryAbstract


class ApiApp(Factory):
    @property
    def impl(self) -> ApiFactoryAbstract:
        return self.instance("api.factory", ApiFactoryAbstract)

    def run(self):
        self.impl.run()
