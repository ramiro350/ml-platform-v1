# ML Platform API

Esta é uma plataforma de Machine Learning que permite treinar modelos e fazer predições por meio de uma API REST. A aplicação está containerizada em Docker e pode ser acessada via API documentada com Swagger.

## Pré-requisitos

Certifique-se de ter o Docker instalado na sua máquina. Se não tiver, siga as instruções de instalação no site oficial: [Docker](https://www.docker.com/products/docker-desktop).

## Como construir e rodar o container Docker

1. Clone este repositório em sua máquina:

   ```bash
   git clone https://github.com/antonio-marcos1989/ml-platform-v1.git
   cd ml-platform-v1
   
2. Construa a imagem Docker:
    ```bash
    docker build -t ml-predict-api
3. Execute o container Docker:
    ```bash
    docker run -p 5001:5001 ml-predict-api
   
## Construindo os Modelos

A API oferece um endpoint para treinar diferentes modelos (pipeline de treinamento) de Machine Learning. Para fazer o treinamento de um modelo, você pode utilizar uma ferramenta como curl ou Postman.

1. Endpoint de treinamento

        URL: /ml/model/train
        Método: POST

    ```bash
    curl -X POST "http://localhost:5001/ml/train" \
    -H "Content-Type: application/json" \
    -d '{
        "algorithm": "RandomForest",
        "train_size": 0.8,
        "hyperparams": {
            "n_estimators": 100,
            "max_depth": 10
        }
      }'

Parâmetros:
algorithm: O algoritmo de Machine Learning que você deseja usar (ex.: RandomForest, SVM).

train_size: A proporção dos dados a serem usados para o treinamento (ex.: 0.8).

hyperparams: Hiperparâmetros opcionais que variam de acordo com o algoritmo.

2. Exemplo de Resposta

    ```json
       {
        "model_file_name": "RandomForest_20231031_235959.pkl",
        "metrics": {
        "accuracy": 0.95,
        "precision": 0.93,
        "recall": 0.94,
        "f1_score": 0.94
        }
    }
   
## Consultando modelos existentes

Você pode listar todos os modelos treinados com o seguinte endpoint:

1. Endpoint de listagem de modelos

        URL: /ml/models
        Método: GET

    ```bash
    curl -X GET "http://localhost:5001/ml/models"

2. Exemplo de Resposta

    ```json
    {
      "models": [
        "SVM_20241031_033202",
        "RandomForest_20241031_033232"
      ]
    }
## Fazendo Predições

1. Endpoint de predição

        URL: /ml/predict/{model_name}
        Método: POST

    ```bash
    curl -X POST "http://localhost:5001/ml/predict/RandomForest_20231031_235959" \
      -H "Content-Type: application/json" \
      -d '{
            "input_data": [
                [5.1, 3.5, 1.4, 0.2],
                [6.1, 3.0, 4.9, 1.8]
            ]
          }'


Parâmetros:

model_name: O nome do modelo já treinado (sem a extensão .pkl). 

input_data: Os dados de entrada para a predição (uma lista de listas, onde cada lista é um conjunto de características).

2. Exemplo de Resposta

    ```json
       {
         "predictions": [0, 2]
       }
   
## Contexto da Predição:
O modelo treinado é um classificador que tenta prever categorias ou classes do dataset Iris. 

O dataset Iris, possui três classes de flores (representadas pelos valores 0, 1, e 2), o resultado da predição [0, 2] indica que o modelo classificou o primeiro conjunto de dados de entrada na classe 0 e o segundo na classe 2.

### Classes do Dataset:

#### As classes podem ser as seguintes:
    0: Iris-setosa
    1: Iris-versicolor
    2: Iris-virginica

Neste caso, a predição [0, 2] está dizendo que o primeiro conjunto de dados de entrada foi classificado como "Iris-setosa" (0), e o segundo foi classificado como "Iris-virginica" (2).
   
## Documentação Swagger

A API está documentada e pode ser acessada via Swagger em:

http://localhost:5001/swagger-ui/

Lá, você poderá testar os endpoints diretamente na interface.

## Arquitetura AWS

                +-----------------------------------------------+
                |                Usuário (Cliente)              |
                |          (Postman, cURL, App Frontend)        |
                +----------------------+------------------------+
                                       |
                                       | Requisições HTTP (Treinamento/Predição)
                                       |
                                       v
                +----------------------+------------------------+
                |               Amazon API Gateway              |
                |         (Interface Central de APIs)           |
                +-----------------+------------+---------------+
                                  |            |
                   Treinamento    |            |    Predição
                                  v            v
          +--------------------+              +--------------------+
          |  AWS Lambda        |              |  AWS Lambda        |
          |  Função de         |              |  Função de         |
          |  Treinamento       |              |  Predição          |
          +---------+----------+              +----------+---------+
                    |                                |
                    |                                | Carregar Modelo
                    |                                v
                    |                        +-------+-------+
                    |                        |               |
                    | Salvar Modelo          |   Amazon S3   |
                    +----------------------->| (Modelos e    |
                                             |  Dados)       |
                                             +-------+-------+
                                                     |
                                                     | Logs, Métricas
                                                     v
                                           +---------+---------+
                                           |                    |
                                           |   Amazon CloudWatch|
                                           | (Monitoramento e   |
                                           |  Logs do Sistema)  |
                                           +--------------------+

