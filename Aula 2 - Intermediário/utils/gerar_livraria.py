"""Gera o banco dos exercícios da Aula 2, com autores e livros fictícios.

Execute na pasta Aula 2 - Intermediário: python utils/gerar_livraria.py
"""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parents[1] / "livraria_aula2.db"


def criar_banco(caminho_banco=CAMINHO_BANCO):
    """Cria o banco da livraria; use um caminho novo para gerar outra cópia."""
    rng = random.Random(42)
    nomes = [
        "Ana Ribeiro", "Bruno Santos", "Carla Mendes", "Diego Costa",
        "Elisa Rocha", "Felipe Lima", "Gabriela Alves", "Henrique Dias",
        "Isabela Duarte", "João Martins", "Larissa Nunes", "Marcos Vieira",
        "Natalia Lopes", "Otavio Souza", "Paula Fernandes", "Rafael Gomes",
        "Sabrina Melo", "Tiago Barros", "Vanessa Pinto", "Wesley Castro",
    ]
    paises = ["Brasil", "Portugal", "Angola", "Moçambique", "Cabo Verde"]
    autores = [(i, nome, paises[(i - 1) % len(paises)]) for i, nome in enumerate(nomes, 1)]
    titulos = [
        "A cidade de papel", "O mapa das estrelas", "Cartas de inverno",
        "A última estação", "O jardim secreto do tempo", "Caminhos de areia",
        "O farol azul", "Memórias de um amanhã", "A ponte entre mundos",
        "O silêncio da praça", "As chaves do castelo", "Depois da chuva",
        "O viajante das nuvens", "Pequenos universos", "A casa do vento",
        "O relógio sem ponteiros", "Entre rios e montanhas", "O espelho da lua",
        "A biblioteca das marés", "O nome das flores", "O canto da cidade",
        "A ilha distante", "O segredo do observatório", "Páginas de outubro",
        "O trem da madrugada", "A estrada de vidro", "Versos para o mar",
        "O céu de outro planeta", "A janela amarela", "O inverno das cartas",
        "A sombra do jardim", "O último cometa", "Palavras ao entardecer",
        "A travessia do bosque", "O planeta das memórias", "O retrato perdido",
        "A noite dos vaga-lumes", "O rio que voltava", "Fragmentos de sol",
        "A estação das descobertas",
    ]
    generos = ["Romance", "Fantasia", "Suspense", "Poesia", "Ficção científica"]
    # Os autores 18, 19 e 20 ficam sem livros.
    livros = [
        (i, (i - 1) % 17 + 1, titulo, generos[(i - 1) % len(generos)], round(rng.uniform(25, 150), 2))
        for i, titulo in enumerate(titulos, 1)
    ]
    inicio = date(2026, 1, 1)
    pedidos = [(i, (inicio + timedelta(days=rng.randrange(273))).isoformat()) for i in range(1, 251)]
    itens = []
    for id_pedido in range(1, 251):
        # Apenas os livros 1 a 35 são vendidos; os últimos cinco ficam sem venda.
        escolhidos = rng.sample(range(1, 36), rng.randint(2, 5))
        # Garante que cada um dos primeiros 35 livros aparece ao menos uma vez.
        if id_pedido <= 35 and id_pedido not in escolhidos:
            escolhidos[0] = id_pedido
        itens.extend((id_pedido, id_livro, rng.randint(1, 4)) for id_livro in escolhidos)

    caminho_banco = Path(caminho_banco)
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.executescript("""
    CREATE TABLE autores (
        id_autor INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        pais TEXT NOT NULL
    );
    CREATE TABLE livros (
        id_livro INTEGER PRIMARY KEY,
        id_autor INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        genero TEXT NOT NULL,
        preco REAL NOT NULL,
        FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
    );
    CREATE TABLE pedidos (
        id_pedido INTEGER PRIMARY KEY,
        data_pedido TEXT NOT NULL
    );
    CREATE TABLE itens_pedido (
        id_pedido INTEGER NOT NULL,
        id_livro INTEGER NOT NULL,
        quantidade INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (id_pedido, id_livro),
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
        FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
    );
    """)
    cursor.executemany("INSERT INTO autores VALUES (?, ?, ?)", autores)
    cursor.executemany("INSERT INTO livros VALUES (?, ?, ?, ?, ?)", livros)
    cursor.executemany("INSERT INTO pedidos VALUES (?, ?)", pedidos)
    cursor.executemany("INSERT INTO itens_pedido VALUES (?, ?, ?)", itens)
    conexao.commit()
    conexao.close()
    return {"autores": len(autores), "livros": len(livros), "pedidos": len(pedidos), "itens_pedido": len(itens)}


if __name__ == "__main__":
    print("Banco criado:", CAMINHO_BANCO)
    print(criar_banco())
