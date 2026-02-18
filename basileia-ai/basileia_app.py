# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 19:47:02 2026
by k :D
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import threading
import time
import os
from datetime import datetime

# ==========================================
# 🧠 LÓGICA DE NEGÓCIO E ML
# ==========================================

class BasileiaEngine:
    def __init__(self):
        self.model = None

    def treinar_modelo(self, df):
        """Treina modelo ML internamente"""
        # Dados sintéticos para calibração inicial
        np.random.seed(42)
        n = 500
        dados_sinteticos = pd.DataFrame({
            'Endividamento': np.random.uniform(0, 1000000, n),
            'EBITDA': np.random.uniform(50000, 500000, n),
            'Receita': np.random.uniform(100000, 2000000, n)
        })
        dados_sinteticos['PD_Sintetico'] = np.clip((dados_sinteticos['Endividamento'] / (dados_sinteticos['EBITDA'] + 1)) * 0.0001, 0.01, 0.5)
        
        # Se o DF tiver dados reais, usa (simplificado para este exemplo)
        X = dados_sinteticos[['Endividamento', 'EBITDA', 'Receita']]
        y = dados_sinteticos['PD_Sintetico']
        
        self.model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        self.model.fit(X, y)
        return True

    def processar_linha(self, row, velocidade_ms):
        """Processa uma única linha e retorna o resultado + delay"""
        time.sleep(velocidade_ms / 1000.0)  # Timelapse

        # 1. Dados
        rating = row.get('Rating', 'BB')
        endiv = row.get('Endividamento', 0)
        ebitda = row.get('EBITDA', 1)
        receita = row.get('Receita', 1)
        garantias = row.get('Garantias', 0)
        cliente = row.get('Cliente', 'Desconhecido')

        # 2. Cálculo Híbrido (Basileia + ML)
        mapa_pd = {'AAA':0.01, 'BBB':0.05, 'BB':0.1, 'B':0.2, 'C':0.3}
        pd_basico = mapa_pd.get(rating, 0.1)
        
        # Predição ML
        try:
            features = pd.DataFrame([[endiv, ebitda, receita]], columns=['Endividamento', 'EBITDA', 'Receita'])
            pd_ml = self.model.predict(features)[0]
        except:
            pd_ml = pd_basico

        pd_final = (pd_ml * 0.7) + (pd_basico * 0.3)
        
        # 3. Fórmulas Basileia
        lgd = max(0, 1 - garantias)
        ead = endiv
        rwa = pd_final * lgd * ead * 12.5

        # 4. XAI Simples (Qual feature mais impactou?)
        # Simplificação: se dívida alta, é o fator
        fator = "Endividamento" if endiv > (ebitda * 4) else "EBITDA" if ebitda < (receita * 0.1) else "Receita"

        return {
            'Cliente': cliente,
            'Rating': rating,
            'PD_Final': round(pd_final, 4),
            'LGD': round(lgd, 4),
            'RWA': round(rwa, 2),
            'Fator_Risco': fator
        }

# ==========================================
# 🖥️ INTERFACE GRÁFICA (TKINTER)
# ==========================================

