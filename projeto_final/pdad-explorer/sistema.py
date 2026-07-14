import threading
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import numpy
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import utils.calcular
import utils.carregar
import utils.exportar

matplotlib.use("TkAgg")

class PDADExplorer:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("PDAD Explorer")
        self.janela.geometry("1100x750")
        self.janela.minsize(900, 650)

        self.moradores = None
        self.domicilios = None
        self.dados_cruzados = None

        self._montar_layout_inicial()
        self._iniciar_carregamento()

    def _montar_layout_inicial(self):
        titulo = tkinter.ttk.Label(
            self.janela,
            text = """
                 PDAD Explorer
                 infraestrutura e condições dos domicílios
                 microdados da Pesquisa Distrital por Amostra de Domicílios de 2024
                 """,
            font = ("Segoe UI", 14, "bold"),
        )
        titulo.pack(pady = (4, 2))

        subtitulo = tkinter.ttk.Label(
            self.janela,
            text = "estudante Marcos Torres, APC 2026.1",
        )
        subtitulo.pack(pady = (0, 2))

        frame_progresso = tkinter.ttk.Frame(self.janela)
        frame_progresso.pack(fill = "x", padx = 16, pady = 2)

        self.label_progresso = tkinter.ttk.Label(frame_progresso, text = "Carregando dados...")
        self.label_progresso.pack(anchor = "w")

        self.barra_progresso = tkinter.ttk.Progressbar(
            frame_progresso,
            mode = "indeterminate",
            length = 400,
        )
        self.barra_progresso.pack(fill = "x", pady = 4)
        self.barra_progresso.start(10)

        self.frame_principal = tkinter.ttk.Frame(self.janela)
        self.frame_principal.pack(fill = "both", expand = True, padx = 16, pady = (4, 8))

    def _iniciar_carregamento(self):
        # carregamento dos dados rodando em uma thread separada para não travar a interface gráfica
        thread = threading.Thread(target = self._carregar_em_segundo_plano, daemon = True)
        thread.start()

    def _carregar_em_segundo_plano(self):
        try:
            moradores, domicilios = utils.carregar.carregar_dados()
            cruzados = utils.carregar.cruzar_tabelas(moradores, domicilios)
            self.janela.after(0, self._finalizar_carregamento, moradores, domicilios, cruzados)
        except Exception as erro:
            self.janela.after(0, self._mostrar_erro_carregamento, str(erro))

    def _mostrar_erro_carregamento(self, mensagem):
        self.barra_progresso.stop()
        self.label_progresso.config(text = "Erro ao carregar dados.")
        tkinter.messagebox.showerror("Erro", mensagem)

    def _finalizar_carregamento(self, moradores, domicilios, cruzados):
        self.moradores = moradores
        self.domicilios = domicilios
        self.dados_cruzados = cruzados

        self.barra_progresso.stop()
        self.barra_progresso.pack_forget()
        self.label_progresso.pack_forget()

        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        self._montar_interface()

    def _lista_ras(self):
        codigos = sorted(self.domicilios["localidade"].unique())
        return ["Todas"] + [f"{utils.carregar.nome_ra(c)} ({c})" for c in codigos]

    def _codigo_da_opcao(self, opcao):
        if opcao in (None, "", "Todas"):
            return "Todas"
        return int(opcao.split("(")[-1].replace(")", "").strip())

    def _montar_interface(self):
        frame_filtros = tkinter.ttk.LabelFrame(self.frame_principal, text = "Filtros", padding = 10)
        frame_filtros.pack(fill = "x", pady = (0, 3))

        tkinter.ttk.Label(frame_filtros, text = "RA:").grid(row = 0, column = 0, sticky = "w", padx = 4, pady = 4)
        self.combo_ra = tkinter.ttk.Combobox(frame_filtros, values = self._lista_ras(), state = "readonly", width = 28)
        self.combo_ra.current(0)
        self.combo_ra.grid(row = 0, column = 1, padx = 4, pady = 4)
        self.combo_ra.bind("<<ComboboxSelected>>", lambda _: self.atualizar_visualizacoes())

        tkinter.ttk.Label(frame_filtros, text = "Indicador:").grid(row = 0, column = 2, sticky = "w", padx = 4, pady = 4)
        self.combo_indicador = tkinter.ttk.Combobox(
            frame_filtros,
            values = list(utils.carregar.INDICADORES.keys()),
            state = "readonly",
            width = 24,
        )
        self.combo_indicador.current(0)
        self.combo_indicador.grid(row = 0, column = 3, padx = 4, pady = 4)
        self.combo_indicador.bind("<<ComboboxSelected>>", lambda _: self.atualizar_visualizacoes())

        tkinter.ttk.Label(frame_filtros, text = "RA comparação:").grid(row = 1, column = 0, sticky = "w", padx = 4, pady = 4)
        opcoes_ra_comparacao = ["nenhuma"] + [f"{utils.carregar.nome_ra(c)} ({c})" for c in sorted(self.domicilios["localidade"].unique())]
        self.combo_ra_comparacao = tkinter.ttk.Combobox(frame_filtros, values = opcoes_ra_comparacao, state = "readonly", width = 28)
        self.combo_ra_comparacao.current(0)
        self.combo_ra_comparacao.grid(row = 1, column = 1, padx = 4, pady = 4)
        self.combo_ra_comparacao.bind("<<ComboboxSelected>>", lambda _: self.atualizar_visualizacoes())

        tkinter.ttk.Button(frame_filtros, text = "gerar mini relatório", command = self.exportar_dados).grid(
            row = 0, column = 4, rowspan = 2, padx = 12, pady = 4, sticky = "ns"
        )

        frame_stats = tkinter.ttk.LabelFrame(self.frame_principal, text = "estatísticas descritivas", padding = 10)
        frame_stats.pack(fill = "x", pady = (0, 3))
        self.label_stats = tkinter.ttk.Label(frame_stats, text = "", justify = "left")
        self.label_stats.pack(anchor = "w")

        frame_conteudo = tkinter.ttk.Frame(self.frame_principal)
        frame_conteudo.pack(fill = "both", expand = True)

        frame_graficos = tkinter.ttk.Frame(frame_conteudo)
        frame_graficos.pack(side = "left", fill = "both", expand = True)

        frame_ranking = tkinter.ttk.LabelFrame(frame_conteudo, text = "ranking de RAs", padding = 8)
        frame_ranking.pack(side = "right", fill = "y", padx = (8, 0))

        self.lista_ranking = tkinter.Listbox(frame_ranking, width = 34, height = 14)
        self.lista_ranking.pack(fill = "y", expand = True)
        self.lista_ranking.bind("<Double-Button-1>", self.abrir_detalhes_ra)

        tkinter.ttk.Label(
            frame_ranking,
            text = "duplo clique em uma RA para detalhes",
            wraplength = 240,
        ).pack(pady = (6, 0))

        self.figura = matplotlib.figure.Figure(figsize = (8, 6), dpi = 100)
        self.ax_barras = self.figura.add_subplot(111)
        self.figura.tight_layout(pad = 2.0)

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.figura, master = frame_graficos)
        self.canvas.get_tk_widget().pack(fill = "both", expand = True)

        self.ranking_dados = []
        self.atualizar_visualizacoes()

    def _coluna_indicador_atual(self):
        nome_descritivo = self.combo_indicador.get()
        return utils.carregar.INDICADORES.get(nome_descritivo, nome_descritivo)

    def _df_filtrado(self):
        ra = self._codigo_da_opcao(self.combo_ra.get())
        return utils.calcular.filtrar_por_ra(self.domicilios, ra)

    def atualizar_visualizacoes(self):
        if self.domicilios is None:
            return

        coluna = self._coluna_indicador_atual()
        df = self._df_filtrado()
        stats = utils.calcular.estatisticas_domicilios(df, coluna)
        indicador_descricao = utils.carregar.INDICADORES_DESCRICOES.get(coluna, coluna)

        self.label_stats.config(
            text = (
                f"indicador: {indicador_descricao}\n"
                f"total de domicílios: {stats['contagem']}  |  "
                f"média de moradores: {stats['media_moradores']:.2f}  |  "
                f"mediana de moradores: {stats['mediana_moradores']:.1f}  |  "
                f"percentual com acesso: {stats['percentual_acesso']:.1f}%"
            )
        )

        self._desenhar_grafico_barras(coluna, df)
        self._atualizar_ranking(coluna)
        self.canvas.draw()

    def _desenhar_grafico_barras(self, coluna, df):
        self.ax_barras.clear()

        ra_selecionada = self._codigo_da_opcao(self.combo_ra.get())
        ra_comparacao = self.combo_ra_comparacao.get()
        
        if ra_comparacao == "nenhuma":
            nomes = []
            valores = []
            for nome_indicador, codigo_indicador in utils.carregar.INDICADORES.items():
                nomes.append(nome_indicador)
                valores.append(utils.calcular.percentual_com_acesso(df, codigo_indicador))

            barras = self.ax_barras.bar(nomes, valores, color = "#F18F01")
            self.ax_barras.set_ylabel("% com acesso")
            self.ax_barras.set_title(
                f"Indicadores de infraestrutura — {utils.carregar.nome_ra(ra_selecionada)}",
                fontsize = 10,
            )
            self.ax_barras.tick_params(axis = "x")
            self.ax_barras.set_ylim(0, 100)

            for barra, valor in zip(barras, valores):
                self.ax_barras.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 1,
                    f"{valor:.1f}%",
                    ha = "center",
                    va = "bottom",
                    fontsize = 8,
                )
        else:
            ra_comp_codigo = self._codigo_da_opcao(ra_comparacao)
            df_ra1 = utils.calcular.filtrar_por_ra(self.domicilios, ra_selecionada)
            df_ra2 = utils.calcular.filtrar_por_ra(self.domicilios, ra_comp_codigo)
            
            nomes_indicadores = []
            valores_ra1 = []
            valores_ra2 = []
            
            for nome_indicador, codigo_indicador in utils.carregar.INDICADORES.items():
                nomes_indicadores.append(nome_indicador)
                valores_ra1.append(utils.calcular.percentual_com_acesso(df_ra1, codigo_indicador))
                valores_ra2.append(utils.calcular.percentual_com_acesso(df_ra2, codigo_indicador))
            
            x = numpy.arange(len(nomes_indicadores))
            largura = 0.35
            
            barras1 = self.ax_barras.bar(x - largura / 2, valores_ra1, largura, label = utils.carregar.nome_ra(ra_selecionada), color = "#2E86AB")
            barras2 = self.ax_barras.bar(x + largura / 2, valores_ra2, largura, label = utils.carregar.nome_ra(ra_comp_codigo), color = "#A23B72")
            
            self.ax_barras.set_ylabel("% com acesso")
            self.ax_barras.set_title(
                f"Comparação de indicadores — {utils.carregar.nome_ra(ra_selecionada)} vs {utils.carregar.nome_ra(ra_comp_codigo)}",
                fontsize = 10,
            )
            self.ax_barras.set_xticks(x)
            self.ax_barras.set_xticklabels(nomes_indicadores)
            self.ax_barras.set_ylim(0, 100)
            self.ax_barras.legend(fontsize = 8)
            
            for barra, valor in zip(barras1, valores_ra1):
                self.ax_barras.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 1,
                    f"{valor:.1f}%",
                    ha = "center",
                    va = "bottom",
                    fontsize = 7,
                )
            
            for barra, valor in zip(barras2, valores_ra2):
                self.ax_barras.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 1,
                    f"{valor:.1f}%",
                    ha = "center",
                    va = "bottom",
                    fontsize = 7,
                )

    def _atualizar_ranking(self, coluna):
        self.lista_ranking.delete(0, tkinter.END)

        # ranking calculado para todas as RAs, independentemente do filtro principal
        self.ranking_dados = utils.calcular.distribuicao_por_ra(self.domicilios, coluna)

        for posicao, item in enumerate(self.ranking_dados, start = 1):
            self.lista_ranking.insert(
                tkinter.END,
                f"{posicao:02d}. {item['nome']}: {item['percentual']:.1f}%",
            )

    def abrir_detalhes_ra(self, _evento=None):
        selecao = self.lista_ranking.curselection()
        if not selecao:
            return
        item = self.ranking_dados[selecao[0]]
        self._abrir_janela_detalhes(item["codigo"])

    # abre uma janela secundária com o resumo da RA selecionada no ranking
    def _abrir_janela_detalhes(self, codigo_ra):
        coluna = self._coluna_indicador_atual()
        info = utils.calcular.detalhes_ra(self.domicilios, codigo_ra, coluna)

        janela = tkinter.Toplevel(self.janela)
        janela.title(f"Detalhes — {info['nome']}")
        janela.geometry("420x360")

        texto = [
            f"região administrativa: {info['nome']} (cód. {info['codigo']})",
            f"indicador: {info['indicador']}",
            "",
            f"total de domicílios: {info['stats']['contagem']}",
            f"média de moradores: {info['stats']['media_moradores']:.2f}",
            f"mediana de moradores: {info['stats']['mediana_moradores']:.1f}",
            f"percentual com acesso: {info['stats']['percentual_acesso']:.1f}%",
            "",
            "distribuição por tipo de imóvel:",
        ]

        for tipo, quantidade in info["tipos_imovel"].items():
            texto.append(f"  • {tipo}: {quantidade}")

        caixa = tkinter.Text(janela, wrap = "word", padx = 12, pady = 12)
        caixa.pack(fill = "both", expand = True)
        caixa.insert("1.0", "\n".join(texto))
        caixa.config(state = "disabled")

    def exportar_dados(self):
        caminho = tkinter.filedialog.asksaveasfilename(
            defaultextension = ".txt",
            filetypes = [
                ("texto", "*.txt"),
                ("CSV", "*.csv"),
            ],
            title = "exportar dados filtrados",
        )
        if not caminho:
            return

        try:
            coluna = self._coluna_indicador_atual()
            ra = self._codigo_da_opcao(self.combo_ra.get())
            utils.exportar.exportar_para_arquivo(caminho, self._df_filtrado(), coluna, ra)
            tkinter.messagebox.showinfo("exportação", f"Arquivo salvo em:\n{caminho}")
        except Exception as erro:
            tkinter.messagebox.showerror("erro na exportação", str(erro))

def main():
    janela = tkinter.Tk()
    PDADExplorer(janela)
    janela.mainloop()

if __name__ == "__main__":
    main()
