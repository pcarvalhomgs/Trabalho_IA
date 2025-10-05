# gui_8puzzle.py
import threading
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

from IA_Blargura import busca_largura
from IA_Bprofundidade import busca_profundidade
from IA_Bgulosa import busca_gulosa
from IA_Aestrela import a_estrela

# --- Parâmetros ---
ANIM_MS = 500  # 1 segundo entre passos na animação (conforme pedido)
objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Reutilizamos algumas funções do seu módulo original:
# Você pode copiar/colar eh_solucionavel/conta_inversoes aqui ou importar se estiver em outro módulo.
def conta_inversoes(estado):
    lista = [num for linha in estado for num in linha if num != 0]
    inversoes = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversoes += 1
    return inversoes

def eh_solucionavel(estado):
    inversoes = conta_inversoes(estado)
    return inversoes % 2 == 0


# --- GUI Principal (Tela 01) ---
class MainGUI:
    def __init__(self, root):
        self.root = root
        root.title("Acaba pelamor")
        root.geometry("1100x850")

        # frame superior: entradas
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")

        entradas_frame = ttk.LabelFrame(top, text="Estado inicial (digite 3 números por linha, use 0 para o vazio)")
        entradas_frame.pack(side="left", padx=8, pady=4)

        # 🔹 Criação do tabuleiro 3x3 interativo
        self.tabuleiro_entries = []
        for i in range(3):
            for j in range(3):
                e = ttk.Entry(entradas_frame, width=5, font=("Arial", 16), justify="center")
                e.grid(row=i, column=j, padx=4, pady=4)
                self.tabuleiro_entries.append(e)

        # # label informativa
        # ttk.Label(
        #     top, text="Digite os números de 0 a 8 (sem repetir, 0 representa o espaço vazio)."
        # ).pack(side="left", padx=12, pady=4)

        # self.entry_lines = []
        # for i in range(3):
        #     e = ttk.Entry(entradas_frame, width=20)
        #     e.grid(row=i, column=0, padx=6, pady=4)
        #     self.entry_lines.append(e)

        # algoritmo e botões
        control_frame = ttk.Frame(top)
        control_frame.pack(side="top", padx=16)

        ttk.Label(control_frame, text="Algoritmo:").grid(row=0, column=0, sticky="w")
        self.alg_combo = ttk.Combobox(control_frame, values=["Busca em Largura", "Busca em Profundidade", "Busca Gulosa", "Busca A*"], state="readonly", width=20)
        self.alg_combo.grid(row=0, column=1, padx=6, pady=2)
        self.alg_combo.current(0)

        self.btn_exec = ttk.Button(control_frame, text="Executar", command=self.on_execute)
        self.btn_exec.grid(row=1, column=0, columnspan=2, pady=6, sticky="ew")

        self.btn_open_anim = ttk.Button(control_frame, text="Abrir Animação", command=self.open_anim_window, state="disabled")
        self.btn_open_anim.grid(row=2, column=0, columnspan=2, pady=6, sticky="ew")

        # status
        self.status_label = ttk.Label(control_frame, text="Pronto")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(6,0))

        # frame central: duas colunas de texto
        center = ttk.Frame(root, padding=6)
        center.pack(fill="both", expand=True)

        # coluna A: Estados por nível
        colA = ttk.LabelFrame(center, text="A: Estados por nível da árvore")
        colA.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self.txt_niveis = scrolledtext.ScrolledText(colA, wrap=tk.WORD, width=50, height=28)
        self.txt_niveis.pack(fill="both", expand=True, padx=4, pady=4)

        # coluna B: Ordem de Exploração
        colB = ttk.LabelFrame(center, text="B: Ordem de Exploração")
        colB.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self.txt_ordem = scrolledtext.ScrolledText(colB, wrap=tk.WORD, width=50, height=28)
        self.txt_ordem.pack(fill="both", expand=True, padx=4, pady=4)

        # Caixa de resumo abaixo
        resumo_frame = ttk.LabelFrame(root, text="Detalhes: ")
        resumo_frame.pack(fill="x", padx=6, pady=6)
        self.txt_resumo = scrolledtext.ScrolledText(resumo_frame, wrap=tk.WORD, height=6)
        self.txt_resumo.pack(fill="x", padx=4, pady=4)

        # fila para comunicação da thread de execução
        self.result_queue = queue.Queue()

        # guarda último resultado (para Tela 02)
        self.last_result = None  # (nome, niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados)


    # lê o estado inicial do tabuleiro 
    def read_state_from_entries(self):
        try:
            valores = [int(e.get()) for e in self.tabuleiro_entries]
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números de 0 a 8.")
            return None

        # valida se contém exatamente os números de 0 a 8
        if sorted(valores) != list(range(9)):
            messagebox.showerror("Erro", "O tabuleiro deve conter todos os números de 0 a 8, sem repetições.")
            return None

        estado = [valores[i:i+3] for i in range(0, 9, 3)]
        return estado


    # lê estado das entradas
    # def read_state_from_entries(self):
    #     try:
    #         estado = []
    #         for e in self.entry_lines:
    #             parts = e.get().strip().split()
    #             if len(parts) != 3:
    #                 raise ValueError("Cada linha deve conter 3 números.")
    #             linha = [int(x) for x in parts]
    #             estado.append(linha)
    #         return estado
    #     except Exception as ex:
    #         messagebox.showerror("Entrada inválida", f"Formato inválido: {ex}")
    #         return None

    # botão executar
    def on_execute(self):
        estado = self.read_state_from_entries()
        if estado is None:
            return
        if not eh_solucionavel(estado):
            messagebox.showerror("Insolucionável", "O estado inserido não é solucionável.")
            return

        alg = self.alg_combo.get()
        # desativa botões enquanto executa
        self.btn_exec['state'] = 'disabled'
        self.btn_open_anim['state'] = 'disabled'
        self.status_label['text'] = f"Executando {alg}..."

        # start thread
        th = threading.Thread(target=self.run_search_thread, args=(alg, estado), daemon=True)
        th.start()
        self.root.after(100, self.check_result_queue)

    # thread runner
    def run_search_thread(self, alg, estado):
        try:
            if alg == "Busca em Largura":
                res = busca_largura(estado, objetivo)
                nome = "Busca em Largura"
            elif alg == "Busca em Profundidade":
                res = busca_profundidade(estado, objetivo)
                nome = "Busca em Profundidade"
            elif alg == "Busca Gulosa":
                res = busca_gulosa(estado, objetivo)
                nome = "Busca Gulosa"
            else:
                res = a_estrela(estado, objetivo)
                nome = "A*"

            # res deve ser (niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados)
            if res is None:
                self.result_queue.put(("error", f"Algoritmo retornou None ({nome})"))
            else:
                niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados = res
                self.result_queue.put(("ok", (nome, niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados)))
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.result_queue.put(("error", f"Erro ao executar busca: {e}\n{tb}"))

    # checa fila para resultado
    def check_result_queue(self):
        try:
            tag, payload = self.result_queue.get_nowait()
        except queue.Empty:
            self.root.after(100, self.check_result_queue)
            return

        if tag == "error":
            messagebox.showerror("Erro", str(payload))
            self.status_label['text'] = "Erro"
            self.btn_exec['state'] = 'normal'
            return

        # desempacota e atualiza UI
        nome, niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados = payload

        # Preenche txt_niveis com exatamente o mesmo formato textual usado no console
        niveis_text = self.build_niveis_text(niveis)
        self.txt_niveis.delete(1.0, tk.END)
        self.txt_niveis.insert(tk.END, niveis_text)

        # Ordem de exploração (formata dependendo da tupla)
        ordem_text = self.build_ordem_text(ordem)
        self.txt_ordem.delete(1.0, tk.END)
        self.txt_ordem.insert(tk.END, ordem_text)

        # Resumo
        resumo_text = self.build_resumo_text(analisados, fila, profundidade, caminho, caminho_estados)
        self.txt_resumo.delete(1.0, tk.END)
        self.txt_resumo.insert(tk.END, resumo_text)

        # também imprime no console
        print(f"\n=== {nome} ===")
        print(niveis_text)
        print(ordem_text)
        print(resumo_text)

        # habilita botão abrir animação e reabilita executar
        self.last_result = (nome, niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados)
        self.btn_open_anim['state'] = 'normal'
        self.btn_exec['state'] = 'normal'
        self.status_label['text'] = f"Pronto ({nome})"

    # monta string igual ao print em exibir_resultados
    def build_niveis_text(self, niveis):
        lines = []
        # percorre niveis em ordem de nível
        for nivel in sorted(niveis.keys()):
            estados = niveis[nivel]
            lines.append(f"Nível {nivel}: {len(estados)} estados")
            for e in estados:
                # estado pode ser estado (lista) ou (estado, heur)
                if isinstance(e, tuple) and len(e) == 2 and isinstance(e[1], (int, float)):
                    estado, val = e
                    lines.append(f"(f ou h)={val}")
                    lines.append(str(np.array(estado)))
                    lines.append("")  
                else:
                    lines.append(str(np.array(e)))
                    lines.append("")
        return "\n".join(lines)

    def build_ordem_text(self, ordem):
        lines = []
        # cada elemento pode ser (estado, prof) ou (estado, prof, heur)
        for i, item in enumerate(ordem):
            if len(item) == 2:
                estado, prof = item
                lines.append(f"Passo {i} (nível {prof}):")
                lines.append(str(np.array(estado)))
                lines.append("")
            elif len(item) == 3:
                estado, prof, heur = item
                lines.append(f"Passo {i} | nível={prof} | (f ou h)={heur}:")
                lines.append(str(np.array(estado)))
                lines.append("")
            else:
                # fallback
                lines.append(str(item))
                lines.append("")
        return "\n".join(lines)

    def build_resumo_text(self, analisados, fila, profundidade, caminho, caminho_estados):
        lines = []
        lines.append(f"Estados analisados: {analisados}")
        lines.append(f"Estados na fronteira: {len(fila)}")
        lines.append(f"Profundidade da solução: {profundidade}")
        lines.append("")
        lines.append("Caminho da solução: " + (" -> ".join(caminho) if caminho else ""))
        lines.append("")
        return "\n".join(lines)

    # Abre a janela de animação. Requer last_result preenchido.
    def open_anim_window(self):
        if not self.last_result:
            messagebox.showwarning("Aviso", "Execute um algoritmo primeiro para gerar resultado.")
            return
        nome, niveis, ordem, analisados, fila, profundidade, caminho, caminho_estados = self.last_result
        AnimWindow(self.root, caminho_estados, nome, caminho)  # passa só o caminho de estados e nome/caminho


