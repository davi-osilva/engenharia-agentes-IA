from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import Field, BaseModel

modelo = ChatOpenAI(
    model = 'local-model',
    base_url = 'http://127.0.0.1:1234/v1',
    api_key = 'lm-studio'
)

# cidade
class Cidade(BaseModel):
    cidade: str = Field(description='Nome da cidade')
    justificativa: str = Field(description='Justifique da escolha dessa cidade')

parser_cidade = JsonOutputParser(pydantic_object=Cidade)

prompt_cidade = PromptTemplate(
    template = """
        Quero visitar uma cidade com base no meu interesse de {interesse}.
        {formato}
    """,
    input_variables = ['interesse'],
    partial_variables = {'formato': parser_cidade.get_format_instructions()}
)

# restaurantes
class Restaurantes(BaseModel):
    cidade: str = Field(description='Nome da cidade')
    restaurantes: str = Field(description='Nome dos restaurantes')

parser_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

prompt_restaurantes = PromptTemplate(
    template = """
        Quero indicações de restaurantes nessa cidade: {cidade}.
        {formato}
    """,
    input_variables = ['cidade'],
    partial_variables = {'formato': parser_restaurantes.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template="""
        Quero indicações de eventos culturais na cidade {cidade}.
    """,
)

cadeia1 = prompt_cidade | modelo | parser_cidade
cadeia2 = prompt_restaurantes | modelo | parser_restaurantes
cadeia3 = prompt_cultural | modelo | StrOutputParser()

cadeia = cadeia1 | cadeia2 | cadeia3

resposta = cadeia.invoke(
    {
        'interesse': 'estatística'
    }
    )

print(resposta)