class AppBasileia:
    def __init__(self, root):
        self.root = root
        self.root.title("DATAK - XAI|Basileia AI - Local")
        self.root.geometry("900x600")
        self.root.configure(bg="#121212")
        
        self.engine = BasileiaEngine()
        self.arquivo_path = None
        
        # Configuração de Estilo (Tema Dark/Green)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#121212")
        self.style.configure("TLabel", background="#121212", foreground="#00ff41", font=("Consolas", 10))
        self.style.configure("Title.TLabel", font=("Consolas", 16, "bold"), foreground="#00ff41")
        self.style.configure("TButton", background="#004400", foreground="#00ff41", font=("Consolas", 10, "bold"))
        self.style.map("TButton", background=[("active", "#006600")])
        self.style.configure("TProgressbar", background="#00ff41", troughcolor="#333333")
        
        self._criar_widgets()

    def _criar_widgets(self):
        # Header
        header = ttk.Frame(self.root)
        header.pack(pady=20)
        lbl_title = ttk.Label(header, text="🏦 XAI | BASILEIA AI SYSTEM v1.0", style="Title.TLabel")
        lbl_title.pack()
        lbl_sub = ttk.Label(header, text="Processamento Local com Machine Learning", foreground="#888888")
        lbl_sub.pack()

        # Área de Controle
        ctrl_frame = ttk.Frame(self.root)
        ctrl_frame.pack(pady=20, fill="x", padx=50)

        btn_select = ttk.Button(ctrl_frame, text="📂 Selecionar Excel", command=self.selecionar_arquivo)
        btn_select.pack(side="left", padx=10)

        self.lbl_arquivo = ttk.Label(ctrl_frame, text="Nenhum arquivo selecionado", foreground="#666666")
        self.lbl_arquivo.pack(side="left", padx=10)

        # Slider de Velocidade
        lbl_vel = ttk.Label(ctrl_frame, text="Velocidade:")
        lbl_vel.pack(side="right", padx=(20, 5))
        self.slider_vel = ttk.Scale(ctrl_frame, from_=10, to=500, orient="horizontal", length=150)
        self.slider_vel.set(100)
        self.slider_vel.pack(side="right")

        # Área de Log (Terminal Style)
        log_frame = ttk.Frame(self.root, relief="sunken", borderwidth=1)
        log_frame.pack(pady=10, fill="both", expand=True, padx=50)
        
        self.txt_log = tk.Text(log_frame, bg="#1e1e1e", fg="#00ff41", font=("Consolas", 9), insertbackground="#00ff41")
        self.txt_log.pack(fill="both", expand=True)
        
        # Barra de Progresso
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=800, mode="determinate")
        self.progress.pack(pady=20)

        # Botão Processar
        self.btn_processar = ttk.Button(self.root, text="▶ INICIAR PROCESSAMENTO", command=self.iniciar_thread)
        self.btn_processar.pack(pady=10)
        self.btn_processar.config(state="disabled")

    def log(self, mensagem):
        self.txt_log.insert(tk.END, f">> {mensagem}\n")
        self.txt_log.see(tk.END)

    def selecionar_arquivo(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filename:
            self.arquivo_path = filename
            self.lbl_arquivo.config(text=os.path.basename(filename), foreground="#00ff41")
            self.btn_processar.config(state="normal")
            self.log(f"Arquivo carregado: {os.path.basename(filename)}")

    def iniciar_thread(self):
        self.btn_processar.config(state="disabled")
        self.txt_log.delete(1.0, tk.END)
        self.log("Iniciando motor de IA...")
        
        # Roda em thread separada para não travar a UI
        thread = threading.Thread(target=self.processar_tudo)
        thread.start()

    def processar_tudo(self):
        try:
            # 1. Carregar
            self.log("Lendo dados do Excel...")
            df = pd.read_excel(self.arquivo_path)
            
            # Validação simples de colunas
            cols_minimas = ['Cliente', 'Endividamento', 'EBITDA', 'Garantias']
            for col in cols_minimas:
                if col not in df.columns:
                    raise ValueError(f"Coluna '{col}' não encontrada no Excel.")

            # 2. Treinar ML
            self.log("Calibrando modelo Random Forest...")
            self.engine.treinar_modelo(df)
            self.log("Modelo pronto.")

            # 3. Loop de Processamento (Timelapse)
            total = len(df)
            resultados = []
            velocidade = self.slider_vel.get()

            for i, row in df.iterrows():
                res = self.engine.processar_linha(row, velocidade)
                resultados.append(res)
                
                # Atualizar UI
                progresso = (i + 1) / total
                self.root.after(0, self.progress.config, value=progresso*100)
                self.root.after(0, self.log, f"[{i+1}/{total}] {res['Cliente']} | RWA: {res['RWA']:,.2f} | Risco: {res['Fator_Risco']}")

            # 4. Salvar Resultado
            df_res = pd.DataFrame(resultados)
            nome_saida = f"resultado_basileia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df_res.to_excel(nome_saida, index=False)
            
            self.root.after(0, self.log, f"✅ SUCESSO! Arquivo salvo como: {nome_saida}")
            self.root.after(0, messagebox.showinfo, "Concluído", f"Processamento finalizado!\nArquivo salvo: {nome_saida}")

        except Exception as e:
            self.root.after(0, self.log, f"❌ ERRO: {str(e)}")
            self.root.after(0, messagebox.showerror, "Erro", str(e))
        
        finally:
            self.root.after(0, self.btn_processar.config, state="normal")

# ==========================================
# 🚀 EXECUÇÃO
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AppBasileia(root)
    root.mainloop()
