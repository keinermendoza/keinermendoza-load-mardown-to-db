from os import getenv, listdir, path
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from models import (
    Tag,
    Post,
    Project
)
from reader import MarkdownDocument

load_dotenv()

# Criar conexão com o banco de dados
config = {
    "user": getenv("DB_USER"),
    "host": getenv("DB_HOST"),
    "password": getenv("DB_PASSWORD"),
    "database": getenv("DB_NAME"),
}

DATABASE_URL = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def get_db_record_by_slug(session, model, slug):
    """
    Obtém o primeiro registro de um modelo filtrando pelo slug.

    :param session: Sessão ativa do SQLAlchemy
    :param model: Modelo ORM a ser consultado
    :param slug: Valor do slug
    """
    stmt = select(model).where(model.slug == slug)
    return session.scalars(stmt).first()

def create_or_update(session, model: Post | Project | Tag, buffered_item: MarkdownDocument, slug: str):
    """
    Cria ou atualiza uma instância de um modelo a partir de um documento Markdown.

    - Se o registro existir, ele é atualizado
    - Se não existir, ele é criado
    - Atribui metadata e conteúdo HTML

    :param session: Sessão ativa do SQLAlchemy
    :param model: Modelo ORM (Post, Project, Tag, etc.)
    :param buffered_item: Documento Markdown processado
    :param slug: Identificador único do registro
    """
    instance = get_db_record_by_slug(session, model, slug)
    
    if not instance:
        instance = model(slug=slug)

    for key, value in buffered_item.metadata.items():
        if key != "tags":
            setattr(instance, key, value)

    # Instâncias de Post e Project possuem a propriedade "content"
    if isinstance(instance, (Post, Project)):    
        instance.content = buffered_item.content_html

    try:
        session.add(instance)
        session.commit()
    except Exception as e:
        print(e)

    if isinstance(instance, (Post, Project)):
        # Buscar tags referenciadas
        tags = session.scalars(
            select(Tag).where(Tag.slug.in_(buffered_item.get("tags")))
        ).all()

        # Atualizar relação de tags
        instance.tags = tags
        session.commit()        


def read_markdown_documents_from_dir(str_path: str):
    """
    Lê todos os arquivos Markdown de um diretório e os converte em objetos MarkdownDocument.

    :param str_path: Caminho do diretório
    :yield: Tuplas (slug, instância de MarkdownDocument)
    """
    filepath = Path(str_path)
    for file in listdir(filepath):
        filename = Path(file).stem
        if path.isfile(path.join(filepath, file)):
            yield filename, MarkdownDocument.from_file(filepath / file)

def main():
    for slug, buffered_item in read_markdown_documents_from_dir("./tags"):
        create_or_update(session, Tag, buffered_item, slug)

    for slug, buffered_item in read_markdown_documents_from_dir("./posts"):
        create_or_update(session, Post, buffered_item, slug)

    for slug, buffered_item in read_markdown_documents_from_dir("./projects"):
        create_or_update(session, Project, buffered_item, slug)


if __name__ == "__main__":
    main()