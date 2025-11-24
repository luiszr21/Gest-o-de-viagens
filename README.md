# 🌍 Sistema de Gestão de Viagens

Projeto desenvolvido para a disciplina **Algoritmos e Estruturas de Dados I** do curso **Análise e Desenvolvimento de Sistemas**, utilizando **Python** para manipulação de dados de uma API.

O sistema permite gerenciar **viagens** e **reservas** diretamente pelo terminal, incluindo **CRUD**, pesquisas e gráficos coloridos.

---

## 📋 Descrição

O sistema consome dados de uma **API** (JSON Server ou própria API) e possibilita:

- Gerenciar viagens (criar, listar, atualizar e deletar).
- Gerenciar reservas vinculadas às viagens.
- Gerar gráficos resumidos diretamente no terminal, incluindo quantidade de viagens por destino e preço médio.

Todos os gráficos são exibidos com **barras coloridas** e tabelas organizadas usando a biblioteca **Rich**.

---

## ⚙️ Funcionalidades

### ✈️ Viagens

- Listar todas as viagens
- Criar nova viagem
- Atualizar viagem existente
- Deletar viagem

### 🛎 Reservas

- Listar todas as reservas
- Criar nova reserva
- Atualizar reserva existente
- Deletar reserva

### 📊 Gráficos

- Quantidade de viagens por destino
- Preço médio por destino
- Reservas por status

---

## 🛠 Tecnologias

- **Python 3.x**
- Bibliotecas:
  - `pandas` – manipulação de dados
  - `rich` – tabelas, cores e gráficos no terminal
  - `requests` – comunicação com API

---
## 📂 Estrutura do Projeto
SISTEMAVIAGEM/
│
├─ CRUDs/
│ ├─ viagens.py
│ ├─ reservas.py
│ └─ pesquisa.py
│
├─ utils/
│ ├─ graficos.py
│ ├─ requester.py
│ └─ tables.py
│
├─ main.py
└─ README.md


