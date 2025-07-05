from model import Paciente, PreProcessador, Pipeline
from schemas import PacienteSchema

# Instanciando os objetos uma única vez para reutilização
preprocessador = PreProcessador()
pipeline_model = Pipeline()
model_path = './MachineLearning/pipelines/heart_disease_pipeline.pkl'
modelo = pipeline_model.carrega_pipeline(model_path)

def realizar_predicao(form: PacienteSchema) -> Paciente:
    """
    Função de serviço que encapsula a lógica de negócio para
    realizar a predição e criar um objeto Paciente.

    Args:
        form (PacienteSchema): Dados de entrada do paciente.

    Returns:
        Paciente: Objeto SQLAlchemy Paciente com os dados e o diagnóstico.
    """
    
    # 1. Prepara os dados do formulário para o modelo
    X_input = preprocessador.preparar_form(form)
    
    # 2. Realiza a predição com o modelo carregado
    outcome = int(modelo.predict(X_input)[0])
    
    # 3. Cria um objeto Paciente com todos os dados
    paciente = Paciente(
        name=form.name,
        age=form.age,
        cp=form.cp,
        thalach=form.thalach,
        exang=form.exang,
        oldpeak=form.oldpeak,
        ca=form.ca,
        thal=form.thal,
        outcome=outcome
    )
    
    return paciente