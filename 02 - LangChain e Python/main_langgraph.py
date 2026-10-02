from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
import asyncio

modelo = ChatOpenAI(
    model = 'local-model',
    base_url = 'http://127.0.0.1:1234/v1',
    api_key = 'lm-studio'
)

prompt_consultor_praias = ChatPromptTemplate.from_messages(
    [
        ('system', 'Você é um consultor de viagens especializado em praias. Você se chama Sr. Praia e deve se apresentar'),
        ('user', '{pergunta}')
    ],
)

prompt_consultor_montanhas = ChatPromptTemplate.from_messages(
    [
        ('system', 'Você é um consultor de viagens especializado em montanhas. Você se chama Sr. Montanha e deve se apresentar'),
        ('user', '{pergunta}')
    ],
)

cadeia_praias = prompt_consultor_praias | modelo | StrOutputParser()
cadeia_montanhas = prompt_consultor_montanhas| modelo | StrOutputParser()

class Rota(TypedDict):
    destino: Literal['praia', 'montanha']

prompt_roteador = ChatPromptTemplate.from_messages(
    [
        ('system', 'Responda apenas com praia ou montanha'),
        ('user', '{pergunta}')
    ]
)

roteador = prompt_roteador | modelo.with_structured_output(Rota)

class Estado(TypedDict):
    pergunta: str
    destino: Rota
    resposta: str

async def no_roteador(estado: Estado, config: RunnableConfig):
    return {'destino': await roteador.ainvoke({'pergunta': estado['pergunta']}, config)}

async def no_praias(estado: Estado, config: RunnableConfig):
    return {'resposta': await cadeia_praias.ainvoke({'pergunta': estado['pergunta']}, config)}

async def no_montanhas(estado: Estado, config: RunnableConfig):
    return {'resposta': await cadeia_montanhas.ainvoke({'pergunta': estado['pergunta']}, config)}

def escolher_no(estado: Estado) -> Literal['praia', 'montanha']:
    return 'praia' if estado['destino']['destino'] == 'praia' else 'montanha'

grafo = StateGraph(Estado)
grafo.add_node('rotear', no_roteador)
grafo.add_node('praia', no_praias)
grafo.add_node('montanha', no_montanhas)

grafo.add_edge(START, 'rotear')
grafo.add_conditional_edges('rotear', escolher_no)
grafo.add_edge('praia', END)
grafo.add_edge('montanha', END)

app = grafo.compile()

async def main():
    resposta = await app.ainvoke(
        {'pergunta': 'Quero visitar um lugar  no Brasil famoso por praias e culturas'}
    )

    print(resposta['resposta'])

asyncio.run(main())