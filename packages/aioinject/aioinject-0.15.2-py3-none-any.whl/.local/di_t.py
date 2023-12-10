import contextlib
import inspect


@contextlib.contextmanager
def cm():
    yield 42


print(inspect.isgeneratorfunction(cm))
print(inspect.isgeneratorfunction(cm.__wrapped__))
