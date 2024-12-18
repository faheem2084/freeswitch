FROM debian:12

ENV USER=********
ENV TOKEN=******
# Install essential build tools and development libraries

RUN apt-get update && apt-get install -y gnupg2 wget lsb-release

RUN wget --http-user=${USER} --http-password=${TOKEN} -O /usr/share/keyrings/signalwire-freeswitch-repo.gpg https://freeswitch.signalwire.com/repo/deb/debian-release/signalwire-freeswitch-repo.gpg

RUN echo "machine freeswitch.signalwire.com login signalwire password $TOKEN" > /etc/apt/auth.conf
RUN chmod 600 /etc/apt/auth.conf
RUN echo "deb [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" > /etc/apt/sources.list.d/freeswitch.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/signalwire-freeswitch-repo.gpg] https://freeswitch.signalwire.com/repo/deb/debian-release/ `lsb_release -sc` main" >> /etc/apt/sources.list.d/freeswitch.list

# you may want to populate /etc/freeswitch at this point.
# if /etc/freeswitch does not exist, the standard vanilla configuration is deployed
RUN apt-get update && apt-get install -y freeswitch-meta-all

# Cleanup to reduce Docker image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

COPY ./freeswitch.sh /freeswitch.sh
RUN chmod +x /freeswitch.sh

# Expose ports
# EXPOSE 5060/udp 
# EXPOSE 5060/tcp
# EXPOSE 5080/udp
# EXPOSE 16384-32768:16384-32768/udp 
# EXPOSE 7443/tcp

ENTRYPOINT ["/freeswitch.sh"]
# ENTRYPOINT ["ping google.com"]