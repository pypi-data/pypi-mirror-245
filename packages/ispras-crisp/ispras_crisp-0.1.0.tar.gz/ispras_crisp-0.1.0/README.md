# crisp

Coding Rules at ISP

Read the docs (in Russian) [here](docs/source/index.rst).

## Why this exists

* I'm tired of typing `ruff check <something>` **and** `black <something>` **and**
checking I'm in the right directory.
* I need a simple way to enforce a uniform coding style in many projects. Just install
this package and enjoy a carefully crafted set of coding rules being applied
automatically.
* I hate accidentially fixing somebody else's linting errors in my own commits so this
tool sees only files **you** have modified. Faster than checking the entire codebase
once again as well.
