FROM python:3.9-slim
RUN adduser --system --no-create-home nonroot
LABEL maintainer="Zipstack Inc."
ENV UNSTRACT_ENTRYPOINT "python /app/src/main.py"

# Set the working directory in the container
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy the contents of your project directory into the container at /app
COPY src /app/src/
WORKDIR /app/src

USER nonroot
ENTRYPOINT ["python", "main.py"]
