import re
import csv
import pandas as pd
from googletrans import Translator
import nltk
nltk.download('movie_reviews')
nltk.download('punkt')
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#Canal de Referencia para utilizar algoritimo Textblob
#Ciência dos Dados - https://www.youtube.com/channel/UCd3ThZLzVDDnKSZMsbK0icg
#Canal de Referencia para utilizar API Google Translate Python
#Papa Thalyson - https://www.youtube.com/channel/UCU_UvuruXP7DmQy62k_Bv1w
#Canal de Referencia para usar pandas
#Programe Python - https://www.youtube.com/channel/UCScH4esOy2vcg2-iy-1UqQQ
#Tito Spadini - https://www.youtube.com/channel/UC2b8NHlgDnG-tA-gjN97vvg
#Hashtag Treinamentos - https://www.youtube.com/c/HashtagTreinamentos/featured

#Importando base e traduzindo
def Traduzir_Base():

    # Ler base twitter extraida do RPA
    data = pd.read_csv('ScrapperTwitterBase.csv', sep=';', encoding='utf-8')

    # Cria nova Coluna para traduzir textos e joga em data frame diferente
    data['Texto_Traduz'] = "0"
    df_NewData = data

    # Remove Caracteres indejesados no texto do tweet
    # Total de linhas do CSV para looping (Realiza -1 pois vetor contem valor na linha "0")
    x = int(len(df_NewData.index))
    x = x - 1

    # Converte linha a linha do DataFrame para Ingles
    while x >= 0:
        df_NewData.iat[x, 3] = limpando_chars(df_NewData.iat[x, 3])
        x = x - 1

    # Total de linhas do CSV para looping (Realiza -1 pois vetor contem valor na linha "0")
    x = int(len(df_NewData.index))
    x = x - 1

    # Traduzir palavras do Tweet para Ingles
    trans = Translator(service_urls=['translate.googleapis.com'])

    # Converte linha a linha do DataFrame para Ingles
    while x >= 0:
        df_NewData.iat[x, 7] = trans.translate(str(data.iat[x, 3]), dest="en").text
        x = x - 1

    # Testa para ver funcionalidade do looping
    # df_NewData.head()
    # df_NewData.iat[0,3]

    #Chama analise sentimentos Textblob
    print('Traduzindo Bases')
    Analise_sentimentos_textblob(df_NewData)

def limpando_chars(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) #removendo @
    text = re.sub('#', '', text) #removendo #
    text = re.sub('RT[\s]+', '', text) # Removendo RT
    text = re.sub('https?:\/\/\S+', '', text) # Removendo hyperlink
    text = re.sub('&amp','', text)# removendo marcação HTML de início
    return text

def Analise_sentimentos_textblob(df_NewData):
    # Analise de Sentimento utilizando BLOB
    print('Limpando textos da base')
    # Variavel para looping dentro do while com qtd de linhas da base
    x = int(len(df_NewData.index))
    x = x - 1

    # Cria 3 novas colunas para adicionar resultado da analise de sentimentos
    df_NewData['Classificação_Blob'] = "0"
    df_NewData['percent_pos_blob'] = "0"
    df_NewData['percent_neg_blob'] = "0"

    while x >= 0:
        # Retira texto do DataFrame e coloca em função de analise de sentimentos
        texto = df_NewData.iat[x, 7]
        blob = TextBlob(texto, analyzer=NaiveBayesAnalyzer())
        # Verifica Classificação de sentimentos
        blob.sentiment
        df_NewData.iat[x, 8] = blob.sentiment.classification
        df_NewData.iat[x, 9] = blob.sentiment.p_pos
        df_NewData.iat[x, 10] = blob.sentiment.p_neg
        x = x - 1

    # df_NewData.iat[1,3]
    df_NewData.head()

    #Salva CSV
    df_NewData.to_csv("Analise_Sentimentos_Base.csv", sep=';', encoding='utf-8', index=False)
    print('Analise de sentimentos concluida, exportando base')

def Executa_AnaliseSentimentos_TextBlob():
    Traduzir_Base()

