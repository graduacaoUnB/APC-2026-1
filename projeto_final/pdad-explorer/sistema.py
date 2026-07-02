import matplotlib
import pandas
import tkinter

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
