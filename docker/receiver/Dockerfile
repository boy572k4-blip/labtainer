FROM labtainers/labtainer.base:latest

USER root

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-pil \
        openssh-server iputils-ping net-tools && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install Pillow --break-system-packages 2>/dev/null || pip3 install Pillow

RUN mkdir -p /home/ubuntu/steg_lab /var/run/sshd && \
    echo 'ubuntu:receiver123' | chpasswd && \
    sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    ssh-keygen -A

COPY steg_lab/ /home/ubuntu/steg_lab/
RUN chmod +x /home/ubuntu/steg_lab/*.py && \
    chown -R ubuntu:ubuntu /home/ubuntu/steg_lab

LABEL version="1.0"
LABEL base="labtainers/labtainer.base.latest"
