from model import Carregador, Avaliador, Pipeline

# Para executar: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
avaliador = Avaliador()
pipeline = Pipeline()

# --- PARÂMETROS DO TESTE ---

# Usamos o arquivo de teste que o nosso notebook gerou
url_dados = "./MachineLearning/data/test_dataset_heart.csv"

# Definimos as colunas do nosso dataset com os 7 atributos + target
colunas = ['thal', 'ca', 'cp', 'oldpeak', 'thalach', 'exang', 'age', 'target']

# Caminho para o nosso pipeline treinado
rf_path = './MachineLearning/pipelines/heart_disease_pipeline.pkl'

# Threshold mínimo de acurácia que o modelo deve atingir
# Baseado no resultado do notebook (~85%), definimos 80% como um valor seguro.
ACURACIA_MINIMA = 0.80

# --- CARGA DOS DADOS DE TESTE ---
dataset = carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:,0:-1]  # Atributos
y = array[:,-1]   # Target

# --- TESTE DO MODELO ---

def test_modelo_random_forest():  
    """
    Função para testar o pipeline de Random Forest.
    Verifica se a acurácia do modelo no conjunto de teste é maior ou igual 
    ao nosso threshold definido.
    """
    # Importando o pipeline de Random Forest
    modelo_rf = pipeline.carrega_pipeline(rf_path)

    # Obtendo a acurácia do modelo
    acuracia_rf = avaliador.avaliar(modelo_rf, X, y)
    
    # Verificando se a acurácia atende ao requisito mínimo
    assert acuracia_rf >= ACURACIA_MINIMA