import json
import requests

API_URL = "https://www.themealdb.com/api/json/v1/1/search.php"

TRADUCOES = {
    "frango": "chicken",
    "frango assado": "roast chicken",
    "carne": "beef",
    "carne bovina": "beef",
    "carne moída": "minced beef",
    "carne moida": "minced beef",
    "costela": "ribs",
    "linguiça": "sausage",
    "linguica": "sausage",
    "bacon": "bacon",
    "porco": "pork",
    "presunto": "ham",
    "peixe": "fish",
    "salmão": "salmon",
    "salmao": "salmon",
    "atum": "tuna",
    "camarão": "prawn",
    "camarao": "prawn",
    "caranguejo": "crab",
    "lagosta": "lobster",
    "ovo": "egg",
    "ovos": "egg",
    "arroz": "rice",
    "batata": "potato",
    "batata frita": "chips",
    "feijão": "beans",
    "feijao": "beans",
    "milho": "corn",
    "cenoura": "carrot",
    "brócolis": "broccoli",
    "brocolis": "broccoli",
    "tomate": "tomato",
    "cebola": "onion",
    "alho": "garlic",
    "queijo": "cheese",
    "pão": "bread",
    "pao": "bread",
    "leite": "milk",
    "macarrão": "pasta",
    "macarrao": "pasta",
    "espaguete": "spaghetti",
    "sanduíche": "sandwich",
    "sanduiche": "sandwich",
    "cachorro-quente": "hot dog",
    "cachorro quente": "hot dog",
    "pizza": "pizza",
    "hambúrguer": "burger",
    "hamburguer": "burger",
    "bolo": "cake",
    "bolo de chocolate": "chocolate cake",
    "chocolate": "chocolate",
    "brigadeiro": "chocolate truffles",
    "sorvete": "ice cream",
    "pudim": "pudding",
    "panqueca": "pancakes",
    "crepe": "crepes",
    "biscoito": "cookie",
    "biscoitos": "cookies",
    "torta": "pie",
    "salada": "salad",
    "sopa": "soup",
    "sushi": "sushi",
    "risoto": "risotto",
    "lasanha": "lasagna",
    "empada": "pie",
    "coxinha": "chicken croquettes",
    "pastel": "pastry",
    "feijoada": "feijoada",
}


def traduzir_comida(comida):
    return TRADUCOES.get(comida.lower(), comida)


def buscar_comidas(termo):
    try:
        resposta = requests.get(API_URL, params={"s": termo}, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.exceptions.RequestException as erro:
        print("Erro ao acessar a API:", erro)
        return []
    except ValueError:
        print("A API retornou um JSON inválido.")
        return []

    return dados.get("meals") or []


def salvar_e_mostrar_comida(comida):
    nome = comida.get("strMeal", "Prato sem nome")
    nome = nome.replace("Chicken", "Frango").replace("Sticky", "Agridoce")
    dados = [{
        "id": comida.get("idMeal"),
        "nome": nome,
        "video_receita": comida.get("strYoutube") or "Vídeo não disponível",
    }]

    with open("dados_api.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    print("\nDados da comida escolhida:")
    for item in dados:
        print(f"- Nome: {item['nome']}")
        print(f"- Vídeo da receita: {item['video_receita']}")
    print("Lista salva em dados_api.json.")


def recomendar_com_coca(comida):
    categoria = (comida.get("strCategory") or "").casefold()
    categorias_que_combinam = {"beef", "chicken", "dessert", "pork", "side", "starter"}
    if categoria in categorias_que_combinam:
        return "Combina com Coca-Cola!"
    return "Não combina com Coca-Cola."


def escolher_comida(comidas):
    print("\nComidas encontradas:")
    for indice, comida in enumerate(comidas, start=1):
        categoria = comida.get("strCategory") or "categoria não informada"
        print(f"{indice}. {comida.get('strMeal', 'Prato sem nome')} ({categoria})")

    while True:
        escolha = input("Digite o número da comida (ou 0 para cancelar): ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(comidas):
            return comidas[int(escolha) - 1]
        print("Opção inválida. Escolha um número da lista.")


def main():
    print("Idiomas disponíveis para consulta: Português e Inglês.")
    print("=== Coca combina? ===")
    while True:
        termo = input("\nQual comida você quer procurar? (ou digite 'sair'): ").strip()
        if termo.lower() == "sair":
            print("Aplicativo encerrado.")
            break
        if not termo:
            print("Digite o nome de uma comida.")
            continue

        termo_em_ingles = traduzir_comida(termo)
        if termo_em_ingles != termo:
            print(f"Buscando por: {termo_em_ingles}")

        comidas = buscar_comidas(termo_em_ingles)
        if not comidas:
            print("Nenhuma comida encontrada. Tente outra busca.")
            continue

        comida = escolher_comida(comidas)
        if comida is None:
            print("Busca cancelada.")
            continue

        resultado = recomendar_com_coca(comida)
        print(f"\n{comida.get('strMeal')}: {resultado}")
        salvar_e_mostrar_comida(comida)


if __name__ == "__main__":
    main()
