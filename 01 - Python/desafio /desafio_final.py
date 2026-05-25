from contato_com_llm import gerar_json
import json

reviews = []

with open("Resenhas_App_ChatGPT.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        reviews.append(linha.strip())

def listar_reviews():
    lista_reviews = []

    for review in reviews:
        review_estruturada = gerar_json(review).replace("```json", "").replace("```", "")
        review_em_json = json.loads(review_estruturada)
        lista_reviews.append(review_em_json)

    return lista_reviews

def contar_avaliacoes(lista_reviews):
    positiva = 0
    negativa = 0
    neutra = 0
    for review in lista_reviews:
        avaliacao = review['avaliacao']
        
        if avaliacao == "positiva":
            positiva += 1
        elif avaliacao == "negativa":
            negativa += 1
        else:
            neutra += 1

    return f"positivas: {positiva}\nnegativas: {negativa}\nneutras: {neutra}"

def unir_items(lista_reviews):
    lista_reviews_str = []

    for review in lista_reviews:
        review = str(review)
        lista_reviews_str.append(review)
    
    return "####".join(lista_reviews_str)

def main():
    lista_reviews = listar_reviews()
    contagem_avaliacoes = contar_avaliacoes(lista_reviews)
    uniao_items = unir_items(lista_reviews)
    print(contagem_avaliacoes)
    print(uniao_items)

main()