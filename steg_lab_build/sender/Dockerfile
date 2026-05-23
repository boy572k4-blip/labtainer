FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-client \
    openssh-server \
    iputils-ping \
    net-tools \
    nano \
    vim \
    sshpass \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pillow

# Configure SSH server
RUN mkdir -p /var/run/sshd && \
    echo 'root:labtainer' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Configure SSH client (no host-key prompts in lab)
RUN mkdir -p /root/.ssh && \
    printf 'Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile /dev/null\n    LogLevel ERROR\n' \
    > /root/.ssh/config && chmod 600 /root/.ssh/config

# Create lab directory & copy scripts
RUN mkdir -p /root/steg_lab
COPY scripts/lsb_embed.py            /root/steg_lab/lsb_embed.py
COPY scripts/chi_square_test.py      /root/steg_lab/chi_square_test.py
COPY scripts/generate_cover_image.py /root/steg_lab/generate_cover_image.py
RUN chmod +x /root/steg_lab/*.py

# Generate the cover image at build time
RUN python3 /root/steg_lab/generate_cover_image.py

# Hostname
RUN echo "sender" > /etc/hostname

# Welcome banner
RUN printf '#!/bin/bash\necho ""\necho "================================================"\necho "  T-STEG01: LSB Steganography Lab - SENDER"\necho "================================================"\necho "  Directory: ~/steg_lab/"\necho "  Scripts  : lsb_embed.py  chi_square_test.py"\necho "  Cover    : ~/steg_lab/cover_image.png"\necho "  Receiver : receiver@172.21.0.30"\necho "================================================"\necho ""\n' \
    > /root/.bashrc_lab && \
    echo 'source /root/.bashrc_lab' >> /root/.bashrc

EXPOSE 22
CMD ["/bin/bash", "-c", "service ssh start && /bin/bash"]
