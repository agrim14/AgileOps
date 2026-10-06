FROM public.ecr.aws/docker/library/python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
