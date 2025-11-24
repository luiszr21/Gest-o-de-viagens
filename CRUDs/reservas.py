from utils.requester import api_request
from utils.tables import print_table, print_detailed


def listar_reservas():
    """Lista todas as reservas"""
    print("\n🔍 Buscando reservas...")
    data = api_request("GET", "/reservas")
    
    if not data:
        return None
    
    # Simplificar dados aninhados para tabela
    simplified = []
    for item in data:
        simple_item = {
            'id_reserva': item.get('id_reserva'),
            'data_reserva': item.get('data_reserva'),
            'status': item.get('status'),
            'id_cliente': item.get('id_cliente'),
            'cliente_nome': item.get('cliente', {}).get('nome', 'N/A') if isinstance(item.get('cliente'), dict) else 'N/A',
            'id_viagem': item.get('id_viagem')
        }
        simplified.append(simple_item)
    
    return print_table(simplified)


def criar_reserva():
    """Cria uma nova reserva"""
    print("\n" + "="*80)
    print("➕ CRIAR NOVA RESERVA")
    print("="*80)
    
    id_cliente = input("👤 ID do cliente: ")
    id_viagem = input("✈️  ID da viagem: ")
    email = input("📧 E-mail para confirmação: ")

    try:
        body = {
            "id_cliente": int(id_cliente),
            "id_viagem": int(id_viagem),
            "email": email
        }
    except ValueError:
        print("\n❌ Erro: IDs devem ser números!\n")
        return

    print("\n⏳ Criando reserva...")
    res = api_request("POST", "/reservas", json_body=body)
    
    if res:
        print("\n" + "="*80)
        print("✅ RESERVA CRIADA COM SUCESSO!")
        print("="*80)
        print_detailed([res], "NOVA RESERVA")


def atualizar_reserva():
    """Atualiza uma reserva existente"""
    print("\n" + "="*80)
    print("✏️  ATUALIZAR RESERVA")
    print("="*80)
    
    # Listar reservas primeiro
    listar_reservas()
    
    idr = input("\n🔢 ID da reserva para atualizar: ")
    
    print("\n📋 Status disponíveis: confirmada, cancelada, realizado")
    status = input("📊 Novo status: ")

    if not status:
        print("\n⚠️  Status não informado.")
        return

    print("\n⏳ Atualizando reserva...")
    res = api_request("PUT", f"/reservas/{idr}", json_body={"status": status})
    
    if res:
        print("\n✅ Reserva atualizada com sucesso!\n")


def deletar_reserva():
    """Deleta uma reserva"""
    print("\n" + "="*80)
    print("🗑️  DELETAR RESERVA")
    print("="*80)
    
    # Listar reservas primeiro
    listar_reservas()
    
    idr = input("\n🔢 ID da reserva para excluir: ")
    confirm = input("❓ Confirma a exclusão? (s/n): ").lower()
    
    if confirm == "s":
        print("\n⏳ Deletando reserva...")
        res = api_request("DELETE", f"/reservas/{idr}")
        
        if res is not None:
            print("\n✅ Reserva deletada com sucesso!\n")
    else:
        print("\n❌ Operação cancelada.\n")