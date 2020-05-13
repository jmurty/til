# Use multi-line text blocks with `inspect.cleandoc`

Python's triple-quoting (`"""`) mechanism makes it easy to express long blocks
of multi-line text, but if you indent the text content properly (as you should)
you end up with a lot of whitespace at the beginning of each line.

You can fix this with the built-in [inspect.cleandoc()][cleandoc] function that
left trims indented text blocks.


```python
# Define a multi-line text block
>>> x = ("""
...     Here is some text that I am
...     hoping can be cleaned up properly
...     by cleandoc:
...
...     - while keeping
...      - extra whitespace
...        like this
... """)

# The raw text has a lot of excess left padding
>>> print(x)

    Here is some text that I am
    hoping can be cleaned up properly
    by cleandoc:

    - while keeping
     - extra whitespace
       like this

# Use inspect.cleandoc() to clean it up
>>> import inspect
>>> print(inspect.cleandoc(x))
Here is some text that I am
hoping can be cleaned up properly
by cleandoc:

- while keeping
 - extra whitespace
   like this
```

Be careful though: `inspect.cleandoc()` also trims leading and trailing empty
lines.

[cleandoc]: https://docs.python.org/3/library/inspect.html#inspect.cleandoc
