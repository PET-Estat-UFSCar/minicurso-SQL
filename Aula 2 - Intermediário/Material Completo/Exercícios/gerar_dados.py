"""
Gera o banco SQLite usado na Aula 2 do minicurso de SQL.

Arquivos:
    gerar_banco.py
    minicurso_aula2.db

Estrutura:
    clientes
    pedidos
    produtos
    itens_pedido

A base é propositalmente maior do que a usada na apresentação:
    - 100 clientes
    - 250 pedidos
    - 40 produtos
    - aproximadamente 800 itens de pedido

Também existem casos didáticos intencionais:
    - clientes sem nenhum pedido;
    - produtos nunca vendidos;
    - clientes com vários pedidos;
    - produtos presentes em muitos pedidos.

Como executar:
    python gerar_banco.py
"""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


CAMINHO_BANCO = Path("minicurso_aula2.db")
SEMENTE = 42

N_CLIENTES = 100
N_PEDIDOS = 250
N_PRODUTOS = 40

# Os últimos clientes ficam sem pedido.
N_CLIENTES_ATIVOS = 90

# Os últimos produtos ficam sem venda.
N_PRODUTOS_VENDIDOS = 35


PRIMEIROS_NOMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elisa", "Fernanda", "Gabriel", "Helena",
    "Igor", "Julia", "Kaique", "Larissa", "Marcos", "Natalia", "Otavio", "Paula",
    "Rafael", "Sabrina", "Tiago", "Vanessa", "Wesley", "Yasmin", "Alice", "Beatriz",
    "Caio", "Daniel", "Eduarda", "Felipe", "Giovana", "Henrique",
]

SOBRENOMES = [
    "Silva", "Souza", "Oliveira", "Santos", "Pereira", "Costa", "Rodrigues",
    "Almeida", "Nascimento", "Lima", "Araújo", "Fernandes", "Carvalho", "Gomes",
    "Martins", "Rocha", "Ribeiro", "Alves", "Monteiro", "Mendes",
]

CIDADES = [
    "São Carlos",
    "Campinas",
    "São Paulo",
    "Araraquara",
    "Ribeirão Preto",
    "Sorocaba",
    "Bauru",
    "Piracicaba",
    "Rio Claro",
    "Limeira",
]

CATEGORIAS = {
    "Periféricos": [
        "Teclado", "Mouse", "Webcam", "Headset", "Mousepad",
        "Microfone", "Controle", "Hub USB",
    ],
    "Computadores": [
        "Notebook", "Mini PC", "Desktop", "Chromebook",
    ],
    "Monitores": [
        "Monitor 24", "Monitor 27", "Monitor Ultrawide", "Monitor 4K",
    ],
    "Acessórios": [
        "Suporte para Notebook", "Suporte para Monitor", "Cabo HDMI",
        "Cabo USB-C", "Carregador", "Adaptador USB-C", "Filtro de Linha",
        "Mochila para Notebook",
    ],
    "Armazenamento": [
        "SSD 500GB", "SSD 1TB", "HD Externo 1TB", "Pen Drive 64GB",
    ],
    "Rede": [
        "Roteador", "Switch", "Adaptador Wi-Fi", "Cabo de Rede",
    ],
    "Áudio": [
        "Caixa de Som", "Fone Bluetooth", "Soundbar", "DAC USB",
    ],
}


def gerar_clientes():
    """Gera 100 clientes com nomes e cidades variadas."""
    clientes = []

    combinacoes = [
        f"{primeiro} {sobrenome}"
        for primeiro in PRIMEIROS_NOMES
        for sobrenome in SOBRENOMES
    ]

    random.shuffle(combinacoes)

    for id_cliente in range(1, N_CLIENTES + 1):
        nome = combinacoes[id_cliente - 1]
        cidade = random.choice(CIDADES)

        clientes.append(
            (id_cliente, nome, cidade)
        )

    return clientes


def gerar_produtos():
    """Gera 40 produtos distribuídos em várias categorias."""
    catalogo = []

    for categoria, nomes in CATEGORIAS.items():
        for nome in nomes:
            catalogo.append((nome, categoria))

    # Caso o catálogo tenha menos de 40 itens, completa com produtos genéricos.
    contador = 1
    while len(catalogo) < N_PRODUTOS:
        catalogo.append(
            (f"Produto {contador}", "Outros")
        )
        contador += 1

    random.shuffle(catalogo)
    catalogo = catalogo[:N_PRODUTOS]

    produtos = []

    for id_produto, (nome, categoria) in enumerate(catalogo, start=1):
        preco = round(
            random.uniform(30, 4500),
            2
        )

        produtos.append(
            (id_produto, nome, categoria, preco)
        )

    return produtos


