# letsrolld

## Development

1. [Install flox.](https://flox.dev/docs/install-flox/)

2. Activate flox environment.

```bash
flox activate
```

3. Install `python` dependencies not packaged for `nixos`, yet.

```bash
pdm install
```

4. Run the tests.

```bash
make test
```

5. Initialize an empty database.

```bash
make init_db
```

6. Run the web app.

```bash
make webapp
```
