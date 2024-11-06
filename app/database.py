from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

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
        orm_mode = True

# Rotas de gerenciamento de produtos
@app.post("/produtos/", response_model=Produto)
def cadastrar_produto(produto: Produto, db: Session = Depends(get_db)):
    db_produto = ProdutoDB(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_estoque(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    db_produto.quantidade += quantidade
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos/{produto_id}", response_model=Produto)
def localizar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return db_produto

# Iniciar o servidor
# uvicorn nome_do_arquivo:app --reload
