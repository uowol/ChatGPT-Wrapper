# Step 1: Use a lightweight Ubuntu base image
FROM ubuntu:22.04

# Step 2: Install dependencies
RUN apt-get update && apt-get install -y \
    # 라이브러리 설치
    curl \
    git \
    # 의존성 설치
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    ca-certificates

# Step 3: Install pyenv
RUN curl https://pyenv.run | bash

# Step 4: Configure environment variables for pyenv
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Step 5: Install Python 3.10 and set it as the local version for the project
RUN pyenv install 3.10.11 && pyenv global 3.10.11

# Step 6: Install Poetry (dependency and packaging tool)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Step 7: Set the working directory inside the container
WORKDIR /app

# Step 8: Copy the project files to the container
COPY pyproject.toml poetry.lock ./
COPY . ./

# Step 9: Link Poetry to Pyenv's Python version
RUN poetry env use $(pyenv which python)

# Step 10: Install dependencies using Poetry
RUN poetry install

# Step 11: Default command to run the application
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]