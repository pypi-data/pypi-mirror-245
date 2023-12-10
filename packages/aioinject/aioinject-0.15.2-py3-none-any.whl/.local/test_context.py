from collections.abc import AsyncIterator, Iterator

import pytest

import aioinject
from aioinject import InjectionContext
from aioinject.context import context_var

pytestmark = [pytest.mark.anyio]

container = aioinject.Container()
container.register(aioinject.Callable(int))


@pytest.fixture
async def _container_ctx() -> AsyncIterator[InjectionContext]:
    async with container.context() as ctx:
        yield ctx


@pytest.fixture
def container_ctx(
    _container_ctx: InjectionContext,
) -> Iterator[InjectionContext]:
    token = context_var.set(_container_ctx)
    yield _container_ctx
    context_var.reset(token)


async def test_something(container_ctx: InjectionContext) -> None:
    with container.override(aioinject.Callable(str, type_=int)):
        number = await container_ctx.resolve(int)
        assert number == ""
