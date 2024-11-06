import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000"

# Funções para interagir com a API
def cadastrar_produto():
    produto = {
        "id": int(entry_id.get()),
        "nome": entry_nome.get(),
        "categoria": entry_categoria.get(),
        "quantidade": int(entry_quantidade.get()),
        "preco": float(entry_preco.get()),
        "corredor": entry_corredor.get(),
        "prateleira": entry_prateleira.get(),
    }
    response = requests.post("http://127.0.0.1:8000/produtos/", json=produto)
    
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        listar_produtos()
    else:
        messagebox.showerror("Erro", "Erro ao cadastrar o produto.")

def listar_produtos():
    response = requests.get("http://127.0.0.1:8000/produtos/")

    print(response.status_code)  # Para verificar o código de status  
    print(response.text)         # Para visualizar a resposta em texto  

    if response.status_code == 200:
        produtos = response.json()
        for i in tree.get_children():
            tree.delete(i)
        for produto in produtos:
            tree.insert("", "end", values=(
                produto["id"], produto["nome"], produto["categoria"],
                produto["quantidade"], produto["preco"], produto["corredor"],
                produto["prateleira"]
            ))
    else:
        messagebox.showerror("Erro", "Erro ao listar produtos.")

# Interface Tkinter
app = tk.Tk()
app.title("Sistema de Gerenciamento de Estoque")

# Campos de entrada
tk.Label(app, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(app)
entry_id.grid(row=0, column=1)

tk.Label(app, text="Nome").grid(row=1, column=0)
entry_nome = tk.Entry(app)
entry_nome.grid(row=1, column=1)

tk.Label(app, text="Categoria").grid(row=2, column=0)
entry_categoria = tk.Entry(app)
entry_categoria.grid(row=2, column=1)

tk.Label(app, text="Quantidade").grid(row=3, column=0)
entry_quantidade = tk.Entry(app)
entry_quantidade.grid(row=3, column=1)

tk.Label(app, text="Preço").grid(row=4, column=0)
entry_preco = tk.Entry(app)
entry_preco.grid(row=4, column=1)

tk.Label(app, text="Corredor").grid(row=5, column=0)
entry_corredor = tk.Entry(app)
entry_corredor.grid(row=5, column=1)

tk.Label(app, text="Prateleira").grid(row=6, column=0)
entry_prateleira = tk.Entry(app)
entry_prateleira.grid(row=6, column=1)

# Botões - falta adicionar: atualizar, remover, relatório
btn_cadastrar = tk.Button(app, text="Cadastrar Produto", command=cadastrar_produto)
btn_cadastrar.grid(row=7, column=0, columnspan=2)

# Lista de produtos
tree = ttk.Treeview(app, columns=("ID", "Nome", "Categoria", "Quantidade", "Preço", "Corredor", "Prateleira"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Categoria", text="Categoria")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Preço", text="Preço")
tree.heading("Corredor", text="Corredor")
tree.heading("Prateleira", text="Prateleira")
tree.grid(row=8, column=0, columnspan=2)

btn_listar = tk.Button(app, text="Listar Produtos", command=listar_produtos)
btn_listar.grid(row=9, column=0, columnspan=2)

app.mainloop()
