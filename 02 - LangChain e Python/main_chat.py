from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

modelo = ChatOpenAI(
    model='local-model',
    base_url='http://127.0.0.1:1234/v1',
    api_key='lm-studio'
)

perguntas = [
    'Quero visitar uma cidade brasileira. Preciso de sugestões',
    'Qual é a melhor época do ano para visitar essa cidade?'
]

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um guia especializado em cidades brasileiras'),
    ('placeholder', '{historico}'),
    ('human', '{query}')
])

cadeia = prompt | modelo | StrOutputParser()

memoria = {}
sessao = 'aula_alura'

def historico_por_sessao(session_id: str):
    if session_id not in memoria:
        memoria[session_id] = InMemoryChatMessageHistory()
    return memoria[session_id]

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=historico_por_sessao,
    input_messages_key='query',
    history_messages_key='historico'
)

for pergunta in perguntas:
    resposta = cadeia_com_memoria.invoke(
        {'query': pergunta},
        config={'configurable': {'session_id': sessao}}
    )
    print(f'Eu: {pergunta}')
    print(f'Chatbot: {resposta}')