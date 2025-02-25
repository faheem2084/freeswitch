FROM debian:12

# Define build-time arguments
ARG USER
ARG TOKEN

# Use the build-time arguments as environment variables
ENV USER=${USER}
ENV TOKEN=${TOKEN}

# ENV USER=freeswitch-dev
# ENV TOKEN=pat_j2UPAAc8kRT2ZmkStZkEDUNr

# Install essential build tools and development libraries
RUN apt-get update && apt-get install -y gnupg2 wget lsb-release ca-certificates

# Update CA certificates
RUN update-ca-certificates

# Download the SignalWire repository key
RUN wget --http-user=${USER} --http-password=${TOKEN} -O /usr/share/keyrings/signalwire-freeswitch-repo.gpg https://freeswitch.signalwire.com/repo/deb/debian-release/signalwire-freeswitch-repo.gpg

# Configure APT authentication
RUN echo "machine freeswitch.signalwire.com login signalwire password $TOKEN" > /etc/apt/auth.conf && \
    chmod 600 /etc/apt/auth.conf

# Add SignalWire repository to APT sources
RUN echo "deb [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" > /etc/apt/sources.list.d/freeswitch.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" >> /etc/apt/sources.list.d/freeswitch.list

# Install FreeSWITCH
RUN apt-get update && apt-get install -y freeswitch-meta-all

# Cleanup to reduce Docker image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

COPY ./freeswitch.sh /freeswitch.sh
RUN chmod +x /freeswitch.sh

ENTRYPOINT ["/freeswitch.sh"]