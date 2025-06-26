# py-rpp

## Generate models from RPP XSD

```sh
xsdata generate xsd/epp-1.0.xsd --package rpp.model.epp
xsdata generate xsd/domain-1.0.xsd --package rpp.model.epp
xsdata generate xsd/contact-1.0.xsd --package rpp.model.epp
xsdata generate xsd/secDNS-1.1.xsd --package rpp.model.epp
```

## Running test server

Activate the virtual environment and run the FastAPI server:

```sh
. ./.venv/bin/activate
export rpp_host=...
# epp username
export rpp_epp_client_id=...
# epp password
export rpp_epp_password=...
```

Or use a .env file to set the environment variables, .env.example is provided as a template.

Then run the FastAPI server:

```sh
fastapi dev main.py
```
