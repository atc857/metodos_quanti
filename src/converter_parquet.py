"""Converte os microdados do ENEM 2023 (CSV latin-1, ';') em Parquet, sem as colunas de vetores de respostas.

Uso: uv run --env-file .env python src/converter_parquet.py  (caminhos em src/caminhos.py)
"""
import duckdb

from caminhos import DADOS, microdados

CSV = microdados() / "DADOS" / "MICRODADOS_ENEM_2023.csv"
SAIDA = DADOS / "enem2023.parquet"

con = duckdb.connect()
con.execute(f"""
    COPY (
        SELECT * EXCLUDE (TX_RESPOSTAS_CN, TX_RESPOSTAS_CH, TX_RESPOSTAS_LC, TX_RESPOSTAS_MT,
                          TX_GABARITO_CN, TX_GABARITO_CH, TX_GABARITO_LC, TX_GABARITO_MT)
        FROM read_csv('{CSV.as_posix()}', delim=';', encoding='latin-1', header=true, sample_size=-1)
    ) TO '{SAIDA.as_posix()}' (FORMAT parquet, COMPRESSION zstd)
""")
print("ok", SAIDA, SAIDA.stat().st_size / 1e6, "MB")
