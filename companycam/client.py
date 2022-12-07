from __future__ import annotations

import typing

import httpx

EventHook = typing.Callable[..., typing.Any]
EventHooks = typing.Mapping[str, typing.List[EventHook]]


class LazyClient(object):
    """Thin wrapper around `httpx.Client`.

    Clients are useful because you can configure common parameters to use between
    requests e.g. auth, headers, base URL etc. However they are best used in context
    managers to ensure that connections are cleaned up (i.e. `with Client() as client:`,
    see https://www.python-httpx.org/advanced/#client-instances). They also cannot be
    reinstantiated once closed.

    This class allows us to store a client configuration in an object to be used at a
    later time, so we can leverage the benefits of `httpx.Client` and its configuration
    merging while also observing HTTPX's recommended best practice.
    """

    def __init__(
        self,
        auth: httpx.Auth | None = None,
        headers: typing.Mapping | None = None,
        event_hooks: EventHooks | None = None,
        base_url: str = "",
    ) -> None:
        self.auth = auth
        self.headers = httpx.Headers(headers) if headers else headers
        self.event_hooks = event_hooks
        self.base_url = httpx.URL(base_url)

    def make_client(self) -> httpx.Client:
        return httpx.Client(
            auth=self.auth,
            headers=self.headers,
            event_hooks=self.event_hooks,
            base_url=self.base_url,
        )
