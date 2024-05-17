# letsrolld

## Development

1. [Install flox.](https://flox.dev/docs/install-flox/)

2. Activate flox environment.

```bash
flox activate
```

3. Install dependencies not packaged for `nixos`, yet.

```bash
make install
```

4. Run the tests.

```bash
make test
```

5. Initialize an empty database.

```bash
make init_db
```

6. Populate the database with test data. This will initialize the database with
   10 directors and their films, by default.

```bash
make populate
make run-all
```

7. Run the web backend.

```bash
make webapp
```

At this point, the backend should be running at `http://localhost:8000`. You
can access the API schema at `http://localhost:8000/api/doc/swagger.json`.


8. Open Web UI.

```bash
make ui
```

This should open your browser with the frontend.
