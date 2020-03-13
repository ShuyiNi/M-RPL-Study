FROM i386/ubuntu:18.04

ENV LANG C.UTF-8

# Install basic packages
RUN apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
      build-essential \
      clang-format \
      git \
      xauth \
      > /dev/null && \
    apt-get clean -qq

# Install Java environment for Cooja
RUN apt-get install -qq -y --no-install-recommends \
      ant \
      openjdk-8-jdk \
      > /dev/null && \
    apt-get -qq clean
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-i386
RUN update-java-alternatives -s java-1.8.0-openjdk-i386

# Install Python and Python packages
RUN apt-get install -qq -y --no-install-recommends \
      libfreetype6-dev \
      libpng-dev \
      python3 \
      python3-dev \
      python3-pip \
      python3-setuptools \
      > /dev/null && \
    apt-get clean -qq
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

# Set up user
RUN useradd -ms /bin/bash user
USER user
ENV HOME /home/user

# Set up work environment
WORKDIR ${HOME}/work
ENV PATH ${HOME}/work/bin:${PATH}

CMD bash --login
