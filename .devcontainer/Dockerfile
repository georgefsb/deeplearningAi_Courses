FROM python:3.11-slim

# Instala dependências do sistema que evitam erros em pacotes nativos
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /workspace

# Copia o requirements para instalar dependências
COPY requirements.txt ./

# Instala CrewAI e demais dependências caso existam
RUN pip install --upgrade pip \
    && pip install crewai crewai-tools langchain openai \
    && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Define Python como shell padrão
SHELL ["/bin/bash", "-c"]