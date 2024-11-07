from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./estoque.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir modelos SQLAlchemy
class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    categoria = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)
    corredor = Column(String)
    prateleira = Column(String)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic para validação de dados de entrada/saída
class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    quantidade: int
    preco: float
    corredor: str
    prateleira: str

    class Config:
        from_attributes = True

class Relatorio(BaseModel):
    id: int
    descricao: str
    data: str

class Usuario(BaseModel):
    inscricao: str
    senha: str
    tipo: str  # "UsuarioComum", "Estoquista", ou "Gerente"

# Rotas de gerenciamento de produtos
@app.post("/produtos/", response_model=Produto)
def cadastrar_produto(produto: Produto, db: Session = Depends(get_db)):
    try:        
        # Verifica se o produto já existe no banco
        produto_existente = db.query(ProdutoDB).filter(ProdutoDB.id == produto.id).first()
        if produto_existente:
            raise HTTPException(status_code=400, detail="Produto já cadastrado.")
        
        # Criação do novo produto
        db_produto = ProdutoDB(**produto.dict())  # Cria o objeto ProdutoDB com os dados do Produto Pydantic
        
        db.add(db_produto)  # Adiciona o produto à sessão
        db.commit()  # Confirma a adição no banco
        db.refresh(db_produto)  # Atualiza o objeto para obter o ID gerado e outras informações

        return db_produto  # Retorna o produto cadastrado

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao cadastrar o produto.")
    
@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_estoque(produto_id: int, produto: Produto, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    # Atualiza as informações do produto
    db_produto.nome = produto.nome
    db_produto.categoria = produto.categoria
    db_produto.quantidade = produto.quantidade
    db_produto.preco = produto.preco
    db_produto.corredor = produto.corredor
    db_produto.prateleira = produto.prateleira

    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos/{produto_id}", response_model=Produto)
def localizar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return db_produto

@app.get("/produtos/", response_model=List[Produto])  
def listar_produtos(db: Session = Depends(get_db)):  
    produtos = db.query(ProdutoDB).all()  # Obtém todos os produtos do banco de dados  
    return produtos  

@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    db.delete(db_produto)
    db.commit()
    return {"msg": "Produto excluído com sucesso."}

# Rotas para gerenciamento de relatórios
@app.get("/relatorios/", response_model=List[Relatorio])
def gerar_relatorios(db: Session = Depends(get_db)):
    # Exemplo de relatório de produtos com estoque baixo
    produtos_baixo_estoque = db.query(ProdutoDB).filter(ProdutoDB.quantidade < 10).all()
    
    # Criar relatório com base nos dados do banco
    relatorios = [
        {"id": 1, "descricao": f"Relatório de produtos com baixo estoque: {len(produtos_baixo_estoque)} produtos", "data": "2024-11-04"}
    ]
    return relatorios





