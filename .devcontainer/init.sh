#! /bin/bash

set -e

sudo apt update

# Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

uv tool install crewai
crewai install
