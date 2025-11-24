import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def print_table(data):
    """
    Exibe os dados em formato de tabela organizada com Rich
    """
    if not data:
        console.print("\n❌ [red]Nenhum dado encontrado.[/red]\n")
        return None

    df = pd.DataFrame(data)
    
    # Limpar datas para exibição mais simples
    for col in df.columns:
        if 'data' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], utc=True).dt.strftime('%Y-%m-%d')
            except:
                pass
    
    # Criar tabela Rich
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    
    # Adicionar colunas
    for col in df.columns:
        table.add_column(str(col), style="cyan")
    
    # Adicionar linhas
    for _, row in df.iterrows():
        table.add_row(*[str(val) for val in row])
    
    console.print("\n")
    console.print(table)
    console.print(f"\n[bold green]📊 Total de registros: {len(df)}[/bold green]\n")
    
    return df


def print_detailed(data, title="DETALHES"):
    """
    Exibe dados detalhados item por item com Rich
    """
    if not data:
        console.print("\n❌ [red]Nenhum dado encontrado.[/red]\n")
        return None
    
    # Se for uma lista, exibir cada item
    if isinstance(data, list):
        console.print(f"\n[bold cyan]📋 {title.upper()}[/bold cyan]")
        
        for idx, item in enumerate(data, 1):
            print_item_rich(item, idx)
        
        console.print(f"\n[bold green]📊 Total de registros: {len(data)}[/bold green]\n")
        return data
    
    # Se for um único item
    else:
        console.print(f"\n[bold cyan]📋 {title.upper()}[/bold cyan]")
        print_item_rich(data, 1)
        return data


def print_item_rich(item, index):
    """
    Exibe um item em painel Rich
    """
    if not isinstance(item, dict):
        console.print(Panel(str(item), title=f"Registro #{index}", border_style="blue"))
        return
    
    content = ""
    for key, value in item.items():
        # Pular campos muito complexos
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            content += f"[yellow]📦 {key}:[/yellow] [{len(value)} itens]\n"
            continue
        
        # Se for dicionário, formatar
        if isinstance(value, dict):
            content += f"[yellow]📦 {key}:[/yellow]\n"
            for k, v in value.items():
                content += f"   [dim]▪️  {k}:[/dim] {v}\n"
        else:
            # Formatar datas
            if 'data' in key.lower() and isinstance(value, str) and 'T' in value:
                try:
                    value = pd.to_datetime(value).strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            content += f"[yellow]▪️  {key}:[/yellow] [white]{value}[/white]\n"
    
    console.print(Panel(content.strip(), title=f"🔹 Registro #{index}", border_style="cyan"))


def save_table_to_csv(data, filename):
    """
    Salva dados em arquivo CSV
    """
    if not data:
        console.print("\n❌ [red]Nenhum dado para salvar.[/red]\n")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    console.print(f"\n✅ [green]Dados salvos em '{filename}'[/green]\n")