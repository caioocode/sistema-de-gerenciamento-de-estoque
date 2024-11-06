from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Base de dados simulada
produtos = []
usuarios = []

# Modelos Pydantic para validação dos dados
class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    quantidade: int
    preco: float
    corredor: str
    prateleira: str

class Relatorio(BaseModel):
    id: int
    descricao: str
    data: str

class Usuario(BaseModel):
    inscricao: str
    senha: str
    tipo: str  # "UsuarioComum", "Estoquista", ou "Gerente"

# Rotas para gerenciamento de produtos
@app.post("/produtos/", response_model=Produto)
def cadastrar_produto(produto: Produto):
    # Verifica se o produto já existe
    for p in produtos:
        if p.id == produto.id:
            raise HTTPException(status_code=400, detail="Produto já cadastrado.")
    produtos.append(produto)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_estoque(produto_id: int, quantidade: int):
    for p in produtos:
        if p.id == produto_id:
            p.quantidade += quantidade
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@app.get("/produtos/{produto_id}", response_model=Produto)
def localizar_produto(produto_id: int):
    for p in produtos:
        if p.id == produto_id:
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@app.get("/relatorios/", response_model=List[Relatorio])
def gerar_relatorios():
    # Gerar relatórios sobre o estoque (simulação)
    return [
        {"id": 1, "descricao": "Relatório de produtos com baixo estoque", "data": "2024-11-04"},
        {"id": 2, "descricao": "Movimentação de produtos", "data": "2024-11-04"}
    ]

# Rotas para gerenciamento de usuários
@app.post("/usuarios/", response_model=Usuario)
def cadastrar_usuario(usuario: Usuario):
    # Verifica se o usuário já existe
    for u in usuarios:
        if u.inscricao == usuario.inscricao:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
    usuarios.append(usuario)
    return usuario

@app.get("/usuarios/{inscricao}", response_model=Usuario)
def localizar_usuario(inscricao: str):
    for u in usuarios:
        if u.inscricao == inscricao:
            return u
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")




