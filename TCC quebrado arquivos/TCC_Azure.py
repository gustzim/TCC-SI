from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import pandas as pd
from time import sleep
def Executa_AnaliseSentimentos_Azure():
    # Credenciais de acesso ao Azure
    '''credential = AzureKeyCredential("68729edcd6f24a149f4128d8506779ab")
    text_analytics_client = TextAnalyticsClient(endpoint="https://tccanalisesentimentosapi.cognitiveservices.azure.com/",
                                                credential=credential)'''
    credential = AzureKeyCredential("12c4d32457cd47a6b49602d3c7a73a8e")
    text_analytics_client = TextAnalyticsClient(endpoint="https://tcc2analisesentimentos.cognitiveservices.azure.com/",
        credential=credential)

    # Import de base para analise de sentimentos
    data = pd.read_csv('Analise_Sentimentos_Base.csv', low_memory=False, sep=';')

    indexNames = data[(data['percent_pos_blob'] == 0.500000)
                      & (data['percent_neg_blob'] == 0.500000)].index
    data.drop(indexNames, inplace=True)


    # Pega somente coluna com comentarios do twitter e passa para outro dataframe
    documents1 = data[['Texto']]

    # Cria 4 novas colunas para incluir resultados
    data['Azure_Sentiment'] = "0"
    data['Azure_percent_pos'] = "0"
    data['Azure_percent_neg'] = "0"
    data['Azure_percent_neutro'] = "0"

    #print(documents1)

    # conta total de linhas do DF, cria um vetor e coloca valores do DF dentro do Vetor

    # OBS: Azure não trabalha com Dataframe Pandas, somente com JSON ou Array, por isso é feito esta etapa
    x = int(len(documents1.index))
    x = x - 1
    print(x)
    y=0
    vetor = []
    while x >= 0:
        print(vetor)
        while y < 7:
            if x < 0:
                break
            print(x,y)
            vetor.append(documents1.iat[x, 0])
            # Chama função de analise de sentimentos AZURE e passa em cada linha do VETOR em loop
            # salva resultados no Dataframe original
            # Resultados em Ingles ou Portugues permanecem o mesmo, sendo esse parametro indiferente
            response = text_analytics_client.analyze_sentiment(vetor, language="pt")
            result = [doc for doc in response if not doc.is_error]

            for doc in result:
                print('__________________________________________________')
                data.iat[x, 11] = doc.sentiment
                data.iat[x, 12] = doc.confidence_scores.positive
                data.iat[x, 13] = doc.confidence_scores.negative
                data.iat[x, 14] = doc.confidence_scores.neutral
                print(f"Overall sentiment: {doc.sentiment}")
                print(
                    f"Scores: positive={doc.confidence_scores.positive}; "
                    f"neutral={doc.confidence_scores.neutral}; "
                    f"negative={doc.confidence_scores.negative}\n"
                )
                print(result)
                x = x - 1
                y = y + 1
                vetor.clear()
        if x > 0:
            y=0
        else:
            break

    #Salva CSV com resultados
    data.to_csv("Analise_Sentimentos_Base.csv", sep=';', encoding='utf-8', index=False)
