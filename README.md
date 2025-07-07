# py-rpp

## API Endpoints

See the [OpenAPI documentation](http://localhost:8000/docs) for a complete list of available endpoints.

## Running with Docker

You can build and run the RPP server using the provided `Dockerfile` and `docker-compose.yaml`.

### Build the Docker image

From the project root directory, run:

```sh
docker build -t sidnlabs/py-rpp:latest .
```

### Run with Docker Compose

Start the container using Docker Compose:

```sh
docker-compose up
```

This will build (if needed) and start the `py-rpp` container, exposing the server on port 8001 (as configured in `docker-compose.yaml`).

### Configuration

- The container uses `/app/config.yaml` for configuration, which is mounted from your local directory.
- You can set environment variables in the `docker-compose.yaml` file or by editing `config.yaml`.

### Stopping the server

To stop the server, press `Ctrl+C` or run:

```sh
docker-compose down
```

## Development Setup

### Generate models from RPP XSD

This only needs to be done once, or when the XSD files change.

```sh
. ./.venv/bin/activate

xsdata generate xsd/epp-1.0.xsd --package rpp.model.epp
xsdata generate xsd/domain-1.0.xsd --package rpp.model.epp
xsdata generate xsd/contact-1.0.xsd --package rpp.model.epp
xsdata generate xsd/secDNS-1.1.xsd --package rpp.model.epp
xsdata generate xsd/rgp-1.0.xsd --package rpp.model.epp
```

### Running test server

Activate the virtual environment and run the FastAPI server:

```sh
. ./.venv/bin/activate
```

Set the configuration variables in `config.yaml`, a `config.yaml.example` is provided as a template.

Then run the FastAPI server:

```sh
fastapi dev main.py
```
