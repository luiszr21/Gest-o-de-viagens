from utils.requester import api_request
from utils.tables import print_table, print_detailed

def listar_viagens():
    print("\nBuscando viagens...")
    data = api_request("GET", "/viagens")
    
    if not data:
        print("Nenhuma viagem encontrada.")
        return None
    
    for item in data:
        if 'reservas' in item:
            item['qtd_reservas'] = len(item['reservas'])
            del item['reservas']
    
    return print_table(data)


def criar_viagem():
    print("\n=== CRIAR NOVA VIAGEM ===")
    
    destino = input("Destino: ")
    data_inicio = input("Data início (YYYY-MM-DD): ")
    data_fim = input("Data fim (YYYY-MM-DD): ")
    preco = float(input("Preço: ")) 

    body = {
        "destino": destino,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "preco": preco
    }

    print("\nCriando viagem...")
    res = api_request("POST", "/viagens", json_body=body)
    
    if res:
        print("\n✅ Viagem criada com sucesso!")
        print_detailed([res], "NOVA VIAGEM")


def atualizar_viagem():
    print("\n=== ATUALIZAR VIAGEM ===")
    
    listar_viagens()
    
    idv = input("\nID da viagem para atualizar: ")

    print("Deixe em branco para manter o valor atual")
    destino = input("Novo destino: ")
    data_inicio = input("Nova data início (YYYY-MM-DD): ")
    data_fim = input("Nova data fim (YYYY-MM-DD): ")
    preco = input("Novo preço: ")

    body = {}
    if destino: body["destino"] = destino
    if data_inicio: body["data_inicio"] = data_inicio
    if data_fim: body["data_fim"] = data_fim
    if preco: body["preco"] = float(preco)

    if not body:
        print("Nenhuma alteração informada.")
        return

    print("\nAtualizando viagem...")
    res = api_request("PUT", f"/viagens/{idv}", json_body=body)
    
    if res:
        print("\n✅ Viagem atualizada com sucesso!")


def deletar_viagem():
    print("\n=== DELETAR VIAGEM ===")
    
    listar_viagens()
    
    idv = input("\nID da viagem para deletar: ")
    
    confirm = input("Confirma a exclusão? (s/n): ").lower()

    if confirm == "s":
        print("\nDeletando viagem...")
        res = api_request("DELETE", f"/viagens/{idv}")
        
        if res:
            print("\n✅ Viagem deletada com sucesso!")
    else:
        print("\nOperação cancelada.")
