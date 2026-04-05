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
# Install UV
# -------------------------

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# -------------------------
# Install NVM
# -------------------------

# https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-in-docker
ENV BASH_ENV=/root/.bash_env
RUN touch "${BASH_ENV}"
RUN echo '. "${BASH_ENV}"' >> ~/.bashrc

# Download and install nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | PROFILE="${BASH_ENV}" bash
RUN echo node > .nvmrc
RUN nvm install


# -------------------------
# Finalize user setup
# -------------------------

# Create non-root developer user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV NVM_DIR=/root/.nvm

RUN groupadd --gid "$USER_GID" "$USERNAME" \
    && useradd --uid "$USER_UID" --gid "$USER_GID" -m -s /bin/bash "$USERNAME" \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/$USERNAME" \
    && chmod 0440 "/etc/sudoers.d/$USERNAME" \
    && cat "${BASH_ENV}" >> "/home/$USERNAME/.bashrc"

USER $USERNAME
