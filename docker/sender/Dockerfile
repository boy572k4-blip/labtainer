FROM labtainers/labtainer.base:latest

USER root

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-pil \
        openssh-client iputils-ping net-tools && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install Pillow --break-system-packages 2>/dev/null || pip3 install Pillow

# Tạo sẵn cover image lúc build để không cần tạo lúc chạy
RUN mkdir -p /home/ubuntu/steg_lab
COPY steg_lab/ /home/ubuntu/steg_lab/
RUN chmod +x /home/ubuntu/steg_lab/*.py && \
    chown -R ubuntu:ubuntu /home/ubuntu/steg_lab && \
    python3 /home/ubuntu/steg_lab/generate_cover.py /home/ubuntu/steg_lab/cover_image.png

# SSH config để scp không hỏi fingerprint
RUN mkdir -p /home/ubuntu/.ssh && \
    echo "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile /dev/null\n    LogLevel ERROR" \
    > /home/ubuntu/.ssh/config && \
    chmod 600 /home/ubuntu/.ssh/config && \
    chown -R ubuntu:ubuntu /home/ubuntu/.ssh

LABEL version="1.0"
LABEL base="labtainers/labtainer.base.latest"
