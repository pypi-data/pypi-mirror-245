FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04 AS base_image_stage

FROM base_image_stage AS custom_software_stage

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get upgrade -y && \
    apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget \
                       curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
                       libglib2.0-dev python3-dev
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime

FROM custom_software_stage AS pyenv_stage

USER vscode
RUN curl https://pyenv.run | bash 
RUN echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc 