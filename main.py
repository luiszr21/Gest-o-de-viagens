import sys
from CRUDs.viagens import *
from CRUDs.reservas import *
from CRUDs.pesquisa import pesquisa_avancada_viagens
from utils.graficos import grafico_viagens, grafico_reservas

def menu():
    print("\n" + "="*60)
    print("SISTEMA DE GESTÃO DE VIAGENS")
    print("="*60)
    print("1  - Listar viagens")
    print("2  - Criar viagem")
    print("3  - Atualizar viagem")
    print("4  - Deletar viagem")
    print("5  - Listar reservas")
    print("6  - Criar reserva")
    print("7  - Atualizar reserva")
    print("8  - Deletar reserva")
    print("9  - Pesquisa avançada de viagens")
    print("10 - Gráfico: Viagens por destino")
    
    print("\n0  - Sair")
    print("="*60)
    return input("\nEscolha uma opção: ")

def main():
    print("\nIniciando Sistema de Gestão de Viagens...")
    print("Conectando à API em http://localhost:3000")
    
    while True:
        op = menu()

        if op == "1":
            df = listar_viagens()
        elif op == "2":
            criar_viagem()
        elif op == "3":
            atualizar_viagem()
        elif op == "4":
            deletar_viagem()
        
        elif op == "5":
            df = listar_reservas()
        elif op == "6":
            criar_reserva()
        elif op == "7":
            atualizar_reserva()
        elif op == "8":
            deletar_reserva()
        
        elif op == "9":
            pesquisa_avancada_viagens()
        
        elif op == "10":
            df = listar_viagens()
            if df is not None and not df.empty:
                grafico_viagens(df)
        
         
        elif op == "0":
            print("\nFinalizando sistema...")
            print("Obrigado por usar o Sistema de Gestão de Viagens!")
            sys.exit()
        
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
