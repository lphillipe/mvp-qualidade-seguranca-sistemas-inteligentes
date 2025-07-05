# MVP Qualidade e Segurança de Sistemas Inteligentes - Diagnóstico de doenças cardíacas API

## 📖 Descrição do Projeto

Este projeto é uma aplicação web full-stack que utiliza um modelo de Machine Learning para prever a presença de doenças cardíacas em pacientes, com base em um conjunto de atributos clínicos. A aplicação foi desenvolvida como parte do MVP da Pós-graduação em Engenharia de Software da PUC-Rio.

O sistema permite que um usuário insira os dados de um paciente através de uma interface web, que são enviados para uma API em Flask. A API utiliza um modelo de classificação (Random Forest) previamente treinado para realizar o diagnóstico, armazena os resultados em um banco de dados SQLite e exibe o histórico de pacientes na interface.

## ✨ Funcionalidades

-   **Interface Web Amigável:** Formulário claro para entrada de dados e tabela para visualização dos resultados.
-   **Predição com Machine Learning:** Utiliza um pipeline treinado com Scikit-learn para diagnosticar a presença ou ausência de doença cardíaca.
-   **API RESTful:** Back-end construído com Flask e documentado com OpenAPI (Swagger), permitindo a interação com os dados.
-   **Persistência de Dados:** Armazenamento dos dados e diagnósticos dos pacientes em um banco de dados SQLite.
-   **Testes Automatizados:** Suíte de testes com PyTest para garantir a qualidade do modelo de ML e a funcionalidade da API.

## 🛠️ Tecnologias Utilizadas

-   **Back-end:** Python, Flask, Flask-OpenAPI3, SQLAlchemy, Pydantic
-   **Front-end:** HTML, CSS, JavaScript
-   **Machine Learning:** Scikit-learn, Pandas, NumPy
-   **Testes:** PyTest

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.9 ou superior
-   `pip` (gerenciador de pacotes do Python)

### 2. Instalação e Configuração

**a. Clone o repositório (ou baixe os arquivos):**
```bash
    git clone https://github.com/lphillipe/mvp-qualidade-seguranca-sistemas-inteligentes.git
    cd mvp-qualidade-seguranca-sistemas-inteligentes
```

**b. Navegue até a pasta da API:**
```bash 
    cd api 
```

**c. Crie e ative um ambiente virtual:**

É uma boa prática isolar as dependências do projeto.

## Criar o ambiente virtual
```bash 
    python -m venv venv
```

## Ativar no Windows
```bash 
    venv\Scripts\activate
```

## Ativar no macOS/Linux
```bash 
    source venv/bin/activate
```

**d. Instale as dependências:**
```bash 
    pip install -r requirements.txt
```

### 3. Executando a Aplicação

**a. Inicie o Servidor da API:**

Certifique-se de que você está no diretório `api/` e que o ambiente virtual está ativado.

```bash 
    flask run --host 0.0.0.0 --port 5000 --reload
```

O terminal irá indicar que o servidor está rodando geralmente em http://127.0.0.1:5000

**b. Acessando a Aplicação**

Com o servidor rodando, você pode acessar as duas partes do sistema:

-   **Interface Web do Usuário:** Para usar a aplicação e fazer diagnósticos, acesse a URL principal. Você será redirecionado para a interface.
    ```
    http://127.0.0.1:5000/
    ```

-   **Documentação da API (Swagger):** Para ver e testar os endpoints da API, acesse a rota `/docs`.
    ```
    http://127.0.0.1:5000/docs
    ```

A aplicação estará pronta para uso.

### 4. Executando os Testes Automatizados

Para garantir que tudo está funcionando corretamente, voçê pode executar a suíte de testes.

**a. Execute o PyTest:**

Com o ambiente virtual ativado e no diretório `api/`, execute o comando:

```bash 
    pytest -v
```

Todos os testes devem passar, confirmando que o modelo de ML atende ao requisito de qualidade e que a API está funcionando como esperado.

### 5. Treinando o Modelo

O modelo já está treinado e salvo em `api/MachineLearning/pipelines/`. Se desejar retreiná-lo ou explorar a análise de dados, você pode abrir e executar o notebook `api/MachineLearning/notebooks/Heart_Disease_Classification.ipynb` em um ambiente como o VSCode ou Jupyter.


