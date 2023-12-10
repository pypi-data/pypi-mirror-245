"""
Usage example:

    from chitter import ChainableIter

    result: tuple[int, ...] = (
        ChainableIter(range(100))
            .map(lambda item: 2 * item)
            .filter(lambda item: item % 4 == 0)
            .cycle()
            .take(100)
            .collect(tuple)
    )

    print(result)
"""

# simplify public interface
from .core import ChainableIter
