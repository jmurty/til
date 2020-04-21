# Install Python 3 tools with `pipx`

Use [pipx](https://github.com/pipxproject/pipx) to:

> install and run Python applications insolated environments.

In particular, it's a safe way to "globally" install and manage Python tools
that you don't want to pollute your system or project virtualenvs.

Install on MacOS:

    brew install pipx
    pipx ensurepath

WARNING: `pipx` only supports Python **3** tools, not version **2** tools.
Sometimes python2 tools seem to install okay with `pipx` but will fail with
strange errors when you run them (e.g. `thumbor`)
