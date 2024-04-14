#GITHUB FLAIR: https://github.com/flairNLP/flair
#FONTE DE TUTORIAL PARA UTILIZAÇÃO FLAIR https://pub.towardsai.net/sentiment-analysis-without-modeling-textblob-vs-vader-vs-flair-657b7af855f4
#LIBNAME DE OPEN SOURCE
import pandas as pd
from flair.models import TextClassifier
classifier = TextClassifier.load('en-sentiment')
# Import flair Sentence para processo de input de textos
from flair.data import Sentence


def Executa_AnaliseSentimentos_Flair():
    #Importa base CSV com dados do twitter
    data = pd.read_csv('Analise_Sentimentos_Base.csv', low_memory=False, sep=';')
    #Cria 2 colunas para input de Valores
    data['Classificacao_flair'] = "0"
    data['percent_flair'] = "0"

    #le total de linhas da tabela
    x = int(len(data.index))
    x = x - 1

    #looping: seleciona ultima linha da tabela, realiza analise de sentimento
    #looping da ultima linha até a primeira linha
    #Vetor inicial = 0
    while x >= 0:
        texto = data.iat[x, 7]
        # Flair tokenization
        sentence = Sentence(texto)
        print(sentence)
        # Flair previsão de sentimento de comentarios traduzidos para ingles
        classifier.predict(sentence)
        print(sentence)
        data.iat[x, 15] = sentence.labels[0].value
        data.iat[x, 16] = sentence.labels[0].score
        x = x - 1

    #####Dataprep com analises de sentimento para gerar porcentagem final
    data['percent_pos_flar'] = 0
    data['percent_neg_flar'] = 0
    x = int(len(data.index))
    x = x - 1
    #Cria coluna com porcentagem negativa e positiva do Flair
    while x >= 0:
        if data.iat[x, 15] == 'NEGATIVE':
            data.iat[x, 17] = 1 - data.iat[x, 16]
            data.iat[x, 18] = data.iat[x, 16]
            x = x - 1
        else:
            data.iat[x, 17] = data.iat[x, 16]
            data.iat[x, 18] = 1 - data.iat[x, 16]
            x = x - 1
    #Exclui coluna de percentual padrão do flair
    data = data.drop(columns=['percent_flair'])
    data.head()
    #Cria coluna de media final utilizando media ponderada (Azure peso 4, Flair peso 3, TextBlob peso 1 )
    data['Percent_Media_final'] = (data['percent_pos_blob'] + (data['Azure_percent_pos'] * 4) + (
                data['percent_pos_flar'] * 2)) / 7
    #Cria coluna com classificação final para nosso modelo
    data['Class_final'] = '0'
    x = int(len(data.index))
    x = x - 1
    while x >= 0:
        if float(data.iat[x, 18]) > 0.65:
            data.iat[x, 19] = 'Positivo'
            x = x - 1
        elif float(data.iat[x, 18]) < 0.40:
            data.iat[x, 19] = 'Negativo'
            x = x - 1
        else:
            data.iat[x, 19] = 'Neutro'
            x = x - 1
    data.to_csv("Analise_Sentimentos_Base.csv", sep=';', encoding='utf-8', index=False)
    #print(data)