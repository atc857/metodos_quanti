# Métodos Quantitativos com os microdados do ENEM 2023

Notebook da disciplina de Métodos Quantitativos / Tópicos de Análise Quantitativa para gestores do CBMDF (CAEO/CAO). Cada parte acompanha um módulo da aula, com dados reais e o uso de IA com verificação.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/atc857/metodos_quanti/blob/main/notebooks/enem2023_aula.ipynb)

## O que tem no notebook

[`notebooks/enem2023_aula.ipynb`](notebooks/enem2023_aula.ipynb)

**Fio condutor:** quanto as notas do ENEM variam com a renda, o tipo de escola, o território, o sexo e a cor/raça? De que tamanho são essas diferenças, quem fica fora da medição, e com que segurança podemos afirmar, sem confundir associação com causa? Cada parte responde a um pedaço dessa pergunta; alguns exemplos ficam fora dela de propósito, para introduzir conceitos.

| Parte | Módulo | Assunto |
|---|---|---|
| 0 | 0 | Preparação, leitura da base, registro da execução, rótulos do dicionário, modelo de prompt para IA |
| 1 | 1–2 | Estatística descritiva e análise exploratória: perfil, nulos, zeros, base de análise, gráficos honestos, sexo e cor/raça |
| 2 | 3 | Probabilidade e distribuições: normal, Teorema Central do Limite, binomial, taxa de base |
| 3 | 4 | Amostragem e intervalos de confiança: planos amostrais, vieses, tamanho de amostra, bootstrap |
| 4 | 5 | Testes de hipóteses: t de Welch, ANOVA, qui-quadrado, tamanho do efeito |
| 5 | 6 | Correlação e regressão: resíduos, regressão múltipla, treino/teste, IDHM, quarteto de Anscombe |

## Como usar

**No Google Colab (recomendado):** clique no botão acima. O notebook baixa sozinho a base de dados da [Release `base-v1`](https://github.com/atc857/metodos_quanti/releases/tag/base-v1) (cerca de 55 MB) e roda inteiro em menos de um minuto.

**No seu computador:** instale o [uv](https://docs.astral.sh/uv/), baixe `enem2023_aula.parquet` da Release para a pasta `dados/` e rode:

```
uv sync
uv run jupyter lab
```

Para guardar a base em outra pasta, crie um arquivo `.env` a partir do `.env.example` e rode com `uv run --env-file .env jupyter lab`.

## Dados

Fonte: INEP, [Microdados do ENEM 2023](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). A base do curso é uma versão reduzida: 25 colunas, todos os 3.933.955 inscritos, **sem o número de inscrição**. Consulte o dicionário de dados do INEP antes de usar qualquer coluna.

Para regenerar a base a partir do CSV original (1,7 GB), defina `MQ_MICRODADOS` e `MQ_DADOS` no `.env` e rode:

```
uv run --env-file .env python src/converter_parquet.py
uv run --env-file .env python src/gerar_base_aula.py
```

`src/legado/` guarda scripts de uma primeira rodada de cálculos, mantidos só como histórico.

## Licença

Código sob a [licença MIT](LICENSE). Textos explicativos do notebook sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br). Os microdados são do INEP.
