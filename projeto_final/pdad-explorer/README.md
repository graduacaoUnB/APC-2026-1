# trabalho final da disciplina **Algoritmos e Programação de Computadores**, 2026.1

Marcos Torres, matrícula 261048383

Professor Jorge Henrique Cabral Fernandes | jhcf@unb.br

## descrição do sistema
### Sistema de Exploração dos Microdados PDAD 2024 com Interface Gráfica
Este trabalho integra os conhecimentos adquiridos na disciplina em um **sistema desenvolvido na linguagem Python com interface gráfica criada com a biblioteca Tkinter**. Entre outros, este projeto exige conhecimentos em:
- lógica de programação
- Python (variáveis, tipos, estruturas de controle, funções, listas, dicionários)
- Pandas (leitura de arquivos, filtragem, agrupamento, `value_counts`, `merge`)
- Tkinter (janelas, widgets, layout com `grid`, eventos, diálogos, gráficos com matplotlib)

O sistema permite a uma pessoa explorar interativamente um recorte temático (especificamente o recorte **Infraestrutura e Condições dos Domicílios**) da realidade social do Distrito Federal a partir dos dados da Pesquisa Distrital por Amostra de Domicílios (PDAD), permitindo comparação de indicadores de infraestrutura entre RAs, e visualização da relação entre tamanho do domicílio e tipo de imóvel. A **pergunta central** à qual este programa busca auxiliar a responder é: como varia o acesso a infraestrutura (água, esgoto, internet, energia) entre as regiões administrativas (RAs)?

## dados
Este sistema usa microdados do PDAD 2024:
- 2 tabelas: uma tabela com dados de domicílios, e outra com dados de moradores
    - arquivo `domicilios.xlsx`, com uma linha para cada domicílio
        - é a fonte de dados principal
        - variáveis principais: colunas `localidade`, `A01npessoas`, bloco B (`B01` a `B20`), e bloco D (`D15` a `D16_5`)
    - arquivo `moradores.csv` (compactado), com uma linha para cada morador (~25.000 registros)
- as 2 tabelas se relacionam pelo campo `A01nficha`
- as tabelas possuem "blocos temáticos" (domicílio, educação, saúde, trabalho, renda)
- as colunas possuem "valores sentinela" (99999, 88888), que significam dados inaplicáveis ou não declarados, que serão filtrados das análises
- há ainda o arquivo `dicionario_de_variaveis_pdada_2024_público.xlsx`, um dicionário de variáveis, com descrição de cada coluna
- os arquivos completos do PDAD são muito grandes, o que gera lentidão no carregamento; por isso para desenvolvimento foram incluídos neste repositório apenas arquivos com dados parciais para teste
- pode-se fazer download dos arquivos completos em https://pdad.ipe.df.gov.br -> Resultados -> Microdados:
    - Base de morador
    - Base de domicílios
    - Dicionário de dados

## Estrutura do repositório

```
pdad-explorer/
├── sistema.py        ← arquivo principal, interface com usuário
├── utils/
│   ├── carregar.py        ← funções de leitura e limpeza dos dados
│   ├── calcular.py        ← funções de estatística e ordenação
│   └── exportar.py        ← função de exportação para arquivo
├── dados/
│   ├── moradores.zip        ← arquivo compactado de teste local
│   └── domicilios.xlsx        ← arquivo de teste local
├── README.md
└── requirements.txt        ← listagem das bibliotecas das quais o programa depende (dependências), instaláveis via `pip install`
```

## como executar
- se não estiverem instaladas, executar `pip install -r .\requirements.txt` para instalar dependências
- o programa deve ser executado com o comando `python sistema.py`. Uma janela principal abrirá, a partir da qual o usuário conseguirá explorar os dados.
