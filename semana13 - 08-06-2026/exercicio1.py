# relatorio_moradores.py
import sys
import pandas

if len(sys.argv) < 2:
    print("Uso: python exercicio1.py <nome_do_arquivo.txt>")
    sys.exit(1)

arquivo_saida = sys.argv[1]

moradores = pandas.read_csv("moradores.csv", sep = ";", decimal = ",", encoding = "utf-8-sig")
validos = moradores[moradores["idade_calculada"] != 99999]
idades = validos["idade_calculada"].tolist()
media_idade = sum(idades) / len(idades)

linhas = []
linhas.append("=" * 50)
linhas.append("RELATÓRIO PDAD 2024 — MORADORES")
linhas.append("=" * 50)
linhas.append(f"Total de moradores na amostra : {len(moradores)}")
linhas.append(f"Com idade declarada           : {len(validos)}")
linhas.append(f"Média de idade                : {media_idade:.1f} anos")
linhas.append(f"Idade mínima                  : {min(idades)} anos")
linhas.append(f"Idade máxima                  : {max(idades)} anos")


regioes_administrativas = [
  {"nome": "Arniqueira", "codigo": 5249},
  {"nome": "Sobradinho", "codigo": 5314},
  {"nome": "Jardim Botânico", "codigo": 5315},
  {"nome": "Lago Sul", "codigo": 5319},
  {"nome": "Gama", "codigo": 5320},
  {"nome": "Samambaia", "codigo": 5326},
  {"nome": "São Sebastião", "codigo": 5330}
]

for i in range(1, len(regioes_administrativas)):
    chave = regioes_administrativas[i]
    j = i - 1
    while j >= 0 and regioes_administrativas[j]["nome"] > chave["nome"]:
        regioes_administrativas[j + 1] = regioes_administrativas[j]
        j -= 1
    regioes_administrativas[j + 1] = chave

for ra in regioes_administrativas:
  moradores_da_ra = moradores[moradores["localidade"] == ra["codigo"]]
  linhas.append(f"quantidade de moradores na RA {ra["nome"]}: {len(moradores_da_ra)}")

with open(arquivo_saida, "w", encoding = "utf-8") as f:
    for linha in linhas:
        f.write(linha + "\n")

print(f"Relatório salvo em: {arquivo_saida}")
