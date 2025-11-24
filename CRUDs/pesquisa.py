from utils.requester import api_request
from utils.tables import print_table
import pandas as pd

def pesquisa_avancada_viagens():
    """
    Pesquisa avançada com múltiplos filtros:
    - Destino (texto parcial)
    - Preço máximo
    - Data início mínima
    """
    print("\n=== PESQUISA AVANÇADA DE VIAGENS ===")
    print("(Deixe em branco para não filtrar)")
    
    # Coletar filtros do usuário
    destino_busca = input("Parte do destino: ").strip().lower()
    preco_max = input("Preço máximo: ").strip()
    data_min = input("Data início mínima (YYYY-MM-DD): ").strip()
    
    # Buscar todas as viagens da API
    data = api_request("GET", "/viagens")
    
    if not data:
        print("Nenhuma viagem encontrada.")
        return None
    
    # Converter para DataFrame para facilitar filtragem
    df = pd.DataFrame(data)
    
    # Aplicar filtros
    resultados = df.copy()
    
    # Filtro 1: Destino (busca parcial, case-insensitive)
    if destino_busca:
        resultados = resultados[
            resultados["destino"].str.lower().str.contains(destino_busca, na=False)
        ]
    
    # Filtro 2: Preço máximo
    if preco_max:
        try:
            preco_max_float = float(preco_max)
            resultados["preco"] = pd.to_numeric(resultados["preco"], errors="coerce")
            resultados = resultados[resultados["preco"] <= preco_max_float]
        except ValueError:
            print("⚠️ Preço inválido, ignorando esse filtro.")
    
    # Filtro 3: Data início mínima (CORRIGIDO PARA TIMEZONE)
    if data_min:
        try:
            # Converter coluna para datetime UTC
            resultados["data_inicio"] = pd.to_datetime(resultados["data_inicio"], utc=True)
            # Converter data de busca para UTC também
            data_min_dt = pd.to_datetime(data_min, utc=True)
            resultados = resultados[resultados["data_inicio"] >= data_min_dt]
        except Exception as e:
            print(f"⚠️ Erro ao processar data: {e}")
            print("Ignorando filtro de data.")
    
    # Exibir resultados
    if resultados.empty:
        print("\n❌ Nenhuma viagem encontrada com esses critérios.")
        return None
    
    print(f"\n✅ Encontradas {len(resultados)} viagens:")
    
    # Formatar datas para exibição (sem timezone no display)
    if "data_inicio" in resultados.columns:
        resultados["data_inicio"] = resultados["data_inicio"].dt.strftime('%Y-%m-%d')
    if "data_fim" in resultados.columns:
        resultados["data_fim"] = pd.to_datetime(resultados["data_fim"], utc=True).dt.strftime('%Y-%m-%d')
    
    print_table(resultados.to_dict('records'))
    
    return resultados


def pesquisa_avancada_reservas():
    """
    Pesquisa avançada de reservas com múltiplos filtros:
    - Status da reserva
    - ID do cliente
    - Data de reserva mínima
    """
    print("\n=== PESQUISA AVANÇADA DE RESERVAS ===")
    print("(Deixe em branco para não filtrar)")
    
    # Coletar filtros
    status_busca = input("Status (confirmada/cancelada/realizado): ").strip().lower()
    id_cliente = input("ID do cliente: ").strip()
    data_min = input("Data de reserva mínima (YYYY-MM-DD): ").strip()
    
    # Buscar todas as reservas
    data = api_request("GET", "/reservas")
    
    if not data:
        print("Nenhuma reserva encontrada.")
        return None
    
    df = pd.DataFrame(data)
    resultados = df.copy()
    
    # Filtro 1: Status
    if status_busca:
        resultados = resultados[
            resultados["status"].str.lower().str.contains(status_busca, na=False)
        ]
    
    # Filtro 2: ID do cliente
    if id_cliente:
        try:
            id_cliente_int = int(id_cliente)
            resultados = resultados[resultados["id_cliente"] == id_cliente_int]
        except ValueError:
            print("⚠️ ID inválido, ignorando esse filtro.")
    
    # Filtro 3: Data mínima (CORRIGIDO PARA TIMEZONE)
    if data_min:
        try:
            # Converter coluna para datetime UTC
            resultados["data_reserva"] = pd.to_datetime(resultados["data_reserva"], utc=True)
            # Converter data de busca para UTC
            data_min_dt = pd.to_datetime(data_min, utc=True)
            resultados = resultados[resultados["data_reserva"] >= data_min_dt]
        except Exception as e:
            print(f"⚠️ Erro ao processar data: {e}")
            print("Ignorando filtro de data.")
    
    # Exibir resultados
    if resultados.empty:
        print("\n❌ Nenhuma reserva encontrada com esses critérios.")
        return None
    
    print(f"\n✅ Encontradas {len(resultados)} reservas:")
    
    # Formatar data para exibição
    if "data_reserva" in resultados.columns:
        resultados["data_reserva"] = resultados["data_reserva"].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print_table(resultados.to_dict('records'))
    
    return resultados