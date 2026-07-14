import zipfile
import pandas
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DADOS_DIR = BASE_DIR / "dados"

SENTINELAS = {99999, 88888}

def _carregar_ra_nomes():
    caminho_dicionario = DADOS_DIR / "dicionario_de_variaveis_pdada_2024_público.xlsx"
    df = pandas.read_excel(caminho_dicionario, sheet_name = "anexo_1")
    ra_nomes = {}

    for _, linha in df.iterrows():
        valor = linha["Valor"]
        descricao = linha["Descrição do valor"]
        if pandas.notna(valor) and pandas.notna(descricao):
            ra_nomes[int(valor)] = str(descricao)

    return ra_nomes

RA_NOMES = _carregar_ra_nomes()

# busca no dicionário apenas os indicadores usados na interface
def _carregar_indicadores():
    caminho_dicionario = DADOS_DIR / "dicionario_de_variaveis_pdada_2024_público.xlsx"
    df = pandas.read_excel(caminho_dicionario, sheet_name = "domicilios")
    
    mapeamento_nomes = {}
    mapeamento_descricoes = {}
    
    indicadores_config = [
        ("B13", "água CAESB"),
        ("B14", "saneamento CAESB"),
        ("C05_1_1", "internet banda larga fixa"),
        ("B15", "energia elétrica Neoenergia"),
    ]
    
    for codigo, nome_descritivo in indicadores_config:
        linha = df[df["Coluna"] == codigo]
        if not linha.empty:
            descricao = linha.iloc[0]["Descrição da coluna"]
            mapeamento_nomes[nome_descritivo] = codigo
            mapeamento_descricoes[codigo] = str(descricao)
    
    return mapeamento_nomes, mapeamento_descricoes

INDICADORES, INDICADORES_DESCRICOES = _carregar_indicadores()

TIPO_IMOVEL = {
    1: "Casa",
    2: "Apartamento",
    3: "Cômodo",
    4: "Outro",
}

ESCOLARIDADE = {
    1: "Sem instrução",
    2: "Fund. incompleto",
    3: "Fund. completo",
    4: "Médio incompleto",
    5: "Médio completo",
    6: "Superior incompleto",
    7: "Superior completo",
    8: "Pós-graduação",
}

def nome_ra(codigo):
    if codigo in (None, "", "Todas", "todas"):
        return "Todas as RAs"
    try:
        return RA_NOMES.get(int(codigo), f"RA-{codigo}")
    except (ValueError, TypeError):
        return str(codigo)

def remover_sentinelas(df, colunas):
    resultado = df.copy()
    for coluna in colunas:
        if coluna in resultado.columns:
            resultado = resultado[~resultado[coluna].isin(SENTINELAS)]
    return resultado

def carregar_moradores():
    zip_path = DADOS_DIR / "moradores.zip"
    csv_path = DADOS_DIR / "moradores.csv"

    if csv_path.exists():
        moradores = pandas.read_csv(
            csv_path,
            sep=";",
            decimal=",",
            encoding="utf-8-sig",
            low_memory=False,
        )
    elif zip_path.exists():
        with zipfile.ZipFile(zip_path) as arquivo_zip:
            nome_interno = arquivo_zip.namelist()[0]
            arquivo_zip.extract(nome_interno, DADOS_DIR)
            arquivo_extraido = DADOS_DIR / nome_interno
            arquivo_extraido.rename(csv_path)
        moradores = pandas.read_csv(
            csv_path,
            sep=";",
            decimal=",",
            encoding="utf-8-sig",
            low_memory=False,
        )
    else:
        raise FileNotFoundError(
            "Arquivo de moradores não encontrado em dados/moradores.csv ou dados/moradores.zip"
        )

    moradores = remover_sentinelas(moradores, ["idade_calculada", "escolaridade", "renda_ind"])
    return moradores

def carregar_domicilios():
    caminho_xlsx = DADOS_DIR / "domicilios.xlsx"

    if caminho_xlsx.exists():
        domicilios = pandas.read_excel(caminho_xlsx)
    else:
        raise FileNotFoundError("Arquivo domicilios.xlsx ou domicilios.csv não encontrado em dados/")

    # limpa colunas usadas nas estatísticas e nos gráficos da aplicação
    colunas_limpeza = ["A01npessoas", "B01", "B07", "B08", "D15", "D16_1"]
    domicilios = remover_sentinelas(domicilios, colunas_limpeza)
    return domicilios

def carregar_dados():
    moradores = carregar_moradores()
    domicilios = carregar_domicilios()
    return moradores, domicilios

# usa apenas a pessoa responsável pelo domicílio para relacionar perfil individual e infraestrutura
def cruzar_tabelas(moradores, domicilios):
    responsaveis = moradores[moradores["index"] == 1].copy()
    return pandas.merge(
        responsaveis,
        domicilios,
        on="A01nficha",
        suffixes=("_mor", "_dom"),
    )
