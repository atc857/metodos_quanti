# CLAUDE.md — Métodos Quantitativos (CBMDF)

Repositório público com o código do curso de **Métodos Quantitativos / Tópicos de Análise Quantitativa** para gestores do CBMDF (CAEO/CAO): o notebook que os alunos usam e os scripts que preparam a base. O material de preparação das aulas (conteúdo por módulo, livros, slides) e os dados ficam **fora do repositório**; caminhos e fases do projeto estão no `CLAUDE.local.md` (não versionado), quando existir.

**Fio condutor:** *quanto as notas do ENEM variam com a renda, o tipo de escola, o território, o sexo e a cor/raça? De que tamanho são essas diferenças, quem fica fora da medição, e com que segurança podemos afirmar, sem confundir associação com causa?* Cada módulo responde a um pedaço dessa pergunta (tabela na seção 5.0 do `ROTEIRO_ESTUDOS.md`). Exemplos fora do fio (moeda, binomial dos militares, MT ~ CN, treineiros, Anscombe) são mantidos de propósito, para introduzir conceitos. Cor/raça é autodeclarada; recortes por cor/raça só em nível nacional ou de grandes grupos.

**Decisão de projeto:** não há módulo separado de IA. A IA é integrada em **todos** os módulos, com os **prompts** e as **boas práticas** para resultados precisos e com validade científica. O protocolo de 7 regras está no Módulo 0 (Parte 0 do notebook).

## Público e tom

- Gestores, não estatísticos: priorizar interpretação, decisão e erros comuns em vez de dedução matemática.
- Idioma: **português do Brasil** em tudo (texto, comentários, rótulos de gráficos, nomes de arquivos).
- Nunca inventar dados, citações, normas ou funcionalidades de ferramentas de IA. Na dúvida, verificar em fonte primária ou perguntar. Citações atribuídas sem fonte primária (ex.: Deming) devem ser marcadas como "atribuída".
- Pronomes: usar "o instrutor"; evitar inferir gênero de terceiros.

## Estrutura

```
metodos_quanti/
├── README.md / LICENSE                 # página do repositório para os alunos (MIT; textos CC BY 4.0)
├── CLAUDE.md                           # este arquivo (público)
├── .env.example                        # modelo do .env (caminhos dos dados; o .env não é versionado)
├── pyproject.toml / uv.lock            # ambiente uv
├── notebooks/enem2023_aula.ipynb       # notebook do curso (Partes 0–5 = Módulos 0–6); fonte dos números
└── src/
    ├── caminhos.py                     # lê MQ_DADOS e MQ_MICRODADOS do ambiente
    ├── converter_parquet.py            # CSV do INEP → enem2023.parquet
    ├── gerar_base_aula.py              # → enem2023_aula.parquet (base reduzida do notebook)
    └── legado/                         # 1ª rodada de cálculos (outra base); só histórico
```

Ignorados pelo git: `.venv/`, `.env`, `CLAUDE.local.md`, `dados/`, `saida/` (figuras geradas pelo notebook), e qualquer `*.parquet`, `*.csv`, `*.pdf`, `*.pptx`.

**Notebook:** **um único notebook** com uma parte por módulo. Para regenerar números e figuras: `uv run --env-file .env jupyter nbconvert --to notebook --execute --inplace notebooks/enem2023_aula.ipynb` (~45 s). O notebook não importa nada de `src/`, para rodar sozinho no Colab.

**Onde o notebook acha a base:** `MQ_DADOS/enem2023_aula.parquet` (variável de ambiente) → `dados/enem2023_aula.parquet` na raiz → `URL_BASE` (anexo da Release `base-v1` do GitHub, usado no Colab). Ao regenerar a base, publicar de novo o anexo da Release.

## Dados: microdados do ENEM 2023

Fonte: INEP, <https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem>. O pacote do INEP (1,7 GB; pasta indicada em `MQ_MICRODADOS`) tem `DADOS\MICRODADOS_ENEM_2023.csv` (3.933.955 linhas, 76 colunas), `DADOS\ITENS_PROVA_2023.csv` (5.550 linhas, parâmetros TRI), o dicionário (`DICIONÁRIO\Dicionário_Microdados_Enem_2023.xlsx`) e a documentação técnica.

**Formato:** CSV com separador `;`, codificação **ISO-8859-1 (latin-1)**.

**Parquet derivado:** `enem2023.parquet` (107 MB, `src/converter_parquet.py`, sem as colunas `TX_RESPOSTAS_*` e `TX_GABARITO_*`), na pasta `MQ_DADOS`. Consultar com DuckDB (segundos).

**Base reduzida da aula:** `enem2023_aula.parquet` (55 MB, `src/gerar_base_aula.py`): 25 colunas, todos os 3.933.955 inscritos, sem `NU_INSCRICAO`. É o que o notebook lê.

**Base de análise do curso** (notebook 1.6), usada nos Módulos 3–6: presentes nas 4 provas objetivas, `TP_STATUS_REDACAO == 1` e nenhuma prova objetiva com nota 0 → **2.569.190 participantes** (65,3% dos inscritos); MT: μ = 540,60, σ = 124,91. Análises de presença usam todos os inscritos.

**Regras de manuseio**
- **Nunca commitar o CSV nem os Parquets.** A base reduzida vai só como anexo de Release.
- Não ler o CSV inteiro com `pd.read_csv` direto; usar DuckDB/Polars ou o Parquet.
- Consultar o **dicionário** antes de usar qualquer coluna. Não deduzir significado de códigos pelo nome.

