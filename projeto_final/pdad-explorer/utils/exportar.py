import utils.calcular
import utils.carregar


def exportar_para_arquivo(caminho, df_filtrado, coluna_indicador, ra_selecionada=None):
    stats = utils.calcular.estatisticas_domicilios(df_filtrado, coluna_indicador)
    indicador = utils.carregar.INDICADORES_DESCRICOES.get(coluna_indicador, coluna_indicador)
    ra_texto = "Todas" if ra_selecionada in (None, "", "Todas") else utils.carregar.nome_ra(ra_selecionada)

    if caminho.endswith(".csv"):
        colunas = [
            "A01nficha",
            "localidade",
            "A01npessoas",
            "B01",
            coluna_indicador,
        ]
        colunas_existentes = [c for c in colunas if c in df_filtrado.columns]
        df_filtrado[colunas_existentes].to_csv(caminho, index=False, encoding="utf-8-sig")
        return

    linhas = [
        "mini relatório Infraestrutura de Domicílios, PDAD 2024",
        "Marcos Torres, matrícula 261048383",
        "disciplina APC 2026/1, Prof. Dr. José Carlos de Souza Júnior",
        "",
        f"RA selecionada: {ra_texto}",
        f"Indicador: {indicador}",
        "",
        f"Total de domicílios: {stats['contagem']}",
        f"Média de moradores: {stats['media_moradores']:.2f}",
        f"Mediana de moradores: {stats['mediana_moradores']:.2f}",
        f"Percentual com acesso: {stats['percentual_acesso']:.1f}%",
        "",
        "Compilação de dados por tipo de imóvel:",
    ]

    # Compile data by dwelling type
    tipos_imovel = df_filtrado["B01"].unique()
    for tipo_codigo in sorted(tipos_imovel):
        tipo_nome = utils.carregar.TIPO_IMOVEL.get(int(tipo_codigo), f"tipo {tipo_codigo}")
        df_tipo = df_filtrado[df_filtrado["B01"] == tipo_codigo]
        
        total_tipo = len(df_tipo)
        com_acesso_tipo = (df_tipo[coluna_indicador] == 1).sum()
        sem_acesso_tipo = (df_tipo[coluna_indicador] == 2).sum()
        pct_acesso_tipo = 100.0 * com_acesso_tipo / total_tipo if total_tipo > 0 else 0.0
        
        linhas.append("")
        linhas.append(f"{tipo_nome}:")
        linhas.append(f"  Total: {total_tipo} domicílios")
        linhas.append(f"  Com acesso: {com_acesso_tipo} ({pct_acesso_tipo:.1f}%)")
        linhas.append(f"  Sem acesso: {sem_acesso_tipo} ({100-pct_acesso_tipo:.1f}%)")
        linhas.append(f"  Média de moradores: {df_tipo['A01npessoas'].mean():.2f}")

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas))
