# menu_pdad.py
import pandas as pd
import sys

def carregar_dados():
    print("aguarde o carregamento dos dados (demora alguns segundos)")
    mor = pd.read_csv("moradores.csv", sep=";", decimal=",", encoding="utf-8-sig")
    dom = pd.read_excel("domicilios.xlsx")
    return mor, dom

def relatorio_idades(moradores):
    validos = moradores[moradores["idade_calculada"] != 99999]
    idades = validos["idade_calculada"].tolist()
    print(f"\n  Total com idade declarada: {len(idades)}")
    print(f"  Média: {sum(idades)/len(idades):.1f} anos")
    print(f"  Mínima: {min(idades)} | Máxima: {max(idades)}")

def relatorio_escolaridade(moradores):
    nomes = {1:"Sem instrução",2:"Fund. incompleto",3:"Fund. completo",
             4:"Médio incompleto",5:"Médio completo",6:"Superior incompleto",
             7:"Superior completo",8:"Pós-graduação"}
    contagem = {}
    for _, linha in moradores.iterrows():
        n = linha["escolaridade"]
        if n in nomes:
            contagem[n] = contagem.get(n, 0) + 1
    print("\n  Escolaridade:")
    for nivel, total in sorted(contagem.items()):
        print(f"    {nomes[nivel]}: {total}")

def relatorio_domicilios(domicilios):
    print(f"\n  Total de domicílios: {len(domicilios)}")
    media_pessoas = sum(domicilios["A01npessoas"]) / len(domicilios)
    print(f"  Média de moradores por domicílio: {media_pessoas:.1f}")

def salvar_relatorio_completo_em_txt(moradores, domicilios):
  sys.stdout = open("saida_total.txt", "w")

  relatorio_idades(moradores)
  relatorio_escolaridade(moradores)
  relatorio_domicilios(domicilios)

  sys.stdout.close()
  sys.stdout = sys.__stdout__

moradores, domicilios = carregar_dados()

while True:
    print("\n" + "=" * 40)
    print("  PDAD 2024 — Menu de Relatórios")
    print("=" * 40)
    print("  1. Relatório de idades")
    print("  2. Relatório de escolaridade")
    print("  3. Relatório de domicílios")
    print("  4. Salvar relatório completo em TXT")
    print("  0. Sair")
    opcao = input("\n  Escolha uma opção: ").strip()

    if opcao == "1":
        relatorio_idades(moradores)
    elif opcao == "2":
        relatorio_escolaridade(moradores)
    elif opcao == "3":
        relatorio_domicilios(domicilios)
    elif opcao == "0":
        print("  Até logo!")
        break
    else:
        print("  Opção inválida.")