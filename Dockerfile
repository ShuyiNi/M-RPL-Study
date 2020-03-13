FROM i386/ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# Install basic packages
RUN apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
      build-essential \
      clang-format \
      git \
      python3 \
      python3-pip \
      xauth \
      python3-tk \
      python3-matplotlib \
      > /dev/null && \
    apt-get clean -qq
RUN pip3 install -q \
      black \
      pandas

# Prepare for Cooja
RUN apt-get install -qq -y --no-install-recommends \
      ant \
      openjdk-8-jdk \
      > /dev/null && \
    apt-get -qq clean
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-i386
RUN update-java-alternatives -s java-1.8.0-openjdk-i386

# Set up user
RUN adduser user
USER user
ENV HOME /home/user

# Set up work environment
WORKDIR ${HOME}/work
ENV PATH ${HOME}/work/bin:${PATH}
CMD bash --login
