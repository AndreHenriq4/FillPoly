import tkinter as tk
from tkinter import *
from tkinter import colorchooser  # Para o seletor de cores

root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.polygon_mode = False  # Controla se estamos no modo de criação de polígono
        self.vertices = []  # Armazena os vértices do polígono
        self.polygons = []  # Lista para armazenar os polígonos criados
        self.selected_polygon_name = None  # Nome do polígono selecionado
        self.fill_color = "yellow"  # Cor padrão do preenchimento
        self.edge_color = "yellow"  # Cor das arestas
        self.tela()
        self.frame()
        self.cria_botoes()
        self.canvas_area()  # Área de desenho para os polígonos
        root.mainloop()

    def tela(self):
        self.root.title("Fill Poly")
        self.root.configure(background='white')
        self.root.geometry('800x600')
        self.root.resizable(True, True)

    def frame(self):
        self.frame_1 = Frame(self.root, bg='grey')
        self.frame_1.place(relx=0.8, rely=0, relwidth=1, relheight=1)

    def cria_botoes(self):
        self.bt_novoPoligono = Button(self.frame_1, text='Novo Polígono', command=self.start_polygon_mode)
        self.bt_novoPoligono.place(relx=0.01, rely=0.01, relwidth=0.181, relheight=0.1)

        self.bt_limpar = Button(self.frame_1, text='Limpar', command=self.clear_canvas)
        self.bt_limpar.place(relx=0.01, rely=0.12, relwidth=0.181, relheight=0.1)

        self.bt_cor = Button(self.frame_1, text='Trocar Cor', command=self.trocar_cor)
        self.bt_cor.place(relx=0.01, rely=0.23, relwidth=0.181, relheight=0.1)

        self.bt_sair = Button(self.frame_1, text='Sair', command=self.root.quit)
        self.bt_sair.place(relx=0.01, rely=0.34, relwidth=0.181, relheight=0.1)

        self.bt_deletar = Button(self.frame_1, text='Deletar Polígono', command=self.deletar_poligono)
        self.bt_deletar.place(relx=0.01, rely=0.45, relwidth=0.181, relheight=0.1)

        self.edge_color_var = BooleanVar()
        self.cb_cor_aresta = Checkbutton(self.frame_1, text='Cor da Aresta', variable=self.edge_color_var, command=self.choose_edge_color)
        self.cb_cor_aresta.place(relx=0.01, rely=0.56, relwidth=0.181, relheight=0.1)

        self.lb_nome = Label(self.frame_1, text='Nome', bg='grey')
        self.lb_nome.place(relx=0.01, rely=0.92, relwidth=0.181, relheight=0.04)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.01, rely=0.95, relwidth=0.181, relheight=0.04)

        self.poligonos_lista = Listbox(self.frame_1)
        self.poligonos_lista.place(relx=0.01, rely=0.7, relwidth=0.181, relheight=0.2)
        self.poligonos_lista.bind("<Double-1>", self.seleciona_poligono)

    def canvas_area(self):
        # Criando a área de desenho
        self.canvas = Canvas(self.root, bg="white")
        self.canvas.place(relx=0, rely=0, relwidth=0.8, relheight=1)

        # Captura o clique do mouse na área de desenho
        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<Button-3>", self.complete_polygon)

    def carregar_lista_poligonos(self):
        """Carrega a lista de polígonos e exibe na Listbox"""
        self.poligonos_lista.delete(0, END)
        for poligono in self.polygons:
            self.poligonos_lista.insert(END, poligono['nome'])

    def start_polygon_mode(self):
        """Ativa o modo de criação de polígono após inserir o nome"""
        nome_poligono = self.nome_entry.get()
        if nome_poligono == "":
            print("Por favor, insira um nome para o polígono antes de criar.")
            return

        self.selected_polygon_name = nome_poligono  # Armazena o nome do polígono
        self.polygon_mode = True
        self.vertices = []  # Reinicia a lista de vértices
        print(f"Modo de criação de polígono ativado para '{nome_poligono}' com cor '{self.fill_color}'. Clique na tela para adicionar vértices.")

    def add_vertex(self, event):
        """Adiciona vértices ao clicar com o botão esquerdo do mouse"""
        if self.polygon_mode:
            x, y = event.x, event.y
            self.vertices.append((x, y))
            if len(self.vertices) > 1:
                self.canvas.create_line(self.vertices[-2], self.vertices[-1], fill=self.edge_color, width=2)
            print(f"Vértice adicionado: {x}, {y}")

    def complete_polygon(self, event):
        """Completa o polígono ao clicar com o botão direito"""
        if len(self.vertices) > 2:
            # Desenha o polígono completo, conectando o último vértice ao primeiro
            self.canvas.create_polygon(self.vertices, outline=self.edge_color, fill=self.fill_color, width=2)
            self.scanline_fill(self.vertices, self.fill_color)

            # Salva o polígono na lista de polígonos
            self.polygons.append({
                'nome': self.selected_polygon_name,
                'vertices': self.vertices[:],
                'cor': self.fill_color,
                'edge_color': self.edge_color
            })
            self.carregar_lista_poligonos()  # Atualiza a lista de polígonos

            self.polygon_mode = False  # Sai do modo de criação
            self.vertices = []  # Limpa os vértices para o próximo polígono
            print(f"Polígono '{self.selected_polygon_name}' finalizado e salvo.")
        else:
            print("Um polígono precisa de ao menos 3 vértices.")

    def seleciona_poligono(self, event):
        """Carrega o polígono selecionado da lista e exibe na tela"""
        selection = self.poligonos_lista.get(self.poligonos_lista.curselection())
        # Encontra o polígono na lista pela chave nome
        for poligono in self.polygons:
            if poligono['nome'] == selection:
                vertices = poligono['vertices']
                fill_color = poligono['cor']
                edge_color = poligono['edge_color']

                # Exibe o polígono na tela
                self.canvas.create_polygon(vertices, outline=edge_color, fill=fill_color, width=2)
                self.scanline_fill(vertices, fill_color)

                self.selected_polygon_name = selection
                print(f"Polígono '{selection}' carregado e desenhado.")
                break

    def trocar_cor(self):
        """Troca a cor de preenchimento do polígono selecionado ou o próximo a ser criado"""
        # Escolhe uma nova cor
        nova_cor = colorchooser.askcolor()[1]
        if nova_cor:
            # Atualiza a cor de preenchimento global para novos polígonos
            self.fill_color = nova_cor
            
            if self.selected_polygon_name:
                # Se um polígono estiver selecionado, altere sua cor
                for poligono in self.polygons:
                    if poligono['nome'] == self.selected_polygon_name:
                        poligono['cor'] = nova_cor
                        vertices = poligono['vertices']
                        edge_color = poligono['edge_color']

                        # Redesenha com a nova cor
                        self.canvas.create_polygon(vertices, outline=edge_color, fill=nova_cor, width=2)
                        self.scanline_fill(vertices, nova_cor)
                        print(f"Cor do polígono '{self.selected_polygon_name}' atualizada.")
                        break
            else:
                print(f"Cor para novos polígonos alterada para {nova_cor}.")

    def deletar_poligono(self):
        """Deleta o polígono selecionado da lista e redesenha o restante"""
        if not self.selected_polygon_name:
            print("Selecione um polígono primeiro para deletar.")
            return

        # Remove o polígono da lista
        self.polygons = [p for p in self.polygons if p['nome'] != self.selected_polygon_name]
        
        # Atualiza a lista de polígonos na interface
        self.carregar_lista_poligonos()

        # Limpa o canvas, mas redesenha todos os polígonos restantes
        self.redesenhar_poligonos()

        # Limpa a seleção atual
        self.selected_polygon_name = None
        print(f"Polígono '{self.selected_polygon_name}' deletado.")

    def redesenhar_poligonos(self):
        """Redesenha todos os polígonos no canvas após uma modificação"""
        self.canvas.delete("all")  # Limpa o canvas

        # Desenha novamente cada polígono que ainda está na lista
        for poligono in self.polygons:
            vertices = poligono['vertices']
            fill_color = poligono['cor']
            edge_color = poligono['edge_color']

            # Desenha o polígono com suas propriedades
            self.canvas.create_polygon(vertices, outline=edge_color, fill=fill_color, width=2)
            self.scanline_fill(vertices, fill_color)

    def scanline_fill(self, vertices, color):
        if len(vertices) < 3:
            return
        
        min_y = min(y for _, y in vertices)
        max_y = max(y for _, y in vertices)

        edge_table = []
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % len(vertices)]

            if v1[1] > v2[1]:
                v1, v2 = v2, v1
            inv_slope = (v2[0] - v1[0]) / (v2[1] - v1[1])
            edge_table.append({
                'x': v1[0],
                'y_min': v1[1],
                'y_max': v2[1],
                'inv_slope': inv_slope
            })
    
        for y in range(min_y, max_y + 1):
            active_edges = []
            for edge in edge_table:
                if edge['y_min'] <= y < edge['y_max']:
                    x_intersect = edge['x'] + (y - edge['y_min']) * edge['inv_slope']
                    active_edges.append(x_intersect)

            active_edges.sort()
            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):
                    self.canvas.create_line(active_edges[i], y, active_edges[i + 1], y, fill=color)

    def choose_edge_color(self):
        if self.edge_color_var.get() == 1:
            self.edge_color = colorchooser.askcolor()[1]
            print(f"Cor da aresta selecionada: {self.edge_color}")
        else:
            self.edge_color = "yellow"
            print(f"Cor da aresta igual à cor de preenchimento: {self.edge_color}")

    def clear_canvas(self):
        """Limpa o canvas e reseta o modo"""
        self.canvas.delete("all")
        self.vertices = []
        self.polygon_mode = False
        self.selected_polygon_name = None
        print("Canvas limpo.")

    def sair(self):
        self.root.quit()

# Executa a aplicação
if __name__ == "__main__":
    app = Application()