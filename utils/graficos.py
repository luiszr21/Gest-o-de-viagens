import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

cores = ["red", "green", "yellow", "blue", "magenta", "cyan", "bright_green", "bright_blue"]

def print_barras_coloridas(label, valor, max_val, cor="cyan", largura=60, casas_decimais=0):
 
    if max_val == 0:
        bar_len = 0
    else:
        bar_len = max(int((valor / max_val) * largura), 1) if valor > 0 else 0
    
    if casas_decimais == 0:
        valor_str = str(int(valor)) 
    else:
        valor_str = f"{valor:.{casas_decimais}f}"
    
    texto = Text(label.title().ljust(35))
    texto.append(" | ")
    texto.append("█" * bar_len, style=cor)
    texto.append(f" {valor_str}")
    console.print(texto)



def grafico_viagens(df):
  
    if df is None or df.empty:
        console.print("[red]❌ Sem dados para gráfico.[/red]")
        return

   
    df['destino'] = df['destino'].astype(str).str.strip().str.lower()

    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

    resumo = df.groupby("destino", as_index=False).agg(
        quantidade=("id_viagem", "count"),
        preco_medio=("preco", "mean")
    ).round(2)

    table = Table(title="📊 Resumo de Viagens por Destino")
    table.add_column("Destino", justify="left")
    table.add_column("Quantidade", justify="center")
    table.add_column("Preço Médio (R$)", justify="center")
    for _, row in resumo.iterrows():
        preco_medio_str = f"{row['preco_medio']:.2f}" if pd.notna(row['preco_medio']) else "-"
        table.add_row(row['destino'].title(), str(row['quantidade']), preco_medio_str)
    console.print(table)
    console.print("---") 

    console.print("\n[bold cyan]📈 Gráfico de Quantidade por Destino[/bold cyan]\n")
    max_qtd = resumo['quantidade'].max()
    for i, row in resumo.iterrows():
        cor = cores[i % len(cores)]
        print_barras_coloridas(row['destino'], row['quantidade'], max_qtd, cor, casas_decimais=0)

    console.print("\n---") 

    console.print("\n[bold cyan]💰 Gráfico de Preço Médio por Destino (R$)[/bold cyan]\n")
    resumo_preco = resumo.dropna(subset=['preco_medio']).reset_index(drop=True) 

    if not resumo_preco.empty:
        max_preco = resumo_preco['preco_medio'].max()
        for i, row in resumo_preco.iterrows():
            cor = cores[i % len(cores)]
            print_barras_coloridas(row['destino'], row['preco_medio'], max_preco, cor, casas_decimais=2)
    else:
        console.print("[yellow]⚠️ Nenhum dado de preço disponível para gráfico.[/yellow]")

def grafico_reservas(df):
    
    if df is None or df.empty:
        console.print("[red]❌ Nenhuma reserva para gráfico.[/red]")
        return

    console.print(f"\n[bold cyan]--- Total de reservas: {len(df)} ---[/bold cyan]\n")

    if 'status' in df.columns:
        status_count_series = df['status'].value_counts()
        
        status_count = status_count_series.reset_index()
        status_count.columns = ['status', 'quantidade']
        
        console.print("[bold cyan]📊 Reservas por Status[/bold cyan]\n")
        max_status = status_count['quantidade'].max()
        for i, row in status_count.iterrows():
            cor = cores[i % len(cores)]
            print_barras_coloridas(row['status'], row['quantidade'], max_status, cor, casas_decimais=0)
    else:
        console.print("[yellow]⚠️ A coluna 'status' não foi encontrada no DataFrame de reservas.[/yellow]")



console.print("\n" + "="*80)
console.print("[bold underline green]🚀 TESTE DA CORREÇÃO DE NORMALIZAÇÃO DE DESTINOS[/bold underline green]")
console.print("="*80)

dados_viagens_teste = {
    'id_viagem': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'destino': ['Rio de Janeiro', 'Londres', 'rio de janeiro ', 'Roma', ' Londres', 'Paris', 'roma', 'Berlim', 'Rio de Janeiro'],
    'preco': [1500.50, 1200.00, 1600.50, 900.00, 1300.00, 1450.00, 950.00, 800.00, 1700.00]
}
df_viagens_teste = pd.DataFrame(dados_viagens_teste)

grafico_viagens(df_viagens_teste)