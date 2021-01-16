#https://github.com/dimmg/dockselpy/blob/master/Dockerfile
#docker run --privileged -e FILE_NAME="main.py" --name selenium -p 4000:4000 -d -it selenium_docker
#docker run --privileged -v $(pwd):/usr/src/app --name selenium -p 4000:4000 -d -it selenium_docker
#docker run --privileged -v $(pwd):/usr/src/app --name selenium --network="host" -d -it selenium_docker
#docker start selenium && docker exec -it selenium python3 main.py && docker stop selenium
#docker build -t selenium_docker .
#docker build -t selenium_docker:vers2 .
#docker run --name selenium02 -d -v csbet:/usr/src/app/data --network=mynet selenium_docker:vers2

FROM ubuntu:bionic

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb


# install chromedriver and google-chrome

RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    apt-get install libgbm1 -y && \
    rm chromedriver_linux64.zip

RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP


RUN pip3 install selenium && \
    pip3 install pyvirtualdisplay &&\
    pip3 install redis && \
    pip3 install peewee && \
    pip3 install fake-useragent

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /script
ENV BASE_DIR ${APP_HOME}
WORKDIR $APP_HOME

COPY ./app ${APP_HOME}

#CMD tail -f /dev/null
CMD python3 main.py
#CMD ["python3", "/usr/src/app/main.py"]
