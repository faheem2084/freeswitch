# Use a slim Debian image
FROM debian:12-slim

# Define build-time arguments
ARG USER
ARG TOKEN

# Use the build-time arguments as environment variables
ENV USER=${USER}
ENV TOKEN=${TOKEN}

# Install essential build tools and development libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    wget \
    lsb-release \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download the SignalWire repository key
RUN wget --http-user=${USER} --http-password=${TOKEN} -O /usr/share/keyrings/signalwire-freeswitch-repo.gpg https://freeswitch.signalwire.com/repo/deb/debian-release/signalwire-freeswitch-repo.gpg

# Configure APT authentication
RUN echo "machine freeswitch.signalwire.com login signalwire password $TOKEN" > /etc/apt/auth.conf && \
    chmod 600 /etc/apt/auth.conf

# Add SignalWire repository to APT sources
RUN echo "deb [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" > /etc/apt/sources.list.d/freeswitch.list && \
    echo "deb-src [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" >> /etc/apt/sources.list.d/freeswitch.list

# Install FreeSWITCH and clean up in one RUN command
RUN apt-get update && apt-get install -y --no-install-recommends \
    freeswitch-meta-all && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and set permissions for the startup script
COPY ./freeswitch.sh /freeswitch.sh
RUN chmod +x /freeswitch.sh

# Set the entrypoint
ENTRYPOINT ["/freeswitch.sh"]