FROM python:3.9-slim
#Replace with your own email or company name
LABEL maintainer="Zipstack Inc."
ENV UNSTRACT_ENTRYPOINT "python /app/src/main.py"

# Set the working directory in the container
WORKDIR /app
# Copy the contents of your project directory into the container at /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/src
ENTRYPOINT ["python", "main.py"]
