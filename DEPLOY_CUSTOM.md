# Deploy the custom CRM build

This repository contains three build branches in addition to `main`:

- `app-frappe` — the customised Frappe Framework
- `app-crm` — the customised CRM application
- `app-voice-crm` — the Voice CRM application

The `apps.json` file installs the two applications. Frappe itself is selected
with the two build arguments below. A deployment must build this custom image;
running a stock Frappe image or the disposable `pwd.yml` demo will show the
default CRM instead.

## Build

From the root of a fresh clone of `main`:

```sh
docker build \
  --build-arg FRAPPE_PATH=https://github.com/CaucaMyTan/frappe-saas-web.git \
  --build-arg FRAPPE_BRANCH=app-frappe \
  --secret id=apps_json,src=apps.json \
  --tag cauca-frappe-saas:custom \
  --file images/custom/Containerfile .
```

If the repository is private, give the builder read-only GitHub access through
a deploy key or a BuildKit secret. Do not put a GitHub token in `apps.json`, a
Dockerfile, or `.env`.

## Run the custom image

Set these values in the deployment environment file used by Compose:

```dotenv
CUSTOM_IMAGE=cauca-frappe-saas
CUSTOM_TAG=custom
PULL_POLICY=never
```

Start the usual production Compose stack with its selected database, Redis,
and HTTPS overrides. For an existing site, run the migration after switching
the stack to the custom image:

```sh
docker compose exec backend bench --site <your-site-name> migrate
```

Build and test the image in staging before replacing a production image. Site
databases, site configuration, backups, logs, virtual environments, and
secrets are intentionally not stored in this repository.
