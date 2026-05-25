from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

dias = 7
numero_criancas = 2
atividade = "música"

modelo_prompt = PromptTemplate(
    template="""
       Crie um roteiro de viagem para uma família que ficará {dias} dias fora,
       nesta família há {numero_criancas} crianças,
       a atividade preferida da família é {atividade}.
       """
)

prompt = modelo_prompt.format(
    dias = dias,
    numero_criancas = numero_criancas,
    atividade = atividade
)

modelo = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    model="google/gemma-3-1b",
    temperature=0.5, 
    api_key="lm-studio"
)

resposta = modelo.invoke(prompt)
print(resposta.content)