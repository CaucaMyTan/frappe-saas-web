# Run the custom CRM demo locally

This creates a **new local demo site** with the custom Frappe Framework, CRM,
and Voice CRM code in this repository. It does not copy another user's CRM
data, passwords, files, or site configuration.

## Requirements

1. Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Install Git.
3. If this GitHub repository is private, add the person as a repository
   collaborator before they clone it.

## Start

```sh
git clone https://github.com/CaucaMyTan/frappe-saas-web.git
cd frappe-saas-web
bash demo/start-local.sh
```

The initial run downloads Docker images, builds frontend assets, creates the
database, and installs the custom apps. It can take several minutes. Open
<http://demo.localhost:8000> when it finishes, then sign in with:

- User: `Administrator`
- Password: `admin`

This account is for a local demo only. Change the password before putting any
real data in the system.

## Stop or reset

Stop the demo without deleting its data:

```sh
docker compose -f .devcontainer/docker-compose.yml down
```

To discard the local demo completely, delete the cloned repository and remove
the Docker volume named `frappe-saas-web_mariadb-data` (the exact volume name
can differ by folder name).

## Why this uses custom branches

The main branch is the deployment repository. The three app branches provide
the app source at each branch root so Frappe Bench can install it correctly:

- `app-frappe`
- `app-crm`
- `app-voice-crm`

Running the stock `pwd.yml` demo or an official CRM image skips these branches
and therefore shows the default CRM UI.