**Colunas principais**
- Participante: `TP_FAIXA_ETARIA`, `TP_SEXO` (M/F), `TP_ESTADO_CIVIL`, `TP_COR_RACA`, `TP_NACIONALIDADE`, `TP_ST_CONCLUSAO`, `TP_ESCOLA`, `TP_ENSINO`, `IN_TREINEIRO`.
- Escola: `TP_DEPENDENCIA_ADM_ESC` (1 federal, 2 estadual, 3 municipal, 4 privada), `TP_LOCALIZACAO_ESC`, `SG_UF_ESC`, `CO_MUNICIPIO_ESC`.
- Prova: `SG_UF_PROVA`, `TP_PRESENCA_CN/CH/LC/MT` (0 faltou, 1 presente, 2 eliminado), `TP_LINGUA`, `TP_STATUS_REDACAO` (1 = sem problemas).
- Notas: `NU_NOTA_CN/CH/LC/MT/REDACAO`, `NU_NOTA_COMP1..5`.
- Questionário: `Q001`–`Q025`. `Q006` = renda familiar, **ordinal com 17 faixas (A–Q)**; `Q005` = nº de moradores.
- `ITENS_PROVA_2023.csv`: `CO_ITEM`, `SG_AREA`, `TX_GABARITO`, `NU_PARAM_A/B/C` (TRI).

**Armadilhas já confirmadas nos dados (usar em aula)**
- Nota é **vazia** exatamente para quem não esteve presente (nota MT preenchida = 2.692.427 = presentes). Filtrar `TP_PRESENCA_* == 1`.
- **`TP_ESCOLA` só é respondida por concluintes de 2023** (`TP_ST_CONCLUSAO == 2`); 64,4% constam como "1 = Não respondeu". `TP_DEPENDENCIA_ADM_ESC` tem o mesmo recorte (24,4% da base).
- Zeros: 117.829 redações com 0, todas com `TP_STATUS_REDACAO ≠ 1` (zero administrativo). Nas objetivas (16.638 em MT, 16.547 em CN, 5.612 em CH, 2.169 em LC), **100% são cartões sem nenhuma resposta marcada** (conferido em `TX_RESPOSTAS_*` no CSV); não há notas entre 0 e ≈ 290. Redação em múltiplos de 20.
- **Os microdados de 2023 não têm `CO_ESCOLA`** (o ENEM 2024 das turmas anteriores tinha).
- A presença cresce com a renda (58,5% na faixa A a ≈ 84% nas altas): viés de seleção. Varia também por cor/raça (73,6% brancos, 62,5% pretos, 58,8% indígenas) e é igual entre os sexos.
- **Sexo muda de sinal conforme a prova:** homens +46,5 em MT, mulheres +36,4 na redação (notebook 1.12). **Cor/raça:** brancos × pretos em MT, d = 0,63; com renda, escola e sexo na regressão, a diferença cai de −73 para −35 pontos (notebook 5.4). η² em MT: renda 23,1%, cor/raça 7,0%, sexo 3,3%.
- **Simpson real:** na base de análise, treineiros têm média de MT maior no agregado (549,4 × 538,5) e menor em todas as faixas etárias (notebook 3.8).
- Com n em milhões, qualquer teste dá "significativo": reportar **tamanho de efeito** e IC, e ler o IC contra a margem de relevância. Federais × privadas em LC: d = 0,15 (abaixo do relevante), mas 91% das amostras de n = 1.000 dão p < 0,05.
- `pingouin.ttest` reporta `power` calculado com o d observado (poder *post hoc*); não usar. Planejar n com `statsmodels` (`TTestIndPower`).
- Privacidade: `NU_INSCRICAO` é uma máscara; evitar recortes que reidentifiquem pessoas (município pequeno × cor × escola).

## Ambiente técnico

- Usar **`uv`**: `uv run --env-file .env python src/<script>.py`. O ambiente tem pandas, pyarrow, duckdb, scipy, statsmodels, scikit-learn, matplotlib, seaborn, jupyter, nbconvert. Para ler o dicionário `.xlsx`, acrescentar `--with openpyxl`.
- No `.env`, usar aspas simples nos caminhos do Windows (barras invertidas e espaços ficam literais).
- Para o CSV completo, preferir DuckDB; o Parquet lê em segundos.

## Convenções de trabalho

- **Reprodutibilidade:** todo número ou gráfico mostrado em aula sai do notebook (ou de `src/`), com semente fixa (`np.random.default_rng(2023)`). Células novas inseridas no meio do notebook não devem usar `rng` (isso mudaria todos os sorteios seguintes); se precisarem sortear, usam um gerador próprio (`np.random.default_rng(SEMENTE)`). Para não renumerar, acrescentar seções no fim da parte (ex.: 1.11, 1.12, 2.4). Números fora do notebook (ex.: parâmetro c da TRI, verificação dos cartões em branco) são marcados como consulta avulsa.
- **IA no notebook:** todo prompt mostrado deve ter (a) contexto e restrições explícitos, (b) pedido de código e não de números, (c) pedido de premissas e limitações, (d) a **verificação independente** que o analista faz depois. Não afirmar capacidades de produtos de IA sem fonte primária; a referência de prompting usada é a documentação da Anthropic.
- **Gráficos:** títulos que dizem a conclusão, eixos rotulados com unidade, sem 3D nem eixos truncados. Paleta consistente; usar a skill `dataviz`.
- **Antes de commitar:** conferir `git status`; nada de dados, PDFs, `.env` ou caminhos pessoais em saídas do notebook.
