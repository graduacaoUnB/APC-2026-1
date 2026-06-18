## 1
```python
import tkinter

# cria a janela raiz
janela = tkinter.Tk()

# configura propriedades
janela.title("minha primeira janela")
janela.geometry("400x200")

# inicia o loop de eventos (aparentemente deve ficar no final)
janela.mainloop()
```

## 2
```python
import tkinter

janela = tkinter.Tk()
janela.title("Widgets")
janela.geometry("320x280")

# texto estático
label = tkinter.Label(janela, text = "nome: ")
label.pack(pady = 4)

# campo de texto de 1 linha
entrada = tkinter.Entry(janela, width = 25)
entrada.pack()

# botão clicável
def saudar():
    nome = entrada.get()
    resultado.config(text = f"Olá, {nome}!")

botao = tkinter.Button(janela, text = "Saudar", command = saudar)
botao.pack(pady = 8)

# label que muda dinamicamente
resultado = tkinter.Label(janela, text = "", fg = "blue")
resultado.pack()

# caixa de seleção
var = tkinter.BooleanVar()
caixa_de_selecao = tkinter.Checkbutton(janela,
                                       text = "lembrar nome",
                                       variable = var)
caixa_de_selecao.pack(pady = 4)

janela.mainloop()
```
