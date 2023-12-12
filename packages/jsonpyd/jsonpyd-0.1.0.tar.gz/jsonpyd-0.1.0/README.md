<div align="center">
  <h2>jsonpyd</h2>
  <h3>Generate related pydantic class with any json type.</h3>
  <a href="https://github.com/sinantan/jsonpyd/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sinantan/jsonpyd"></a>
  <a href="https://github.com/sinantan/jsonpyd/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/sinantan/jsonpyd"></a>
  <a href="https://github.com/sinantan/jsonpyd/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/sinantan/jsonpyd"></a>
</div>

## Installation

_jsonpyd_ can be installed by running `pip install jsonpyd`

## Example Usage

Let's say you have a class like that;

```python
class M:
    qux = "blue"

    def __init__(self):
        self.bar = 55
        self.foo = 89
        self.baz = 121
```

To watch the changes, you need the add the `@pys()` as a class decorator.
