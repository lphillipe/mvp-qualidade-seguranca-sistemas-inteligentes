from pydantic import BaseModel
from typing import List
from model.paciente import Paciente

class PacienteSchema(BaseModel):
    """ Define como os dados de um novo paciente devem ser representados na entrada.
        Todos os campos são obrigatórios.
    """
    name: str
    age: float
    cp: float
    thalach: float
    exang: float
    oldpeak: float
    ca: float
    thal: float

class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado, incluindo o diagnóstico"""
    id: int
    name: str
    age: float
    cp: float
    thalach: float
    exang: float
    oldpeak: float
    ca: float
    thal: float
    outcome: int

class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por nome."""
    name: str

class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada"""
    pacientes: List[PacienteViewSchema]

class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado"""
    name: str

def apresenta_paciente(paciente: Paciente):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "name": paciente.name,
        "age": paciente.age,
        "cp": paciente.cp,
        "thalach": paciente.thalach,
        "exang": paciente.exang,
        "oldpeak": paciente.oldpeak,
        "ca": paciente.ca,
        "thal": paciente.thal,
        "outcome": paciente.outcome
    }

def apresenta_pacientes(pacientes: List[Paciente]):
    """ Retorna uma representação de pacientes seguindo o schema definido.
    """
    result = []
    for paciente in pacientes:
        result.append(apresenta_paciente(paciente))

    return {"pacientes": result}