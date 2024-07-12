FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y libgl1
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
# Copy entrypoint.sh
COPY entrypoint.sh /usr/src/entrypoint.sh
RUN chmod +x /usr/src/entrypoint.sh

COPY . /usr/src/app
# Run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]