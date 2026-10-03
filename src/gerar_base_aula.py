"""Gera a base reduzida usada no notebook de aula (notebooks/enem2023_aula.ipynb).

Parte de enem2023.parquet (gerado por converter_parquet.py, na pasta MQ_DADOS) e mantém só as colunas
usadas em aula, sem NU_INSCRICAO. Todos os 3.933.955 inscritos ficam na base (inclusive
os faltosos), porque o viés de seleção pela presença é tema do Módulo 4.

O arquivo de saída (enem2023_aula.parquet, na mesma pasta) é publicado como anexo de uma
Release do GitHub para os alunos rodarem o notebook no Colab. Não versionar no repositório.

Uso: uv run --env-file .env python src/gerar_base_aula.py  (caminhos em src/caminhos.py)
"""
import duckdb

from caminhos import DADOS

ORIGEM = DADOS / "enem2023.parquet"
SAIDA = DADOS / "enem2023_aula.parquet"

COLUNAS = [
    # participante
    "TP_FAIXA_ETARIA", "TP_SEXO", "TP_COR_RACA", "TP_ST_CONCLUSAO", "TP_ESCOLA", "IN_TREINEIRO",
    # escola (só concluintes de 2023)
    "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
    # local da prova
    "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA",
    # presença e notas
    "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT",
    "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT",
    "TP_STATUS_REDACAO", "NU_NOTA_REDACAO",
    # questionário: escolaridade do pai e da mãe, moradores, renda
    "Q001", "Q002", "Q005", "Q006",
]

con = duckdb.connect()
con.execute(f"""
    COPY (SELECT {', '.join(COLUNAS)} FROM '{ORIGEM.as_posix()}')
    TO '{SAIDA.as_posix()}' (FORMAT parquet, COMPRESSION zstd)
""")
n = con.sql(f"SELECT count(*) FROM '{SAIDA.as_posix()}'").fetchone()[0]
print(f"ok: {SAIDA} | {n:,} linhas | {len(COLUNAS)} colunas | {SAIDA.stat().st_size / 1e6:.1f} MB")