# --- Tela 02: Animação ---
class AnimWindow:
    def __init__(self, parent, caminho_estados, nome_alg, caminho_movimentos):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Animação — {nome_alg}")
        self.top.geometry("800x420")
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

        # painel esquerdo: tabuleiro
        left = ttk.Frame(self.top, padding=8)
        left.pack(side="left", fill="both", expand=False)

        self.tiles = [[None]*3 for _ in range(3)]
        board_frame = ttk.Frame(left)
        board_frame.pack(padx=6, pady=6)
        for i in range(3):
            for j in range(3):
                lbl = tk.Label(board_frame, text="", width=6, height=3, relief="raised", font=("Helvetica", 16))
                lbl.grid(row=i, column=j, padx=4, pady=4)
                self.tiles[i][j] = lbl

        # topo: mostra movimentos (caminho)
        # ttk.Label(left, text="Movimentos (caminho):").pack()
        # self.lbl_moves = tk.Label(left, text=" -> ".join(caminho_movimentos), wraplength=220, justify="left")
        # self.lbl_moves.pack(pady=(2,8))

        # botões de controle
        ctrl = ttk.Frame(left)
        ctrl.pack(pady=4)
        self.btn_play = ttk.Button(ctrl, text="▶ Iniciar/Continuar", command=self.play)
        self.btn_play.grid(row=2, column=0, padx=4)
        self.btn_pause = ttk.Button(ctrl, text="⏸ Pausar", command=self.pause, state="disabled")
        self.btn_pause.grid(row=2, column=1, padx=4)
        self.btn_restart = ttk.Button(ctrl, text="↺ Reiniciar", command=self.restart, state="normal")
        self.btn_restart.grid(row=2, column=2, padx=4)
        self.btn_close = ttk.Button(ctrl, text="Fechar", command=self.on_close)
        self.btn_close.grid(row=2, column=3, padx=4)

        # painel direito: caminho de estados (texto)
        right = ttk.Frame(self.top)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(right, text="Caminho de estados até a solução:").pack(anchor="w")
        self.txt_path = scrolledtext.ScrolledText(right, wrap=tk.WORD, width=50, height=20)
        self.txt_path.pack(fill="both", expand=True, pady=4)

        # prepara os passos da animação - extrai só os estados
        self.steps = [est for (est, prof) in caminho_estados]
        self.path_text_lines = []
        for i, (est, prof) in enumerate(caminho_estados):
            self.path_text_lines.append(f"Passo {i} (nível {prof}):")
            self.path_text_lines.append(str(np.array(est)))
            self.path_text_lines.append("")

        # preenche texto (igual ao console)
        self.txt_path.delete(1.0, tk.END)
        self.txt_path.insert(tk.END, "\n".join(self.path_text_lines))

        # animação estado inicial
        if self.steps:
            self.current_idx = 0
            self.draw_state(self.steps[0])
        else:
            self.current_idx = 0

        # controle de after
        self.after_id = None
        self.is_playing = False

    def draw_state(self, estado):
        for i in range(3):
            for j in range(3):
                val = estado[i][j]
                lbl = self.tiles[i][j]
                if val == 0:
                    lbl['text'] = ""
                    lbl['bg'] = "#d9d9d9"
                else:
                    lbl['text'] = str(val)
                    lbl['bg'] = "#f0f0ff"

    def play(self):
        if not self.steps:
            messagebox.showinfo("Info", "Não há passos para animar.")
            return
        if self.is_playing:
            return
        self.is_playing = True
        self.btn_play['state'] = 'disabled'
        self.btn_pause['state'] = 'normal'
        self.schedule_next()

    def schedule_next(self):
        if self.current_idx < len(self.steps)-1:
            # avança para próximo estado
            self.current_idx += 1
            self.draw_state(self.steps[self.current_idx])
            # também rola o scrolledtext para mostrar o passo atual
            # calcula a posição do texto correspondente (aprox) — vamos buscar a ocorrência do "Passo {current_idx}"
            query = f"Passo {self.current_idx} (nível"
            txt = self.txt_path
            pos = txt.search(query, "1.0", tk.END)
            if pos:
                txt.see(pos)
            # agenda o próximo
            self.after_id = self.top.after(ANIM_MS, self.schedule_next)
        else:
            # terminou Animação
            self.is_playing = False
            self.btn_play['state'] = 'normal'
            self.btn_pause['state'] = 'disabled'
            self.after_id = None

    def pause(self):
        if self.after_id:
            self.top.after_cancel(self.after_id)
            self.after_id = None
        self.is_playing = False
        self.btn_play['state'] = 'normal'
        self.btn_pause['state'] = 'disabled'

    def restart(self):
        if self.after_id:
            self.top.after_cancel(self.after_id)
            self.after_id = None
        self.is_playing = False
        self.current_idx = 0
        if self.steps:
            self.draw_state(self.steps[0])
            # rola para o início do texto
            self.txt_path.see("1.0")
        self.btn_play['state'] = 'normal'
        self.btn_pause['state'] = 'disabled'

    def on_close(self):
        # cancela after se existir
        if self.after_id:
            self.top.after_cancel(self.after_id)
            self.after_id = None
        self.top.destroy()


def main():
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
