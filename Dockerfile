# Dockerfile for BlueMouse MCP Server
# Used by Smithery.ai for automatic containerization

# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirement files first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (if running in SSE mode, though StdIO is default)
EXPOSE 8000

# Default command to run the MCP server
# Smithery uses this as the entry point
CMD ["python", "server.py"]
