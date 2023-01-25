FROM qmcgaw/godevcontainer:debian

ARG DEBIAN_FRONTEND="noninteractive"

# Install Docker CE CLI
RUN apt-get update \
  && apt-get install -y apt-transport-https ca-certificates curl gnupg2 lsb-release \
  && curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | apt-key add - 2>/dev/null \
  && echo "deb [arch=amd64] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list \
  && apt-get update \
  && apt-get install -y docker-ce-cli

# Install Docker Compose
RUN export LATEST_COMPOSE_VERSION=$(curl -sSL "https://api.github.com/repos/docker/compose/releases/latest" | grep -o -P '(?<="tag_name": ").+(?=")') \
  && curl -sSL "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose

RUN apt-get update
RUN apt-get install -y \
    curl \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    gnupg2 \
    openssh-client \
    gcc \
    g++ \
    sqlite3 \
    gh \
    zip \
    unzip \
    gnupg \
    software-properties-common

RUN apt-get update && apt-get install -y protobuf-compiler

# RUN gh extension install nektos/gh-act
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install

COPY library-scripts/*.sh /tmp/library-scripts/
ARG TERRAFORM_VERSION=1.2.0
ARG TFLINT_VERSION=0.44.1
ARG TERRAGRUNT_VERSION=0.43.0
RUN bash /tmp/library-scripts/terraform-debian.sh "${TERRAFORM_VERSION}" "${TFLINT_VERSION}" "${TERRAGRUNT_VERSION}" "${TERRAFORM_DOCS_VERSION}"

RUN git clone https://github.com/pyenv/pyenv.git /opt/pyenv
ENV PYENV_ROOT="/opt/pyenv"
ENV PATH="/opt/pyenv/shims:/opt/pyenv/bin:$PATH"
ENV PYENV_SHELL="bash"
RUN pyenv install 3.8.12
RUN pyenv global 3.8.12

RUN curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n
RUN bash n 16
RUN pip install poetry==1.2.0b3
RUN mkdir -p /root/workspace/
