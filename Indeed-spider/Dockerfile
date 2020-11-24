# Use latest Python runtime as a parent image
FROM python:3.8-slim


# Copy the requirements.txt into the container at /app
COPY requirements.txt ./

# pip install
RUN pip --no-cache-dir install -r requirements.txt

# Copy the current directory contents into the container
COPY . ./

# ENTRYPOINT allows us to specify the default executible
ENTRYPOINT ["python"]

# CMD sets default arguments to executable which may be overwritten when using docker run
CMD ["indeed_requests_bs4_to_DB.py"]


# gcloud builds submit --tag gcr.io/diesel-studio-282016/indeed-spider-on-gcp
# gcloud run deploy --image gcr.io/diesel-studio-282016/indeed-spider-on-gcp --platform managed

# docker build . --tag gcr.io/diesel-studio-282016/indeed-spider
# docker push gcr.io/diesel-studio-282016/indeed-spider
# PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} gcr.io/diesel-studio-282016/hello-world

