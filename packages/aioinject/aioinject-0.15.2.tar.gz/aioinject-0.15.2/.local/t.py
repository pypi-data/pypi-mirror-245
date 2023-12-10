import time

import aioinject


class A:
    pass


class B:
    def __init__(self, a: A):
        self.a = a


class C:
    def __init__(self, b: B):
        self.b = b


def simple_factory():
    return C(b=B(a=A()))


def main():
    container = aioinject.Container()
    container.register(aioinject.Callable(A))
    container.register(aioinject.Callable(B))
    container.register(aioinject.Callable(C))

    n_rounds = 1
    n = 1_000_000
    sum_ = 0
    for _ in range(n_rounds):
        start = time.perf_counter()
        for _ in range(n):
            with container.sync_context() as ctx:
                ctx.resolve(C)
        diff = time.perf_counter() - start
        print(diff)
        sum_ += diff
    print(sum_)


main()
