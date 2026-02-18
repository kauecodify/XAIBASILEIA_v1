# gerar_modelo.py
import pandas as pd

dados = {
    'Cliente': [
        'Empresa Alpha LTDA',
        'Empresa Beta SA',
        'Empresa Gamma ME',
        'Empresa Delta LTDA',
        'Empresa Epsilon SA',
        'Empresa Zeta ME',
        'Empresa Eta LTDA',
        'Empresa Theta SA',
        'Empresa Iota ME',
        'Empresa Kappa LTDA'
    ],
    'Receita': [
        1000000, 500000, 2000000, 150000, 800000,
        1500000, 300000, 2500000, 400000, 1200000
    ],
    'Endividamento': [
        200000, 400000, 500000, 100000, 600000,
        300000, 250000, 800000, 350000, 450000
    ],
    'EBITDA': [
        300000, 50000, 800000, 10000, 200000,
        500000, 80000, 900000, 100000, 400000
    ],
    'Rating': [
        'AAA', 'B', 'AA', 'C', 'BB',
        'A', 'BBB', 'AAA', 'BB', 'A'
    ],
    'Garantias': [
        0.8, 0.2, 0.9, 0.1, 0.5,
        0.7, 0.6, 0.85, 0.4, 0.65
    ]
}

df = pd.DataFrame(dados)
df.to_excel('clientes_modelo.xlsx', index=False)
print('✅ Arquivo clientes_modelo.xlsx gerado com sucesso!')
