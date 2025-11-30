from no import Node

def show_chain(node):
    print(f"\n=== Blockchain de {node.name} (tamanho: {len(node.blockchain.chain)}) ===")
    for b in node.blockchain.chain:
        print(f"Bloco {b.index}:")
        print(f"  Hash: {b.hash}")
        print(f"  Prev: {b.previous_hash}")
        print(f"  Nonce: {b.nonce}")
        print(f"  Transações: {b.transactions}")
    print()

def menu():
    print("\n--- MENU ---")
    print("1. Criar transação")
    print("2. Minerar bloco")
    print("3. Mostrar blockchain de todos os nós")
    print("4. Sair")
    return input("Escolha: ")

def main():
    # cria 3 nós da rede P2P
    n1 = Node("Nó A")
    n2 = Node("Nó B")
    n3 = Node("Nó C")

    nodes = [n1, n2, n3]

    # conectar os nós entre si
    for a in nodes:
        for b in nodes:
            if a is not b:
                a.connect_peer(b)

    print("\nRede blockchain inicializada com 3 nós!")

    while True:
        opc = menu()

        if opc == "1":
            print("\n--- Nova Transação ---")
            sender = input("Quem envia? ")
            receiver = input("Quem recebe? ")
            amt = float(input("Valor: "))

            # adiciona no nó A (poderia escolher o nó também)
            n1.add_transaction(sender, receiver, amt)
            print("Transação adicionada!")

        elif opc == "2":
            print("\nMinerando bloco no Nó A...")
            block = n1.mine()
            if block:
                print("Bloco minerado!")
                print("Hash:", block.hash)
            else:
                print("Nenhuma transação para minerar.")

        elif opc == "3":
            for n in nodes:
                show_chain(n)

        elif opc == "4":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
