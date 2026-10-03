"""Caminhos dos dados, lidos de variáveis de ambiente.

Os dados ficam fora do repositório. Defina as variáveis num arquivo .env na raiz
(modelo em .env.example; o .env não é versionado) e rode com:
    uv run --env-file .env python src/<script>.py

MQ_DADOS       pasta dos Parquets derivados (padrão: dados/ na raiz do projeto)
MQ_MICRODADOS  pasta dos microdados do INEP (a que contém DADOS/MICRODADOS_ENEM_2023.csv)
"""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = Path(os.environ.get("MQ_DADOS", RAIZ / "dados"))


def microdados() -> Path:
    if "MQ_MICRODADOS" not in os.environ:
        raise SystemExit("Defina MQ_MICRODADOS (veja .env.example) e rode com: uv run --env-file .env ...")
    return Path(os.environ["MQ_MICRODADOS"])
