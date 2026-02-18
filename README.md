# XAIBASILEIA_v1

---

# 🏦 Sistema Basileia AI + XAI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Produção-green?style=for-the-badge)

**Sistema de Cálculo de Risco de Crédito com Machine Learning e Explainable AI**

</div>

---

## 📖 Sobre

O **Sistema Basileia AI** é uma aplicação desktop para cálculo de **Risk Weighted Assets (RWA)** baseado nos princípios do Acordo de Basileia. O sistema combina:

- ✅ **Regras Clássicas de Basileia** (PD, LGD, EAD)
- ✅ **Machine Learning** (Random Forest para predição de PD)
- ✅ **Explainable AI - XAI** (Explicação dos fatores de risco)
- ✅ **Processamento em Tempo Real** (Timelapse visual linha por linha)

Ideal para instituições financeiras, analistas de crédito e estudantes de finanças.

---

## ⚡ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🧮 **Cálculo Basileia** | PD, LGD, EAD e RWA automatizados |
| 🤖 **Machine Learning** | Modelo Random Forest para refinamento do PD |
| 🔍 **XAI** | Identificação do principal fator de risco por cliente |
| ⏱️ **Timelapse** | Visualização do processamento em tempo real |
| 📊 **Exportação** | Geração automática de Excel com resultados |
| 🎨 **Interface Dark** | Tema cinza/verde estilo terminal financeiro |
| 💻 **100% Local** | Sem dependência de nuvem ou internet |

---

## Requisitos

### Sistema Operacional
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

### Python
- Versão 3.8 ou superior

### Bibliotecas

```bash
pandas>=1.5.0
openpyxl>=3.0.0
scikit-learn>=1.0.0
numpy>=1.20.0
```

---

## Instalação

### 1. Clone ou Baixe o Projeto

```bash
git clone https://github.com/seu-usuario/basileia-ai.git
cd basileia-ai
```

### 2. Crie um Ambiente Virtual (Opcional mas Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação

```bash
python basileia_app.py
```

---

## 📖 Como Usar

### Passo a Passo

1. **Inicie a Aplicação**
   ```bash
   python basileia_app.py
   ```

2. **Selecione o Arquivo Excel**
   - Clique em `📂 Selecionar Excel`
   - Escolha sua planilha de clientes

3. **Ajuste a Velocidade (Opcional)**
   - Use o slider para controlar o timelapse (10ms a 500ms)

4. **Inicie o Processamento**
   - Clique em `▶ INICIAR PROCESSAMENTO`
   - Acompanhe o log em tempo real

5. **Resultado**
   - O arquivo será salvo automaticamente na pasta do projeto
   - Nome: `resultado_basileia_YYYYMMDD_HHMMSS.xlsx`

### Fluxo Visual

<img width="867" height="699" alt="image" src="https://github.com/user-attachments/assets/59b4b954-887e-47f1-9440-f46704edab41" />

---

## 📁 Estrutura do Projeto

```
basileia-ai/
├── basileia_app.py          # Aplicação principal (Desktop)
└── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
└── clientes_modelo.xlsx    # Arquivo de exemplo (opcional)
├── resultados/             # Pasta de saída (gerada automaticamente)
    └── resultado_basileia_YYYYMMDD_HHMMSS.xlsx
├── testes/
├── dados/
```

---

## 📄 Formato do Arquivo de Entrada

O arquivo Excel deve conter as seguintes colunas:

| Coluna | Tipo | Obrigatória | Descrição |
|--------|------|-------------|-----------|
| `Cliente` | Texto | ✅ | Nome ou ID do cliente |
| `Receita` | Numérico | ✅ | Receita anual (R$) |
| `Endividamento` | Numérico | ✅ | Dívida total (R$) |
| `EBITDA` | Numérico | ✅ | Lucro antes de juros, impostos, etc. |
| `Rating` | Texto | ❌ | Classificação de crédito (AAA, BB, B, etc.) |
| `Garantias` | Decimal (0-1) | ✅ | Percentual de garantia (ex: 0.8 = 80%) |

### Exemplo de Planilha

| Cliente   | Receita | Endividamento | EBITDA | Rating | Garantias |
|-----------|---------|---------------|--------|--------|-----------|
| Empresa A | 1000000 | 200000        | 300000 | AAA    | 0.8       |
| Empresa B | 500000  | 400000        | 50000  | B      | 0.2       |
| Empresa C | 2000000 | 500000        | 800000 | AA     | 0.9       |
| Empresa D | 150000  | 100000        | 10000  | C      | 0.1       |   

---

## 🧮 Fórmulas Utilizadas

### Probability of Default (PD)
```
PD_Final = (PD_ML × 0.7) + (PD_Rating × 0.3)
```

| Rating | PD Base |
|--------|---------|
| AAA    | 0.01 (1%) |
| BBB    | 0.05 (5%) |
| BB | 0.10 (10%) |
| B | 0.20 (20%) |
| C | 0.30 (30%) |

### Loss Given Default (LGD)
```
LGD = max(0, 1 - Garantias)
```

### Exposure at Default (EAD)
```
EAD = Endividamento
```

### Risk Weighted Assets (RWA)
```
RWA = PD × LGD × EAD × 12.5
```
*12.5 = inverso de 8% (capital mínimo exigido)*

---

## 📊 Exemplo de Saída

O arquivo de resultado conterá:

| Cliente   | Rating | PD_Final | LGD  | RWA      | Fator_Risco   |
|-----------|--------|----------|------|----------|---------------|
| Empresa A | AAA    | 0.0150   | 0.20 | 750.00   | EBITDA        |
| Empresa B | B      | 0.1850   | 0.80 | 59200.00 | Endividamento |
| Empresa C | AA     | 0.0120   | 0.10 | 600.00   | Receita       |
| Empresa D | C      | 0.2800   | 0.90 | 25200.00 | Endividamento |

---

## 🧠 Machine Learning & XAI

### Modelo Utilizado
- **Algoritmo:** Random Forest Regressor
- **Features:** Endividamento, EBITDA, Receita
- **Target:** Probability of Default (PD)
- **Treinamento:** Híbrido (dados sintéticos + dados do usuário)

### Explainable AI (XAI)
O sistema identifica automaticamente o **Fator de Risco Principal** para cada cliente:

- **Endividamento:** Quando dívida > 4× EBITDA
- **EBITDA:** Quando EBITDA < 10% da Receita
- **Receita:** Quando outros fatores estão dentro do esperado

---

## ⚠️ Avisos Importantes

1. **Uso Profissional:** Este sistema é uma **simplificação** do Acordo de Basileia. Para uso regulatório real, consulte as normas completas do BACEN.

2. **Dados Sensíveis:** Todo processamento é **local**. Nenhum dado é enviado para servidores externos.

3. **Backup:** Mantenha sempre cópia dos arquivos originais antes do processamento.

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Execute `pip install -r requirements.txt` |
| Arquivo não carrega | Verifique se as colunas estão nomeadas corretamente |
| Aplicação trava | Reduza a velocidade do timelapse no slider |
| Erro no Excel | Certifique-se de que o arquivo não está aberto em outro programa |

---

## 📝 Licença

Este projeto está sob a licença **MIT**.´.

```
MIT License

Copyright (c) 2024 Basileia AI System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

`Python` `Basileia` `Machine Learning` `XAI` `Finanças`

</div>
