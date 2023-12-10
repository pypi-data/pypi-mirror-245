from collections.abc import Sequence
from typing import Any

import aioinject
from aioinject import Provider
from benchmark.dependencies import (
    RepositoryA,
    RepositoryB,
    ServiceA,
    ServiceB,
    UseCase,
    create_session,
)


providers: Sequence[Provider[Any]] = [
    aioinject.Callable(create_session),
    aioinject.Callable(RepositoryA),
    aioinject.Callable(RepositoryB),
    aioinject.Callable(ServiceA),
    aioinject.Callable(ServiceB),
    aioinject.Callable(UseCase),
]


def create_container() -> aioinject.Container:
    container = aioinject.Container()
    for provider in providers:
        container.register(provider=provider)

    return container
