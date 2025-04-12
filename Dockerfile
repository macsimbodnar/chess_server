FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.12.2
ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

# Install pip and adduser
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    adduser \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install --break-system-packages -r requirements.txt

# Create app user
RUN adduser --system --group $USER

# Set up app directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME

USER $USER
