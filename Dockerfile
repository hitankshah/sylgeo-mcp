FROM python:3.10-slim

WORKDIR /app

# Copy configuration files
COPY pyproject.toml README.md ./

# Copy source code first
COPY src/ ./src/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# Set the entry point to execute the MCP server
ENTRYPOINT ["python", "-m", "sylgeo_mcp.server"]
