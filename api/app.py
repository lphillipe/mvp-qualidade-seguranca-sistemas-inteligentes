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
home_tag = Tag(name="Documentação e Interface", description="Redirecionamento para a interface do usuário e para a documentação da API.")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de dados de pacientes.")

# Rota principal - redireciona para a interface do usuário
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /front/index.html, a interface web da aplicação."""
    return redirect('/front/index.html')

# Rota para a documentação da API
@app.get('/docs', tags=[home_tag])
def docs():
    """Redireciona para /openapi, a tela de documentação da API (Swagger)."""
    return redirect('/openapi')

# Rota de adição de paciente
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "422": ErrorSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(body: PacienteSchema):
    """Adiciona um novo registro de paciente, realiza a predição e salva na base."""
    form = PacienteSchema.model_validate(body)
    
    try:
        paciente = realizar_predicao(form)
        session = Session()
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            return {"message": "Paciente já existente na base :/"}, 409
        session.add(paciente)
        session.commit()
        return apresenta_paciente(paciente), 200
    except Exception as e:
        return {"message": f"Não foi possível salvar novo paciente: {e}"}, 400

# Rota de listagem de pacientes
@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": ListaPacientesSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os registros de pacientes da base."""
    session = Session()
    pacientes = session.query(Paciente).all()
    if not pacientes:
        return {"pacientes": []}, 200
    return apresenta_pacientes(pacientes), 200

# Rota de busca de paciente por nome
@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Busca um paciente cadastrado na base a partir do nome."""
    paciente_nome = query.name
    session = Session()
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    if not paciente:
        return {"message": f"Paciente {paciente_nome} não encontrado na base :/"}, 404
    return apresenta_paciente(paciente), 200
   
# Rota de remoção de paciente por nome
@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente da base a partir do nome."""
    paciente_nome = unquote(query.name)
    session = Session()
    count = session.query(Paciente).filter(Paciente.name == paciente_nome).delete()
    session.commit()
    if count:
        return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200
    else:
        return {"message": "Paciente não encontrado na base :/"}, 404