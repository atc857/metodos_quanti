# Métodos Quantitativos com os microdados do ENEM 2023

Material da palestra *Metodologia científica: tópicos de análise quantitativa*, para gestores do CBMDF (CAEO). Uma análise só, do zero à regressão, com dados reais e, em cada etapa, o prompt para a IA, o código e a verificação independente.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/atc857/metodos_quanti/blob/main/notebooks/enem2023_analise_v12.ipynb)

## O problema

> Alunos de escola privada tiram **122 pontos a mais** em Matemática do que os de escola pública. **De que tamanho** é essa diferença, **com que segurança** podemos afirmá-la, e **quanto dela permanece** quando levamos em conta renda, sexo e cor/raça?

O notebook [`notebooks/enem2023_analise_v12.ipynb`](notebooks/enem2023_analise_v12.ipynb) responde a essa pergunta em sete partes, na mesma ordem dos slides:

| Parte | Pergunta |
|---|---|
| 1 | O problema e o método: de onde vem a manchete e como vamos checá-la (com IA, sob protocolo)? |
| 2 | Análise exploratória e limpeza: quem está na comparação, e quem ficou de fora? |
| 3 | Estatística descritiva: de que tamanho é a diferença, descrita com honestidade? |
| 4 | Probabilidade: como ler uma probabilidade, e quanto do que vemos pode ser acaso? |
| 5 | Amostragem: se só tivéssemos uma amostra, sorteada como, com que margem de erro, e de que tamanho? |
| 6 | Testes de hipóteses: a diferença é real, e importa? E entre as quatro dependências administrativas? |
| 7 | Regressão: quanto dos 122 pontos permanece com renda, sexo e cor/raça? E o relatório. |

Os dados são observacionais: tudo o que se mede é **associação**, não efeito.

## Como usar

Clique no botão **Abrir no Colab** acima e depois em *Ambiente de execução → Executar tudo*. O notebook baixa sozinho a base de dados da [Release `base-v1`](https://github.com/atc857/metodos_quanti/releases/tag/base-v1) (cerca de 55 MB) e roda inteiro em poucos minutos. Não é preciso instalar nada.

## Slides

[Análise Quantitativa CAEO-2026, v12 (PDF)](slides/Analise_Quantitativa_CAEO-2026_v12.pdf)

## Dados

Fonte: INEP, [Microdados do ENEM 2023](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). A base da palestra é uma versão reduzida: 25 colunas, todos os 3.933.955 inscritos, **sem o número de inscrição**. Consulte o dicionário de dados do INEP antes de usar qualquer coluna.

Os scripts em [`src/`](src/) registram como a base foi gerada a partir do CSV original do INEP (1,7 GB). Para refazê-la, com o [uv](https://docs.astral.sh/uv/) instalado e as variáveis `MQ_MICRODADOS` (pasta dos microdados) e `MQ_DADOS` (pasta de saída) definidas:

```
uv run --no-project --with duckdb python src/converter_parquet.py
uv run --no-project --with duckdb python src/gerar_base_aula.py
```

## Versão anterior

O material do curso completo (notebook dos Módulos 1 a 7, notebook do analista e slides v11) está preservado na tag [`curso-v1`](https://github.com/atc857/metodos_quanti/tree/curso-v1).

## Licença

Código sob a [licença MIT](LICENSE). Textos explicativos do notebook sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br). Os microdados são do INEP.
