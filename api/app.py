from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente
from logger import logger
from schemas import *
from flask_cors import CORS

from services.predicao_service import realizar_predicao

# Instanciando o objeto OpenAPI
info = Info(title="API de Predição de Doenças Cardíacas", version="1.0.0")
app = OpenAPI(__name__, info=info, static_folder='../front', static_url_path='/front')
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de dados de pacientes")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi."""
    return redirect('/openapi')

# Rota de Adicionar Paciente
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "422": ErrorSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(body: PacienteSchema):
    """Adiciona um novo registro de paciente, realiza a predição e salva na base.
       O corpo da requisição deve seguir o PacienteSchema.
    """
    form = PacienteSchema.model_validate(body)
    
    try:
        paciente = realizar_predicao(form)
        
        logger.debug(f"Adicionando paciente de nome: '{paciente.name}' com diagnóstico: {paciente.outcome}")
        
        session = Session()
        
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        session.add(paciente)
        session.commit()
        
        logger.debug(f"Adicionado paciente de nome: '{paciente.name}'")
        return apresenta_paciente(paciente), 200
    
    except Exception as e:
        error_msg = f"Não foi possível salvar novo paciente: {e}"
        logger.warning(f"Erro ao adicionar paciente '{form.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes na base."""
    logger.info("Coletando dados de pacientes")
    session = Session()
    pacientes = session.query(Paciente).all()
    if not pacientes:
        return {"pacientes": []}, 200
    else:
        logger.info(f"%d pacientes encontrados" % len(pacientes))
        return apresenta_pacientes(pacientes), 200

@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Lista o paciente na base pelo nome."""
    paciente_nome = query.name
    logger.debug(f"Coletando dados sobre paciente #{paciente_nome}")
    session = Session()
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    if not paciente:
        error_msg = f"Paciente {paciente_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente '{paciente_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.name}'")
        return apresenta_paciente(paciente), 200

@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Deleta o paciente na base. """
    paciente_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    session = Session()
    count = session.query(Paciente).filter(Paciente.name == paciente_nome).delete()
    session.commit()
    if count:
        logger.debug(f"Deletado paciente #{paciente_nome}")
        return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200
    else:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{paciente_nome}', {error_msg}")
        return {"message": error_msg}, 404