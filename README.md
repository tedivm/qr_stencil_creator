# QR Stencil Creator

qr_stencil is a web service for generating QR codes in SVG format for the use of creating stencils with cutters or lasers. It is built using FastAPI and provides a robust API for QR code generation.


## Launching with Docker

You can launch the qr_stencil web service using Docker. Ensure you have Docker installed and running on your machine.

Build and run the Docker container:

```bash
docker-compose up --build
```

This will start the web service on port 80. You can access it at `http://localhost`.

## FastAPI Routes

### Root Route

The root route serves the static index.html file.

```http
GET /
```

### QR Code Generation Route

Generate a QR code in SVG format.

```http
GET /image.svg
```

#### Query Parameters

- `msg` (str): The message to encode in the QR code.
- `error_level` (int, optional): The error correction level (default is 15).
- `box_size` (int, optional): The size of each box in the QR code (default is 100).
- `border` (int, optional): The border size around the QR code (default is 0).
- `size_ratio` (float, optional): The size ratio of the QR code (default is 0.8).

Example request:

```http
GET /image.svg?msg=https://example.com&error_level=15&box_size=100&border=0&size_ratio=0.8
```

## Maintenance with Makefile

The Makefile provides various commands for setting up the development environment, running tests, and formatting code.

### Setup

Install dependencies and set up the virtual environment:

```bash
make install
```

### Testing

Run tests and check code coverage:

```bash
make tests
```

### Formatting

Automatically format the codebase:

```bash
make chores
```

### Rebuild Dependencies

Rebuild the dependency files:

```bash
make rebuild_dependencies
```

## License

This project is licensed under the MIT License.
