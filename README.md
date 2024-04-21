# letsrolld

## Development

1. [Install flox.](https://flox.dev/docs/install-flox/)

2. Build flox environment.

```bash
flox build
```

3. Activate flox environment.

```bash
flox activate
```

4. Install dependencies not packaged for `nixos`, yet.

```bash
make install
```

5. Run the tests.

```bash
make test
```

6. Initialize an empty database.

```bash
make init_db
```

7. Populate the database with test data. This will initialize the database with
   10 directors and their films, by default.

```bash
make populate
```

8. Run the web app.

```bash
make webapp
```

At this point, the web app should be running at `http://localhost:8000`. You
can access the API schema at `http://localhost:8000/api/doc/swagger.json`.
