import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Configurar banco de dados
def inicializar_banco():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Funções principais
def buscar_produto():
    termo = entry_busca.get()
    coluna = combo_busca.get().lower()

    if not termo:
        messagebox.showwarning("Aviso", "Por favor, insira um termo para busca.")
        return

    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM produtos WHERE {coluna} LIKE ?"
    cursor.execute(query, (f"%{termo}%",))
    resultados = cursor.fetchall()
    conn.close()

    for item in tree.get_children():
        tree.delete(item)

    for resultado in resultados:
        tree.insert("", "end", values=resultado)


def limpar_campos():
    entry_busca.delete(0, tk.END)
    for item in tree.get_children():
        tree.delete(item)


def atualizar_lista():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    resultados = cursor.fetchall()
    conn.close()

    for item in tree.get_children():
        tree.delete(item)

    for resultado in resultados:
        tree.insert("", "end", values=resultado)


def adicionar_produto():
    codigo = entry_codigo.get()
    nome = entry_nome.get()
    preco = entry_preco.get()

    if not codigo or not nome or not preco:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (codigo, nome, preco) VALUES (?, ?, ?)",
        (codigo, nome, float(preco)),
    )
    conn.commit()
    conn.close()

    limpar_campos()
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")


def editar_produto():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para editar.")
        return

    valores = tree.item(item_selecionado, "values")
    codigo = entry_codigo.get()
    nome = entry_nome.get()
    preco = entry_preco.get()

    if not codigo or not nome or not preco:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET codigo = ?, nome = ?, preco = ? WHERE id = ?",
        (codigo, nome, float(preco), valores[0]),
    )
    conn.commit()
    conn.close()

    limpar_campos()
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")


def remover_produto():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para remover.")
        return

    valores = tree.item(item_selecionado, "values")
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (valores[0],))
    conn.commit()
    conn.close()

    atualizar_lista()
    messagebox.showinfo("Sucesso", "Produto removido com sucesso!")


# Interface gráfica
root = tk.Tk()
root.title("Sistema de Gestão de Produtos")
root.geometry("800x500")
root.configure(bg="#f4f4f4")

frame_topo = tk.Frame(root, bg="#333", height=50)
frame_topo.pack(fill=tk.X)

label_titulo = tk.Label(
    frame_topo, text="Gestão de Produtos", bg="#333", fg="white", font=("Arial", 16)
)
label_titulo.pack(pady=10)

frame_principal = tk.Frame(root, bg="#f4f4f4", padx=10, pady=10)
frame_principal.pack(fill=tk.BOTH, expand=True)

# Campos de busca
frame_busca = tk.Frame(frame_principal, bg="#f4f4f4")
frame_busca.pack(fill=tk.X, pady=10)

label_busca = tk.Label(
    frame_busca, text="Buscar por:", bg="#f4f4f4", font=("Arial", 12)
)
label_busca.pack(side=tk.LEFT, padx=5)

combo_busca = ttk.Combobox(
    frame_busca, values=["Código", "Nome", "Preço"], state="readonly", width=15
)
combo_busca.current(0)
combo_busca.pack(side=tk.LEFT, padx=5)

entry_busca = ttk.Entry(frame_busca, width=30)
entry_busca.pack(side=tk.LEFT, padx=5)

btn_buscar = ttk.Button(frame_busca, text="Buscar", command=buscar_produto)
btn_buscar.pack(side=tk.LEFT, padx=5)

btn_limpar = ttk.Button(frame_busca, text="Limpar", command=limpar_campos)
btn_limpar.pack(side=tk.LEFT, padx=5)

btn_atualizar = ttk.Button(frame_busca, text="Atualizar", command=atualizar_lista)
btn_atualizar.pack(side=tk.LEFT, padx=5)

# Lista de produtos
tree = ttk.Treeview(
    frame_principal,
    columns=("ID", "Código", "Nome", "Preço"),
    show="headings",
    height=15,
)
tree.column("ID", width=50, anchor="center")
tree.column("Código", width=100, anchor="center")
tree.column("Nome", width=200, anchor="w")
tree.column("Preço", width=100, anchor="center")
tree.heading("ID", text="ID")
tree.heading("Código", text="Código")
tree.heading("Nome", text="Nome")
tree.heading("Preço", text="Preço")
tree.pack(fill=tk.BOTH, expand=True, pady=10)

# Formulário de produto
frame_formulario = tk.Frame(root, bg="#f4f4f4", pady=10)
frame_formulario.pack(fill=tk.X)

label_codigo = tk.Label(
    frame_formulario, text="Código:", bg="#f4f4f4", font=("Arial", 12)
)
label_codigo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_codigo = ttk.Entry(frame_formulario)
entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_nome = tk.Label(frame_formulario, text="Nome:", bg="#f4f4f4", font=("Arial", 12))
label_nome.grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_nome = ttk.Entry(frame_formulario)
entry_nome.grid(row=0, column=3, padx=5, pady=5, sticky="w")

label_preco = tk.Label(
    frame_formulario, text="Preço:", bg="#f4f4f4", font=("Arial", 12)
)
label_preco.grid(row=0, column=4, padx=5, pady=5, sticky="w")
entry_preco = ttk.Entry(frame_formulario)
entry_preco.grid(row=0, column=5, padx=5, pady=5, sticky="w")

btn_adicionar = ttk.Button(
    frame_formulario, text="Adicionar", command=adicionar_produto
)
btn_adicionar.grid(row=0, column=6, padx=5, pady=5)

btn_editar = ttk.Button(frame_formulario, text="Editar", command=editar_produto)
btn_editar.grid(row=0, column=7, padx=5, pady=5)

btn_remover = ttk.Button(frame_formulario, text="Remover", command=remover_produto)
btn_remover.grid(row=0, column=8, padx=5, pady=5)

# Inicialização
inicializar_banco()
atualizar_lista()
root.mainloop()
