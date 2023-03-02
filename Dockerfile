FROM python:3.9

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends vim
RUN apt-get install -y google-chrome-stable

COPY requirements_dep.txt requirements.txt

RUN pip install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.org --no-cache-dir -r requirements.txt

WORKDIR /app
CMD python run_app.py