from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from . import Base

# colunas = thal, ca, cp, oldpeak, thalach, exang, age, outcome

class Paciente(Base):
    __tablename__ = 'dados_cardiacos'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    
    # Nossos 7 atributos relevantes
    age = Column("Age", Float)
    cp = Column("ChestPain", Float)
    thalach = Column("MaxHeartRate", Float)
    exang = Column("ExerciseAngina", Float)
    oldpeak = Column("STDepression", Float)
    ca = Column("MajorVessels", Float)
    thal = Column("Thalassemia", Float)

    # Diagnóstico
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, name:str, age:float, cp:float, thalach:float, 
                 exang:float, oldpeak:float, ca:float, thal:float, 
                 outcome:int, data_insercao:Union[DateTime, None] = None):
        """
        Cria um registro de Dados Cardíacos de um Paciente

        Arguments:
            name: nome do paciente
            age: idade
            cp: tipo de dor no peito
            thalach: frequência cardíaca máxima
            exang: angina induzida por exercício
            oldpeak: depressão de ST
            ca: número de vasos principais
            thal: tipo de thalassemia
            outcome: diagnóstico (0 = baixo risco, 1 = alto risco)
            data_insercao: data de quando o registro foi inserido na base
        """
        self.name = name
        self.age = age
        self.cp = cp
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.ca = ca
        self.thal = thal
        self.outcome = outcome

        if data_insercao:
            self.data_insercao = data_insercao