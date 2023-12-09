# JosiauhTools
#### Table of Contents

- [Examples](#examples)
    - [Simply Then](#simply-then)

Some python general tools. 
```
pip install josiauhtools
```

# Examples
Here's what you can do with JosiauhTools!

## Simply Then
Explanation:

TL;DR: Prints "i got", and the result of running "foo" (bar)

<details>
<summary>Will read</summary>
Runs a function called "foo", which will return "bar".
After that, it runs "bar", which will print "i got bar", where bar was retrieved from "foo".
</details>




Code: 
```py
from josiauhtools import synx

def foo():
    return 'bar'

def bar(p):
    print("i got " + p)

synx.then(foo, bar)
```