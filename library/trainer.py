import os
import pickle
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from models.get_model import get_model

# Função para gerar o nome do arquivo com base no algoritmo e na data/hora
def generate_model_name(algorithm):
    """
    Gera o nome do modelo no formato: algoritmo_datetime.pkl
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{algorithm}_{timestamp}.pkl"

# Função para treinar o modelo e calcular métricas
def train_model(algorithm, train_size, hyperparams):
    """
    Função para treinar um modelo com os parâmetros fornecidos e retornar métricas.

    :param algorithm: Algoritmo a ser usado (ex: RandomForest, SVM)
    :param train_size: Percentual dos dados para treino
    :param hyperparams: Dicionário de hiperparâmetros para o modelo
    :return: Dicionário contendo o nome do modelo e as métricas calculadas
    """
    # Carregar o dataset Iris (dados reais)
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Dividir os dados em treino e teste com base no percentual de treino especificado
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=42)

    # Obter o modelo agnóstico com base no algoritmo e hiperparâmetros fornecidos
    model = get_model(algorithm, **hyperparams)

    # Treinar o modelo
    model.fit(X_train, y_train)

    # Fazer previsões nos dados de teste
    y_pred = model.predict(X_test)

    # Calcular as métricas de avaliação
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Gerar o nome do arquivo de modelo
    model_file_name = generate_model_name(algorithm)

    # Criar o diretório `saved_models/` se ele não existir
    model_dir = '../saved_models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Caminho completo para salvar o modelo
    model_path = os.path.join(model_dir, model_file_name)

    # Salvar o modelo treinado com o nome especificado
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    # Retornar o nome do modelo e as métricas de avaliação
    return {
        'model_file_name': model_file_name,
        'metrics': {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    }
