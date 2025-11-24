import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

# Lista de cores para alternar
cores = ["red", "green", "yellow", "blue", "magenta", "cyan", "bright_green", "bright_blue"]

def print_barras_coloridas(label, valor, max_val, cor="cyan", largura=60, casas_decimais=0):
    """
    Função auxiliar para imprimir barra colorida com espaçamento.
    Permite definir casas decimais para o valor (útil para preços).
    """
    if max_val == 0:
        bar_len = 0
    else:
        # Garante que a barra tenha pelo menos 1 de comprimento se o valor for maior que zero
        bar_len = max(int((valor / max_val) * largura), 1) if valor > 0 else 0
    
    # Formatação do valor para exibição
    if casas_decimais == 0:
        # Exibe como inteiro se casas_decimais for 0
        valor_str = str(int(valor)) 
    else:
        # Exibe com o número de casas decimais especificado
        valor_str = f"{valor:.{casas_decimais}f}"
    
    # Capitaliza o label para melhor exibição (ex: 'rio de janeiro' -> 'Rio De Janeiro')
    texto = Text(label.title().ljust(35))
    texto.append(" | ")
    texto.append("█" * bar_len, style=cor)
    texto.append(f" {valor_str}")
    console.print(texto)
    # Linha em branco para separar as barras
    # console.print() 


def grafico_viagens(df):
    """
    Agrupa os destinos pelo nome, soma quantidade e calcula preço médio,
    e imprime gráficos coloridos no terminal.
    """
    if df is None or df.empty:
        console.print("[red]❌ Sem dados para gráfico.[/red]")
        return

    # --- 💡 CORREÇÃO: NORMALIZAÇÃO DE DESTINO ---
    # Garante que a coluna seja string, remove espaços e converte para minúsculas
    # Isso faz com que 'Rio de Janeiro' e 'Rio de janeiro' sejam tratados como o mesmo destino.
    df['destino'] = df['destino'].astype(str).str.strip().str.lower()
    # ---------------------------------------------

    # Garantir que preco seja numérico
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

    # Agrupar por destino (agora padronizado): quantidade de viagens e preço médio
    resumo = df.groupby("destino", as_index=False).agg(
        quantidade=("id_viagem", "count"),
        preco_medio=("preco", "mean")
    ).round(2)

    # --- Tabela resumo ---
    table = Table(title="📊 Resumo de Viagens por Destino")
    table.add_column("Destino", justify="left")
    table.add_column("Quantidade", justify="center")
    table.add_column("Preço Médio (R$)", justify="center")
    for _, row in resumo.iterrows():
        preco_medio_str = f"{row['preco_medio']:.2f}" if pd.notna(row['preco_medio']) else "-"
        # Usa .title() para exibir o nome formatado na tabela
        table.add_row(row['destino'].title(), str(row['quantidade']), preco_medio_str)
    console.print(table)
    console.print("---") # Separador

    # --- Gráfico de barras de quantidade ---
    console.print("\n[bold cyan]📈 Gráfico de Quantidade por Destino[/bold cyan]\n")
    max_qtd = resumo['quantidade'].max()
    for i, row in resumo.iterrows():
        cor = cores[i % len(cores)]
        # casas_decimais=0 para quantidade
        print_barras_coloridas(row['destino'], row['quantidade'], max_qtd, cor, casas_decimais=0)

    console.print("\n---") # Separador

    # --- Gráfico de barras de preço médio ---
    console.print("\n[bold cyan]💰 Gráfico de Preço Médio por Destino (R$)[/bold cyan]\n")
    # Filtra apenas destinos com preço médio calculado (não NaN)
    resumo_preco = resumo.dropna(subset=['preco_medio']).reset_index(drop=True) 

    if not resumo_preco.empty:
        max_preco = resumo_preco['preco_medio'].max()
        for i, row in resumo_preco.iterrows():
            cor = cores[i % len(cores)]
            # casas_decimais=2 para preço
            print_barras_coloridas(row['destino'], row['preco_medio'], max_preco, cor, casas_decimais=2)
    else:
        console.print("[yellow]⚠️ Nenhum dado de preço disponível para gráfico.[/yellow]")

def grafico_reservas(df):
    """
    Mostra resumo de reservas no terminal com gráfico de barras coloridas por status.
    """
    if df is None or df.empty:
        console.print("[red]❌ Nenhuma reserva para gráfico.[/red]")
        return

    # Estatísticas gerais
    console.print(f"\n[bold cyan]--- Total de reservas: {len(df)} ---[/bold cyan]\n")

    # Por status
    if 'status' in df.columns:
        # value_counts() para uma contagem idiomática
        status_count_series = df['status'].value_counts()
        
        # Converte para DataFrame para iteração
        status_count = status_count_series.reset_index()
        status_count.columns = ['status', 'quantidade']
        
        console.print("[bold cyan]📊 Reservas por Status[/bold cyan]\n")
        max_status = status_count['quantidade'].max()
        for i, row in status_count.iterrows():
            cor = cores[i % len(cores)]
            # casas_decimais=0 para quantidade
            print_barras_coloridas(row['status'], row['quantidade'], max_status, cor, casas_decimais=0)
    else:
        console.print("[yellow]⚠️ A coluna 'status' não foi encontrada no DataFrame de reservas.[/yellow]")


# --- Exemplo de Uso para Teste (INCLUI DADOS REPETIDOS PARA MOSTRAR A CORREÇÃO) ---

console.print("\n" + "="*80)
console.print("[bold underline green]🚀 TESTE DA CORREÇÃO DE NORMALIZAÇÃO DE DESTINOS[/bold underline green]")
console.print("="*80)

# Criando um DataFrame de exemplo com erros de capitalização e espaçamento
dados_viagens_teste = {
    'id_viagem': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    # Duplicações intencionais com case e espaços diferentes:
    'destino': ['Rio de Janeiro', 'Londres', 'rio de janeiro ', 'Roma', ' Londres', 'Paris', 'roma', 'Berlim', 'Rio de Janeiro'],
    'preco': [1500.50, 1200.00, 1600.50, 900.00, 1300.00, 1450.00, 950.00, 800.00, 1700.00]
}
df_viagens_teste = pd.DataFrame(dados_viagens_teste)

grafico_viagens(df_viagens_teste)