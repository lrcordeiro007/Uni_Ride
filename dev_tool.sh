#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem cor

echo -e "${BLUE}=== UniRide Dev Tool ===${NC}"

# Verifica se está na raiz do projeto
if [ ! -d "backend" ]; then
    echo -e "${RED}Erro: Execute este script na raiz do projeto (onde a pasta /backend está).${NC}"
    exit 1
fi

show_help() {
    echo "Uso: ./dev_tool.sh [comando]"
    echo ""
    echo "Comandos:"
    echo "  setup          Instala dependências e cria arquivos .env"
    echo "  db-reset       Apaga e recria o banco de DESENVOLVIMENTO"
    echo "  db-test-setup  Cria o banco de TESTES manualmente"
    echo "  run            Inicia o servidor em modo DEV (.env.dev)"
    echo "  test           Inicia o servidor em modo TESTE (.env.test)"
    echo "  clean          Remove cache e arquivos temporários"
}

case "$1" in
    setup)
        echo -e "${GREEN}[1/3] Criando ambiente virtual...${NC}"
        python3 -m venv .venv
        echo -e "${GREEN}[2/3] Instalando dependências...${NC}"
        source .venv/bin/activate && pip install -r requirements.txt
        echo -e "${GREEN}[3/3] Criando ficheiros .env...${NC}"
        [ ! -f .env.dev ] && cp .env.example .env.dev
        [ ! -f .env.test ] && cp .env.example .env.test
        echo "Setup concluído!"
        ;;

    db-reset)
        echo -e "${RED}Resetar banco de DESENVOLVIMENTO (Carona_DB)? (s/n)${NC}"
        read -r confirm
        if [ "$confirm" = "s" ]; then
            sudo -u postgres psql -c "DROP DATABASE IF EXISTS \"Carona_DB\";"
            sudo -u postgres psql -c "CREATE DATABASE \"Carona_DB\";"
            echo -e "${GREEN}Banco de Dev resetado!${NC}"
        fi
        ;;

    db-test-setup)
        echo -e "${YELLOW}A criar banco de TESTES (Carona_Test_DB)...${NC}"
        sudo -u postgres psql -c "CREATE DATABASE \"Carona_Test_DB\";"
        echo -e "${GREEN}Banco de Testes pronto!${NC}"
        ;;

    run)
        echo -e "${GREEN}A iniciar ambiente de DESENVOLVIMENTO...${NC}"
        export APP_ENV=dev
        source .venv/bin/activate
        uvicorn main:app --reload --app-dir backend
        ;;

    test)
        echo -e "${YELLOW}A iniciar ambiente de TESTE (.env.test)...${NC}"
        # Define a variável que o seu database.py usa para escolher o ficheiro .env
        export APP_ENV=test
        source .venv/bin/activate
        # Roda o servidor apontando para o banco de testes
        uvicorn main:app --reload --app-dir backend
        ;;

    clean)
        echo -e "${BLUE}Limpando cache...${NC}"
        find . -type d -name "__pycache__" -exec rm -rf {} +
        find . -type f -name "*.pyc" -delete
        echo "Limpeza concluída."
        ;;

    *)
        show_help
        ;;
esac

if [ ! -d "backend" ]; then
    echo "Erro: Execute este script na raiz do projeto UniRide."
    exit 1
fi