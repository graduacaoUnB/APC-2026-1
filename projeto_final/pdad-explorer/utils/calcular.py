import utils.carregar

def filtrar_por_ra(df, ra_codigo, coluna_localidade="localidade"):
    if ra_codigo in (None, "", "todas", "Todas"):
        return df.copy()
    return df[df[coluna_localidade] == int(ra_codigo)].copy()

def percentual_com_acesso(df, coluna_indicador):
    if df.empty or coluna_indicador not in df.columns:
        return 0.0

    # só considera respostas válidas: 1 (com acesso), e 2 (sem acesso)
    validos = df[df[coluna_indicador].isin([1, 2])]
    if validos.empty:
        return 0.0

    com_acesso = (validos[coluna_indicador] == 1).sum()
    return 100.0 * com_acesso / len(validos)

def estatisticas_domicilios(df, coluna_indicador):
    if df.empty:
        return {
            "contagem": 0,
            "media_moradores": 0.0,
            "mediana_moradores": 0.0,
            "percentual_acesso": 0.0,
        }

    moradores = df["A01npessoas"].tolist()
    moradores_ordenados = sorted(moradores)
    meio = len(moradores_ordenados) // 2

    if len(moradores_ordenados) % 2 == 0:
        mediana = (
            moradores_ordenados[meio - 1] + moradores_ordenados[meio]
        ) / 2
    else:
        mediana = moradores_ordenados[meio]

    return {
        "contagem": len(df),
        "media_moradores": sum(moradores) / len(moradores),
        "mediana_moradores": mediana,
        "percentual_acesso": percentual_com_acesso(df, coluna_indicador),
    }

def distribuicao_por_ra(df, coluna_indicador):
    if df.empty:
        return []

    # agrupa por RA para contar quantos domicílios válidos existem e quantos têm acesso
    agrupado = {}
    for _, linha in df.iterrows():
        codigo = int(linha["localidade"])
        valor = linha[coluna_indicador]
        if valor not in (1, 2):
            continue

        if codigo not in agrupado:
            agrupado[codigo] = {"total": 0, "com_acesso": 0}

        agrupado[codigo]["total"] += 1
        if valor == 1:
            agrupado[codigo]["com_acesso"] += 1

    resultado = []
    for codigo, dados in agrupado.items():
        percentual = 0.0
        if dados["total"] > 0:
            percentual = 100.0 * dados["com_acesso"] / dados["total"]
        resultado.append(
            {
                "codigo": codigo,
                "nome": utils.carregar.nome_ra(codigo),
                "percentual": percentual,
                "total": dados["total"],
                "com_acesso": dados["com_acesso"],
            }
        )

    return insertion_sort_por_percentual(resultado)

def insertion_sort_por_percentual(lista):
    ordenada = lista[:]
    for i in range(1, len(ordenada)):
        chave = ordenada[i]
        j = i - 1
        while j >= 0 and ordenada[j]["percentual"] < chave["percentual"]:
            ordenada[j + 1] = ordenada[j]
            j -= 1
        ordenada[j + 1] = chave
    return ordenada

def comparar_duas_ras(df, ra1, ra2, coluna_indicador):
    filtro1 = filtrar_por_ra(df, ra1)
    filtro2 = filtrar_por_ra(df, ra2)
    return {
        "ra1": {
            "codigo": int(ra1),
            "nome": utils.carregar.nome_ra(ra1),
            "percentual": percentual_com_acesso(filtro1, coluna_indicador),
            "contagem": len(filtro1),
        },
        "ra2": {
            "codigo": int(ra2),
            "nome": utils.carregar.nome_ra(ra2),
            "percentual": percentual_com_acesso(filtro2, coluna_indicador),
            "contagem": len(filtro2),
        },
    }

def distribuicao_tamanho_por_tipo(df):
    if df.empty:
        return {}, []

    dados = {}
    for _, linha in df.iterrows():
        tipo = int(linha["B01"])
        pessoas = int(linha["A01npessoas"])
        nome_tipo = utils.carregar.TIPO_IMOVEL.get(tipo, f"tipo {tipo}")
        dados.setdefault(nome_tipo, []).append(pessoas)

    tipos_ordenados = sorted(dados.keys())
    return dados, tipos_ordenados

def analise_escolaridade_infraestrutura(df_cruzado, coluna_indicador):
    if df_cruzado.empty:
        return []

    # o nome da coluna de localidade muda após o merge
    coluna_local = "localidade_dom" if "localidade_dom" in df_cruzado.columns else "localidade"
    resultado = []

    for nivel, nome in utils.carregar.ESCOLARIDADE.items():
        filtro = df_cruzado[df_cruzado["escolaridade"] == nivel]
        if filtro.empty:
            continue

        resultado.append(
            {
                "escolaridade": nome,
                "contagem": len(filtro),
                "percentual_acesso": percentual_com_acesso(filtro, coluna_indicador),
            }
        )

    return resultado

def detalhes_ra(df, codigo_ra, coluna_indicador):
    filtro = filtrar_por_ra(df, codigo_ra)
    stats = estatisticas_domicilios(filtro, coluna_indicador)
    indicador_descricao = utils.carregar.INDICADORES_DESCRICOES.get(coluna_indicador, coluna_indicador)

    tipos = {}
    for _, linha in filtro.iterrows():
        tipo = utils.carregar.TIPO_IMOVEL.get(int(linha["B01"]), "outro")
        tipos[tipo] = tipos.get(tipo, 0) + 1

    return {
        "nome": utils.carregar.nome_ra(codigo_ra),
        "codigo": int(codigo_ra),
        "indicador": indicador_descricao,
        "stats": stats,
        "tipos_imovel": tipos,
    }