def gerar_pedidos():
    """
    Gera 250 pedidos.

    Os primeiros 90 clientes recebem pelo menos um pedido.
    Assim, exatamente 10 clientes ficam propositalmente sem pedido.
    """
    pedidos = []

    inicio = date(2026, 1, 1)
    fim = date(2026, 9, 30)
    intervalo = (fim - inicio).days

    id_pedido = 1

    # Garante pelo menos um pedido para cada cliente ativo.
    for cliente in range(1, N_CLIENTES_ATIVOS + 1):
        data_pedido = inicio + timedelta(
            days=random.randint(0, intervalo)
        )

        pedidos.append(
            (
                id_pedido,
                cliente,
                data_pedido.isoformat(),
            )
        )

        id_pedido += 1

    # Completa o restante dos 250 pedidos de forma aleatória.
    while id_pedido <= N_PEDIDOS:
        cliente = random.randint(
            1,
            N_CLIENTES_ATIVOS
        )

        data_pedido = inicio + timedelta(
            days=random.randint(0, intervalo)
        )

        pedidos.append(
            (
                id_pedido,
                cliente,
                data_pedido.isoformat(),
            )
        )

        id_pedido += 1

    return pedidos


def gerar_itens_pedido():
    """
    Gera aproximadamente 800 itens.

    Cada pedido recebe de 2 a 5 produtos diferentes.
    Apenas os primeiros 35 produtos podem ser vendidos,
    deixando 5 produtos sem nenhuma venda.
    """
    itens = []

    produtos_vendidos = list(
        range(1, N_PRODUTOS_VENDIDOS + 1)
    )

    for id_pedido in range(1, N_PEDIDOS + 1):
        quantidade_produtos = random.randint(
            2,
            5
        )

        produtos_do_pedido = random.sample(
            produtos_vendidos,
            quantidade_produtos,
        )

        for id_produto in produtos_do_pedido:
            quantidade = random.randint(
                1,
                4
            )

            itens.append(
                (
                    id_pedido,
                    id_produto,
                    quantidade,
                )
            )

    return itens


def criar_banco(caminho_banco: Path = CAMINHO_BANCO):
    """Cria do zero o banco SQLite do minicurso."""

    random.seed(SEMENTE)

    if caminho_banco.exists():
        caminho_banco.unlink()

    conexao = sqlite3.connect(
        caminho_banco
    )

    cursor = conexao.cursor()

    cursor.execute(
        "PRAGMA foreign_keys = ON"
    )

    cursor.executescript(
        """
        CREATE TABLE clientes (
            id_cliente INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL
        );

        CREATE TABLE pedidos (
            id_pedido INTEGER PRIMARY KEY,
            id_cliente INTEGER NOT NULL,
            data_pedido TEXT NOT NULL,

            FOREIGN KEY (id_cliente)
                REFERENCES clientes(id_cliente)
        );

        CREATE TABLE produtos (
            id_produto INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL
        );

        CREATE TABLE itens_pedido (
            id_pedido INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,

            PRIMARY KEY (
                id_pedido,
                id_produto
            ),

            FOREIGN KEY (id_pedido)
                REFERENCES pedidos(id_pedido),

            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto)
        );
        """
    )

    clientes = gerar_clientes()
    produtos = gerar_produtos()
    pedidos = gerar_pedidos()
    itens_pedido = gerar_itens_pedido()

    cursor.executemany(
        """
        INSERT INTO clientes (
            id_cliente,
            nome,
            cidade
        )
        VALUES (?, ?, ?)
        """,
        clientes,
    )

    cursor.executemany(
        """
        INSERT INTO produtos (
            id_produto,
            nome,
            categoria,
            preco
        )
        VALUES (?, ?, ?, ?)
        """,
        produtos,
    )

    cursor.executemany(
        """
        INSERT INTO pedidos (
            id_pedido,
            id_cliente,
            data_pedido
        )
        VALUES (?, ?, ?)
        """,
        pedidos,
    )

    cursor.executemany(
        """
        INSERT INTO itens_pedido (
            id_pedido,
            id_produto,
            quantidade
        )
        VALUES (?, ?, ?)
        """,
        itens_pedido,
    )

    conexao.commit()

    # Pequeno resumo para quem executar o script.
    cursor.execute(
        "SELECT COUNT(*) FROM clientes"
    )
    total_clientes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM pedidos"
    )
    total_pedidos = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM produtos"
    )
    total_produtos = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM itens_pedido"
    )
    total_itens = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM clientes
        LEFT JOIN pedidos
            ON clientes.id_cliente = pedidos.id_cliente
        WHERE pedidos.id_pedido IS NULL
        """
    )
    clientes_sem_pedido = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM produtos
        LEFT JOIN itens_pedido
            ON produtos.id_produto = itens_pedido.id_produto
        WHERE itens_pedido.id_produto IS NULL
        """
    )
    produtos_sem_venda = cursor.fetchone()[0]

    conexao.close()

    print()
    print("Banco criado com sucesso!")
    print(f"Arquivo: {caminho_banco.resolve()}")
    print()
    print("Resumo da base:")
    print(f"  Clientes: {total_clientes}")
    print(f"  Pedidos: {total_pedidos}")
    print(f"  Produtos: {total_produtos}")
    print(f"  Itens de pedido: {total_itens}")
    print(f"  Clientes sem pedido: {clientes_sem_pedido}")
    print(f"  Produtos sem venda: {produtos_sem_venda}")
    print()


if __name__ == "__main__":
    criar_banco()
