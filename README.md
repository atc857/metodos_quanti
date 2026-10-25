# Métodos Quantitativos com os microdados do ENEM 2023

Notebook da disciplina de Métodos Quantitativos / Tópicos de Análise Quantitativa para gestores do CBMDF (CAEO/CAO). Cada parte acompanha um módulo da aula, com dados reais e, em cada etapa, o prompt para a IA, os comandos que ele produz e a verificação independente.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/atc857/metodos_quanti/blob/main/notebooks/enem2023_curso.ipynb)

## O que tem no notebook

[`notebooks/enem2023_curso.ipynb`](notebooks/enem2023_curso.ipynb)

**Fio condutor:** quanto as notas do ENEM variam com a renda, o tipo de escola, o território, o sexo e a cor/raça? De que tamanho são essas diferenças, quem fica fora da medição, e com que segurança podemos afirmar, sem confundir associação com causa? Cada parte responde a um pedaço dessa pergunta; alguns exemplos ficam fora dela de propósito, para introduzir conceitos.

| Módulo | Assunto |
|---|---|
| 1 | A base do ENEM 2023 e como se chegou à base reduzida; protocolo de IA |
| 2 | Análise exploratória e limpeza: nulos, a armadilha da escola, zeros, base de análise |
| 3 | Estatística descritiva: Matemática por tipo de escola, sexo e cor/raça, gráfico honesto |
| 4 | Probabilidade: condicional e taxa de base, binomial, normal, Teorema Central do Limite |
| 5 | Amostragem: erro padrão, intervalo de confiança, tamanho da amostra, vieses |
| 6 | Testes de hipóteses, um por seção, do planejamento ao relato: t de Welch, ANOVA e Tukey, qui-quadrado |
| 7 | Correlação e regressão: resíduos, quarteto de Anscombe, regressão múltipla |

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
