# Django CRUD App for Generic Risk Models

### Setup *.env* file to define environment variables (You only need to set in `DEBUG=True` on local env)
  - `DEBUG` (default=False)
  - `DATABASE_URL` (default=sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
  - `STATIC_S3_ENABLED` (default=False)
    - Allow static content to be served from AWS S3
  - `SITE_USES_SSL` (default=False)
    - Set to True in production if using SSL

  - Example `.env` file might look like this
    ```
      DEBUG=True
    ```

### Bootstraping dev environment

These steps will install all required dependencies including development ones, run migrations and start dev server.

```bash
make dev
make migrate
make run
```

### Run tests
```bash
make test
```

### Deployment

These steps will install production dependencies and build vue.js application to `static/dist` folder.

```bash
make prod
make build
```

After deployment step you can choose zappa to deploy app to AWS Lambda.

```
zappa deploy <project-name>
```

If using zappa fill in `AWS S3 Bucket` name in `zappa_settings.json`
