<!--
    vim: nospell
-->

<!-- [![Documentation 
Status](https://readthedocs.org/projects/iterchain/badge/?version=latest)](https://iterchain.readthedocs.io/en/latest/?badge=latest) 
-->

# Chitter: my take on iterator chaining for Python

## Introduction

Chitter is a fork Evelyn H's 
[iterchain](https://github.com/Evelyn-H/iterchain.git) package, but made to be 
mine. Anyway, this package makes working with iterators in python more 
ergonomic by allowing you to chain methods on them (that's easier to read).

Similarly to Evelyn's this package's design is inspired by the [Rust 
iterators](https://doc.rust-lang.org/std/iter/index.html), stuff from python's 
own standard library 
([itertools](https://docs.python.org/3/library/itertools.html)).

## Installation

With Poetry:

    poetry add chitter

With Pip:

    pip install chitter

For the development version:

    git clone https://github.com/brunofauth/chitter.git
    cd ./chitter/
    poetry install

***Everything below this line comes straight from `iterchain`'s docs, so keep that in mind while reading...***

## Why would I need this?

Say we want to know the sum of all the squares of even numbers up to 100.  
How can we do this?

Let's try some straightforward, procedural Python:
```python
>>> total = 0
>>> for i in range(100):
...     if i % 2 is 0:
...         total += i ** 2
...
>>> total
161700
```

This works, but if you read this for the first time it can take a bit of effort 
to figure out what's happening, especially in slightly less trivial cases.
So, how about we use iterators instead?

Well, let's see:
```python
>>> sum(i**2 for i in range(100) if i % 2 is 0)
161700
```

That's pretty nice! Much shorter, and much easier to understand.  But there's a 
problem, this pattern only works for relatively simple manipulations. In those 
cases you could try using the python `map` and `filter` builtins (and the 
slightly more hidden `functools.reduce`). They let you construct more complex 
processing chains.

Let's rewrite our iterator to use those functions instead:
```python
>>> sum(map(lambda x: x**2, filter(lambda x: x % 2 is 0, range(100))))
161700
```

Okay, now _that_ is a mess...  I don't know about you, but it would take me 
quite a while to unravel what's happening here. The problem is that the whole 
expression is inside out. The `filter` gets applied first, but it's hidden in 
the middle of the expression, and the `sum` gets applied last but it is all the 
way in the front. Makes no sense...

So, how can we improve on this? `iterchain` of course!  
(you probably saw this coming already)

So, let's see how it looks using `iterchain`:
```python
>>> import iterchain
>>> (iterchain.count(stop=100)
...     .filter(lambda x: x % 2 is 0)
...     .map(lambda x: x**2)
...     .sum())
161700
```

Isn't this much better? The operations are listed in the order that they're 
executed, are clearly separated, and you can have as few or as many operations 
as you want. This is why you should use `iterchain`!


## Generators

`iterchain` also provides handy methods that let you build new `Iterator` 
instances from scratch. These are contained in the `iterchain.generators` 
sub-module, but they're also accessible directly from the `iterchain` module, 
which is the preferred way of using them.

For example:
```
  >>> import iterchain
  >>> iterchain.count().take(4).map(lambda x: x**2).to_list()
  [0, 1, 4, 9]
```
