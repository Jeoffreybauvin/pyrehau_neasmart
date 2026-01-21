FROM python:3.14-slim

WORKDIR /app

COPY . .

# Install the package in editable mode
RUN pip install -e .

CMD ["tail", "-f", "/dev/null"]
