# py-rpp

**py-rpp** is a Python-based RPP (RESTful Provisioning Protocol) to EPP (Extensible Provisioning Protocol) adapter intended for RPP-EPP compatibility testing. It converts RPP requests to EPP requests, and transforms EPP responses back into RPP responses. This allows systems using RPP to communicate seamlessly with EPP-based registries.

Currently, py-rpp is tightly bound to the EPP data model. In future versions, this will change as we begin developing a dedicated RPP data model. This will improve flexibility and better reflect the RPP protocol

## How to Use

You can run easily using Docker. Once running, you can use the RPP API by sending HTTP requests to the server (see the OpenAPI docs at `/docs`).  
**Note:**

- The API requires HTTP Basic Auth to log in, use your EPP server credentials.
- Configure the connection details for your backend EPP server in the `config.yaml` file before
- The EPP server MUST have support for TLS connections, as the RPP server will always use TLS to connect to the EPP server.

**Example:**
This example uses Curl, but any HTTP client can be used to interact with the RPP API. Make sure to replace `<username>` and `<password>` with your actual EPP credentials and make sure the contacts used in the request exist in the EPP server:

Request to create a new domain using RPP:

```sh
curl -X POST "http://localhost:8000/domains/" \
  -u "<username>:<password>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-domain-mw-123.nl",
    "authInfo": {
        "value": "XYZ12345"
    },
    "registrant": "MAK005714-X2627",
    "contact": [
        {
            "type": "admin",
            "value": "MAK005713-X2627"
        },
        {
            "type": "tech",
            "value": "MAK005712-X2627"
        }
    ]
}'
```

Response:

```json
{
    "@type": "Domain",
    "result": [
        {
            "code": 1000,
            "message": "The domain name has been registered.",
            "lang": "en"
        }
    ],
    "trID": {
        "clTRID": "trfefd043199558da0",
        "svTRID": "48554516"
    },
    "resData": {
        "name": "test-domain-mw-123.nl",
        "creDate": "2025-07-08T13:41:16Z"
    }
}
```

## API Endpoints

See the [OpenAPI documentation](http://localhost:8000/docs) for a complete list of available endpoints, requires server running on localhost.

## OpenAPI JSON Schema

See the [OpenAPI JSON schema](http://localhost:8000/openapi.json) for the API specification, requires server running on localhost.

## Running with Docker

You can build and run the RPP server using the provided `Dockerfile` and `docker-compose.yaml`.

### Build the Docker image

From the project root directory, run:

```sh
docker build -t py-rpp:latest .
```

### Run with Docker Compose

Start the container using Docker Compose (the container will be built automatically if it doesn't exist yet):

```sh
docker-compose up
```

### Examples

See the `examples` directory for example requests. You can use tools like `curl` or Postman to test the API endpoints.

This will build (if needed) and start the `py-rpp` container, exposing the server on port 8000 (as configured in `docker-compose.yaml`).

### Configuration

The container uses `/app/config.yaml` for configuration, which is mounted from your local directory.
You can set environment variables in the `docker-compose.yaml` file or by editing `config.yaml`.
The `rpp_epp_host` variable should point to the EPP server you want to connect to.

### Stopping the server

To stop the server, press `Ctrl+C` or run:

```sh
docker-compose down
```

## Development Setup

To set up a development environment for py-rpp, follow these steps:

- Clone the repository:

```sh
git clone https://github.com/SIDN/py-rpp.git
cd py-rpp
```

- Create a virtual environment:

```sh
python3 -m venv .venv
```

- Activate the virtual environment:

```sh
. ./.venv/bin/activate
```

- Install the required dependencies:

```sh
pip install -r requirements.txt
```

- Create a configuration file: `config.yaml`, a `config.yaml.example` is provided as a template.
- Edit `config.yaml` to set the connection details for your EPP server.

- Start the server using FastAPI's development server:

```sh
fastapi dev main.py
```

- The server will be available at `http://localhost:8000`. You can access the OpenAPI documentation at `http://localhost:8000/docs`.
