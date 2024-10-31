import sys
sys.path.append('/app')

import os
import pickle

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from library.trainer import train_model

app = Flask(__name__)

# Configurar o Swagger com um caminho específico
api = Api(app, version='1.0', title='ML Model API',
          description='API para treinar vários modelos de Machine Learning',
          doc='/swagger-ui/'  # Define o caminho da interface Swagger
          )

# Namespace para a API de treinamento
ns = api.namespace('ml', description='Operações relacionadas a Machine Learning')

# Definir o modelo de entrada no Swagger (sem exemplos de hiperparâmetros)
train_model_payload = ns.model('TrainModel', {
    'algorithm': fields.String(required=True, description='O algoritmo a ser utilizado (ex: RandomForest, SVM)'),
    'train_size': fields.Float(required=True, description='Porcentagem dos dados a serem utilizados para treino'),
    'hyperparams': fields.Raw(description='Hiperparâmetros opcionais do modelo, variando de acordo com o algoritmo',
                              required=False)
})


# Rota para treinar o modelo
@ns.route('/model/train')
class TrainModel(Resource):
    @ns.doc('train_model')
    @ns.expect(train_model_payload)
    def post(self):

        # Obter os parâmetros da requisição
        data = request.get_json()
        algorithm = data.get('algorithm')
        train_size = data.get('train_size')

        # Se não forem fornecidos hiperparâmetros, usar um dicionário vazio
        hyperparams = data.get('hyperparams', {})

        # Chamar a função da biblioteca para treinar o modelo
        result = train_model(algorithm, train_size, hyperparams)

        # Retornar o resultado (nome do modelo e métricas)
        return result, 200

# Modelo para a predição no Swagger
predict_payload = ns.model('PredictPayload', {
    'input_data': fields.List(fields.List(fields.Float), required=True, description='Dados de entrada para a predição')
})

# Diretório onde os modelos são salvos
MODEL_DIR = '../saved_models'

# Função para listar os modelos
def list_saved_models():
    if not os.path.exists(MODEL_DIR):
        return []
    # Remover a extensão '.pkl' ao listar os modelos
    return [os.path.splitext(f)[0] for f in os.listdir(MODEL_DIR) if f.endswith('.pkl')]

# Função para carregar o modelo salvo
def load_model(model_name):
    model_path = os.path.join(MODEL_DIR, model_name + '.pkl')
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# Rota para listar os modelos existentes
@ns.route('/models')
class ListModels(Resource):
    @ns.doc('list_models')
    def get(self):
        """
        Lista todos os modelos salvos no diretório de modelos.
        """
        models = list_saved_models()
        if not models:
            return jsonify({'message': 'Nenhum modelo encontrado'})
        return jsonify({'models': models})

# Rota para fazer predições com um modelo treinado, passando os dados no body
@ns.route('/model/predict/<string:model_name>')
class PredictModel(Resource):
    @ns.doc('predict_model')
    @ns.expect(predict_payload)
    def post(self, model_name):
        """
        Faz predições usando um modelo existente, com os dados de entrada no body da requisição
        """
        # Carregar o modelo
        model = load_model(model_name)
        if model is None:
            return jsonify({'error': 'Modelo não encontrado'}), 404

        # Obter os dados de entrada do corpo da requisição
        data = request.get_json()
        input_data = data.get('input_data')

        if not input_data:
            return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

        try:
            # Realizar a predição com os dados fornecidos
            predictions = model.predict(input_data)
            return jsonify({'predictions': predictions.tolist()})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)