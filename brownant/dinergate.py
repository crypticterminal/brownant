from six import with_metaclass
from werkzeug.utils import cached_property
from requests import Session


class DinergateType(type):
    """The metaclass of :class:`~Dinergate` and its subclasses.

    This metaclass will give all members are instance of
    :class:`~werkzeug.utils.cached_property` default names. It is because many
    pipeline properties are subclasses of :class:`cached_property`, but them
    would not be created by decorating functions. They will has not built-in
    :attr:`__name__`, which may cause them could not cache values as expected.
    """

    def __new__(metacls, name, bases, members):
        cls = type.__new__(metacls, name, bases, members)
        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, cached_property) and not value.__name__:
                value.__name__ = name
                value.__module__ = cls.__module__
        return cls


class Dinergate(with_metaclass(DinergateType)):
    """The simple classify crawler.

    :param request: the standard parameter passed by app.
    :param http_client: the instance of :class:`~requests.Session`.
    :param kwargs: other arguments from the URL pattern.
    """

    #: the URL template string for generating crawled target. the `self` could
    #: be referenced in the template.
    #: .e.g. `"http://www.example.com/items/{self.item_id}?page={self.page}"`
    URL_TEMPLATE = None

    def __init__(self, request, http_client=None, **kwargs):
        self.request = request
        self.http_client = http_client or Session()
        # assign arguments from URL pattern
        vars(self).update(kwargs)

    @property
    def url(self):
        """The fetching target URL.

        The default behavior of this property is build URL string with the
        :const:`~Dinergate.URL_TEMPLATE`.

        The subclasses could override :const:`~Dinergate.URL_TEMPLATE` or give
        a different implementation of this property.
        """
        if not self.URL_TEMPLATE:
            raise NotImplemented
        return self.URL_TEMPLATE.format(self=self)
