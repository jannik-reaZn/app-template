FROM debian:bookworm-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# --------------------------
# Install system dependencies
# --------------------------

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        sudo \
    && rm -rf /var/lib/apt/lists/*



# -------------------------
# Finalize user setup
# -------------------------

# Create non-root developer user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid "$USER_GID" "$USERNAME" \
    && useradd --uid "$USER_UID" --gid "$USER_GID" -m -s /bin/bash "$USERNAME" \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/$USERNAME" \
    && chmod 0440 "/etc/sudoers.d/$USERNAME"

USER $USERNAME

# -------------------------
# Install UV (as vscode user)
# -------------------------

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
ADD --chown=$USERNAME https://astral.sh/uv/install.sh /tmp/uv-installer.sh
RUN sh /tmp/uv-installer.sh && rm /tmp/uv-installer.sh
ENV PATH="/home/${USERNAME}/.local/bin:$PATH"

# -------------------------
# Install NVM (as vscode user)
# -------------------------

# https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-in-docker
ENV NVM_DIR=/home/${USERNAME}/.nvm
WORKDIR /home/${USERNAME}
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash \
    && . "${NVM_DIR}/nvm.sh" \
    && nvm install node \
    && nvm use node \
    && nvm alias default node
ENV PATH="${NVM_DIR}/versions/node/$(ls ${NVM_DIR}/versions/node | tail -1)/bin:${PATH}"
