from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def gerar_json(review):
    conteudo = client.chat.completions.create(
        model="google/gemma-3-1b",
        messages=[
            {"role": "system", "content": "Especialista em converter textos em estruturas JSON"},
            {"role": "user", "content": f"""Responda com um texto na estrutura exata do JSON, cada uma 
            dessas reviews você cria um objeto com:
            -resenha original (sem traduzir ainda)
            -resenha_pt (agora traduzida em português),
            -avaliacao (decidir se a avaliação é positiva, negativa ou neutra). 
             
            Estrutura esperada:
            {{
            "resenha_original": "",
            "resenha_pt": "",
            "avaliacao": ""
            }}

            Essas são as reviews: {review}"""}
        ],
        temperature=0
    )

    resposta = conteudo.choices[0].message.content
    return resposta

