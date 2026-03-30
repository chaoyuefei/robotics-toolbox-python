# Development Setup

This guide covers setting up a local development environment using [uv](https://docs.astral.sh/uv/).

## Prerequisites

- Python 3.9+ (3.11 recommended)
- [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A C/C++ compiler (Xcode Command Line Tools on macOS, `build-essential` on Linux)

## Setup

### 1. Create a virtual environment

```bash
uv venv --python 3.11
source .venv/bin/activate
```

### 2. Install dependencies and build C extensions

The project includes C/C++ extensions (`frne`, `fknm`) that require NumPy headers at build time. Use `--no-build-isolation` so the build can find the installed NumPy:

```bash
uv pip install setuptools numpy
uv pip install -e ".[dev]" --no-build-isolation
```

### 3. Rebuild dependencies with NumPy 2.x (if needed)

Some dependencies (`spatialgeometry`, `swift-sim`) publish wheels compiled against NumPy 1.x. If you see `_ARRAY_API not found` or `numpy.core.multiarray failed to import`, rebuild them from source:

```bash
uv cache clean spatialgeometry swift-sim
uv pip install spatialgeometry --force-reinstall --no-binary spatialgeometry --no-build-isolation
uv pip install swift-sim --force-reinstall --no-binary swift-sim --no-build-isolation
```

### 4. Install collision support (optional)

Collision checking requires PyBullet, which may not build on all platforms:

```bash
uv pip install pybullet
```

## Running Tests

Always use the venv Python to avoid picking up system Python:

```bash
.venv/bin/python -m pytest tests
```

Or if the venv is activated:

```bash
pytest tests
```

## Common Issues

### `ModuleNotFoundError: No module named 'roboticstoolbox.fknm'`

The C extensions were not compiled. Reinstall with:

```bash
uv pip install setuptools numpy
uv pip install -e "." --no-build-isolation
```

### `_ARRAY_API not found` / `numpy.core.multiarray failed to import`

A dependency was compiled against a different NumPy major version. Rebuild it from source (see step 3 above).

### Tests use wrong Python version

If `pytest` picks up your system Python instead of the venv, use:

```bash
.venv/bin/python -m pytest tests
```

This can happen when conda or another environment manager shadows the venv activation.
