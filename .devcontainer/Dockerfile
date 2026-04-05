FROM debian:bookworm-slim

SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# Install UV (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# Install NVM and Node.js (latest)
ENV NVM_DIR=/usr/local/nvm
RUN mkdir -p "$NVM_DIR" \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash \
    && source "$NVM_DIR/nvm.sh" \
    && nvm install node \
    && nvm alias default node \
    && nvm cache clear

# Symlink node binaries so they are available in non-interactive shells
RUN LATEST_NODE="$(ls "$NVM_DIR/versions/node" | sort -V | tail -1)" \
    && ln -sf "$NVM_DIR/versions/node/$LATEST_NODE/bin/node" /usr/local/bin/node \
    && ln -sf "$NVM_DIR/versions/node/$LATEST_NODE/bin/npm"  /usr/local/bin/npm \
    && ln -sf "$NVM_DIR/versions/node/$LATEST_NODE/bin/npx"  /usr/local/bin/npx

# Make NVM available in interactive shells (system-wide)
RUN printf 'export NVM_DIR="/usr/local/nvm"\n[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"\n[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"\n' \
    > /etc/profile.d/nvm.sh \
    && chmod +x /etc/profile.d/nvm.sh

# Create non-root developer user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid "$USER_GID" "$USERNAME" \
    && useradd --uid "$USER_UID" --gid "$USER_GID" -m -s /bin/bash "$USERNAME" \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/$USERNAME" \
    && chmod 0440 "/etc/sudoers.d/$USERNAME" \
    && cat /etc/profile.d/nvm.sh >> "/home/$USERNAME/.bashrc"

USER $USERNAME
