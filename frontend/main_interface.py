import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000"

# Funções para interagir com a API
def cadastrar_produto():
    try:
        produto = {
            "id": int(entry_id.get()),
            "nome": entry_nome.get(),
            "categoria": entry_categoria.get(),
            "quantidade": int(entry_quantidade.get()),
            "preco": float(entry_preco.get()),
            "corredor": entry_corredor.get(),
            "prateleira": entry_prateleira.get(),
        }
        
        # Se o botão for para atualizar
        if btn_cadastrar['text'] == "Atualizar Produto":
            response = requests.put(f"{API_URL}/produtos/{produto['id']}/", json=produto)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                listar_produtos()  # Atualiza a lista de produtos
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o produto.")
        else:
            # Se for cadastrar
            response = requests.post(f"{API_URL}/produtos/", json=produto)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                listar_produtos()  # Atualiza a lista de produtos
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar o produto.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente!")

def listar_produtos():
    response = requests.get(f"{API_URL}/produtos/")
    print(response.status_code)
    print(response.text)

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

def editar_produto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Selecione um produto para editar.")
        return
    
    item = tree.item(selected_item)
    values = item['values']
    
    # Preenche os campos com os dados do produto selecionado
    entry_id.delete(0, tk.END)
    entry_id.insert(0, values[0])
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, values[1])
    entry_categoria.delete(0, tk.END)
    entry_categoria.insert(0, values[2])
    entry_quantidade.delete(0, tk.END)
    entry_quantidade.insert(0, values[3])
    entry_preco.delete(0, tk.END)
    entry_preco.insert(0, values[4])
    entry_corredor.delete(0, tk.END)
    entry_corredor.insert(0, values[5])
    entry_prateleira.delete(0, tk.END)
    entry_prateleira.insert(0, values[6])

    btn_cadastrar.config(text="Atualizar Produto")  # Altera o botão para "Atualizar"

def excluir_produto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Selecione um produto para excluir.")
        return

    item = tree.item(selected_item)
    produto_id = item['values'][0]

    # Confirmar exclusão
    if messagebox.askyesno("Confirmar", f"Você tem certeza que deseja excluir o produto com ID {produto_id}?"):
        response = requests.delete(f"{API_URL}/produtos/{produto_id}/")
        if response.status_code == 204:  # Sucesso na exclusão
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            listar_produtos()  # Atualiza a lista de produtos
        else:
            messagebox.showerror("Erro", "Erro ao excluir o produto.")

# Interface Tkinter
app = tk.Tk()
app.title("Sistema de Gerenciamento de Estoque")

# Campos de entrada
tk.Label(app, text="ID").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_id = tk.Entry(app)
entry_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(app, text="Nome").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_nome = tk.Entry(app)
entry_nome.grid(row=1, column=1, padx=5, pady=5)

tk.Label(app, text="Categoria").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_categoria = tk.Entry(app)
entry_categoria.grid(row=2, column=1, padx=5, pady=5)

tk.Label(app, text="Quantidade").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_quantidade = tk.Entry(app)
entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

tk.Label(app, text="Preço").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_preco = tk.Entry(app)
entry_preco.grid(row=4, column=1, padx=5, pady=5)

tk.Label(app, text="Corredor").grid(row=5, column=0, sticky="e", padx=5, pady=5)
entry_corredor = tk.Entry(app)
entry_corredor.grid(row=5, column=1, padx=5, pady=5)

tk.Label(app, text="Prateleira").grid(row=6, column=0, sticky="e", padx=5, pady=5)
entry_prateleira = tk.Entry(app)
entry_prateleira.grid(row=6, column=1, padx=5, pady=5)

# Botões - Cadastro, Edição e Exclusão
btn_cadastrar = tk.Button(app, text="Cadastrar Produto", command=cadastrar_produto)
btn_cadastrar.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

btn_editar = tk.Button(app, text="Editar Produto", command=editar_produto)
btn_editar.grid(row=7, column=2, padx=5, pady=5)

btn_excluir = tk.Button(app, text="Excluir Produto", command=excluir_produto)
btn_excluir.grid(row=7, column=3, padx=5, pady=5)

# Lista de produtos
tree = ttk.Treeview(app, columns=("ID", "Nome", "Categoria", "Quantidade", "Preço", "Corredor", "Prateleira"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Categoria", text="Categoria")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Preço", text="Preço")
tree.heading("Corredor", text="Corredor")
tree.heading("Prateleira", text="Prateleira")
tree.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

btn_listar = tk.Button(app, text="Listar Produtos", command=listar_produtos)
btn_listar.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

app.mainloop()
