# trabalho final da disciplina **Algoritmos e Programação de Computadores**, 2026.1

- dependências (`pip install pandas matplotlib`)
- nome dos arquivos de dados necessários
- nomes dos integrantes da dupla

Prof. Jorge Henrique Cabral Fernandes | jhcf@unb.br

## descrição do sistema
- Sistema de Exploração dos Microdados PDAD 2024 com Interface Gráfica
O sistema é um programa desenvolvido na linguagem Python, com a biblioteca tkinter para criação da interface gráfica.
descrição do sistema em 3–5 frases



**D1 — Segundo gráfico de tipo diferente**
Além do gráfico obrigatório, incluir um segundo gráfico de tipo distinto (ex: se o obrigatório é barras, o adicional pode ser histograma ou dispersão).

**D2 — Comparação entre duas RAs**
Permitir que o usuário selecione duas RAs e visualize uma comparação lado a lado no mesmo gráfico.

**D3 — Merge entre as duas tabelas**
Usar `pd.merge()` para cruzar a tabela de moradores com a de domicílios, produzindo alguma análise que exige dados das duas fontes (ex: escolaridade do responsável × infraestrutura do domicílio).

**D4 — Ordenação implementada à mão**
Para pelo menos uma lista exibida no sistema (ex: ranking de RAs por renda), implementar o algoritmo de ordenação manualmente (Bubble Sort, Selection Sort ou Insertion Sort) em vez de usar `.sort()` ou `.sort_values()` do pandas.

**D5 — Janela secundária com detalhes**
Ao clicar num item de uma lista ou barra do gráfico, abrir uma `tk.Toplevel` com informações detalhadas daquele item.

**D6 — Barra de progresso de carregamento**
Usar `ttk.Progressbar` para indicar visualmente o carregamento dos arquivos, que pode ser lento para os arquivos completos (~25 mil linhas).




## Estrutura do repositório

```
pdad-explorer/
├── sistema.py        ← arquivo principal, interface com usuário
├── utils/
│   ├── carregar.py        ← funções de leitura e limpeza dos dados
│   ├── calcular.py        ← funções de estatística e ordenação
│   └── exportar.py        ← função de exportação para arquivo
├── dados/
│   ├── moradores_parcial.csv        ← arquivo de teste local
│   └── domicilios_parcial.xlsx        ← arquivo de teste local
├── README.md
└── requirements.txt        ← listagem das bibliotecas das quais o programa depende (dependências), instaláveis via `pip install`
```






#### dados
- os arquivos completos do PDAD são muito grandes, o que gera lentidão no carregamento, por isso para desenvolvomento foram incluídos neste repositório apenas arquivos com dados parciais para teste
- pode-se fazer download dos arquivos completos em https://pdad.ipe.df.gov.br:
    - `PDAD_2024-Moradores.csv` — uma linha por morador (~25.000 registros)
    - `PDAD_2024-Domicilios.xlsx` — uma linha por domicílio
    - `Dicionario_de_variaveis_PDAD_2024.xlsx` — descrição de cada coluna








## como executar
- O programa deve ser executado com o comando `python sistema.py`. Uma janela principal abrirá, a partir da qual o usuário conseguirá explorar os dados.

#### contexto


- lógica de programação com JavaScript (Code.org Game Lab)
- Python: variáveis, tipos, estruturas de controle, funções, listas, dicionários
- pandas: leitura de CSV/Excel, filtragem, agrupamento, `value_counts`, `merge`
- tkinter: janelas, widgets, layout com `grid`, eventos, diálogos, gráficos com matplotlib
- microdados PDAD 2024: estrutura de duas tabelas relacionadas por `A01nficha`, dicionário de variáveis, valores sentinela (99999, 88888), blocos temáticos (domicílio, educação, saúde, trabalho, renda)

Este trabalho integra os conhecimentos adquiridos na disciplina em um **sistema com interface gráfica** que permite a uma pessoa explorar interativamente algum recorte da realidade social do Distrito Federal a partir dos dados do PDAD.








### Requisito 2 — Pelo menos um filtro interativo

O usuário deve poder filtrar os dados por pelo menos uma variável
- uma lista suspensa (`OptionMenu` ou `ttk.Combobox`) para selecionar RA ou categoria
- ou um campo de texto (`Entry`) para buscar valor específico
- os resultados da filtragem devem aparecer na mesma janela, sem abrir um novo arquivo

### Requisito 3 — Pelo menos uma visualização com matplotlib

O sistema deve gerar pelo menos um gráfico de barras, histograma ou gráfico de linhas embutido na janela tkinter. O gráfico deve mudar quando o usuário alterar o filtro.

### Requisito 4 — Exibição de estatísticas descritivas

o sistema deve calcular e exibir na janela:
- pelo menos três estatísticas numéricas relevantes (média, mediana, contagem, percentual ou similar)

### Requisito 5 — Diálogo de exportação

O usuário deve poder exportar os dados filtrados ou as estatísticas para um arquivo `.txt` ou `.csv`, usando `filedialog.asksaveasfilename` 










## Escolha do recorte temático

### Recorte D — Infraestrutura e condições dos domicílios

**Pergunta central:** como varia o acesso a infraestrutura (água, esgoto, internet, energia) entre as RAs?

Variáveis principais: blocos B e D da tabela de domicílios, `localidade`, `A01npessoas`

O sistema deve usar a tabela de domicílios como fonte principal, permitindo comparar indicadores de infraestrutura entre RAs e visualizar a relação entre tamanho do domicílio e tipo de imóvel.



---



## Dica de arquitetura

Uma estrutura que funciona bem para projetos desse tipo:

```python
import tkinter as tk
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")

# 1. Carregar dados ao iniciar
def carregar_dados():
    """Lê e limpa os arquivos PDAD; retorna dois DataFrames."""
    ...

# 2. Funções de análise (sem tkinter)
def calcular_distribuicao(df, variavel, filtro_ra=None):
    """Retorna contagem por categoria, com filtro opcional de RA."""
    ...

# 3. Funções de interface (chamam as de análise)
def atualizar_grafico():
    """Redesenha o gráfico com base nos filtros selecionados."""
    ...

# 4. Construir a janela
janela = tk.Tk()
moradores, domicilios = carregar_dados()
# ... montar widgets ...
janela.mainloop()
```
