from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll, Middle, ItemGrid, Grid, HorizontalGroup, Vertical, Horizontal, HorizontalScroll, Container
from textual.widgets import Button, Header, Label, ProgressBar
from threading import Thread
from time import sleep
from textual.color import Gradient

class FundingProgressApp(App[None]):
    """
    Aplicação baseada no Textual para simular uma competição de barras de progresso.
    Cada barra representa um competidor e seu progresso é atualizado dinamicamente.
    """
    TITLE = "Competição de Barra"
    CSS = """
    ItemGrid {
        grid-size: 4;  /* Define 3 colunas */
        position: relative;
    }
    Container {
        align: center middle
    }
    Button {
        margin: 2 0;
    }
    """

    def __init__(self, driver_class=None, css_path=None, watch_css=False, ansi_color=False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.items = 60  # Número de barras de progresso
        self.bars = ['Winner'] * self.items  # Lista de status de cada barra
        self.gradient = Gradient.from_colors(  # Gradiente de cores para a barra de progresso
            "#881177", "#aa3355", "#cc6666", "#ee9944", "#eedd00", "#99dd55", 
            "#44dd88", "#22ccbb", "#00bbcc", "#0099cc", "#3366bb", "#663399"
        )

    def compose(self) -> ComposeResult:
        """
        Define a estrutura da interface gráfica da aplicação.
        """
        yield Header()
        with Middle():
            with Center():
                with Center():
                    yield Button("Iniciar Progresso", id='reset')  # Botão para iniciar a simulação
                with ItemGrid():
                    for i in range(self.items):  # Criando múltiplas barras de progresso
                        with Container():
                            yield Label(f'Barra {i}', id=f'lab{i}')
                            yield ProgressBar(id=f"bar{i}", total=100, show_eta=False, show_percentage=True, gradient=self.gradient)

    def on_button_pressed(self) -> None:
        """
        Evento acionado quando o botão "Iniciar Progresso" é pressionado.
        Verifica o estado das barras e inicia sua atualização.
        """
        count = sum(1 for b in self.bars if b == 'Winner')
        if count <= 1:
            for i in range(self.items):
                bar = self.query_one(f"#bar{i}", ProgressBar)
                lab = self.query_one(f"#lab{i}", Label)
                lab.visible = True
                bar.visible = True
                bar.update(progress=50)
                self.bars[i] = 'Winner'
    
        for i in range(self.items):
            if self.bars[i] == 'Winner':
                bar = self.query_one(f"#bar{i}", ProgressBar)
                bar.update(progress=50)
            
            # Inicia threads para atualizar o progresso da barra de forma assíncrona
            Thread(target=self.update_progress, args=(i, 5)).start()
            Thread(target=self.update_progress, args=(i, -5)).start()
    
    def update_progress(self, bar_id: int, amount: int) -> None:
        """
        Simula a atualização contínua da barra de progresso em uma thread separada.
        
        :param bar_id: Identificador da barra de progresso.
        :param amount: Quantidade a ser incrementada ou decrementada no progresso.
        """
        while True:
            resultado = self.call_from_thread(self.advance_bar, bar_id, amount)  # Atualiza a UI na thread principal
            if resultado:  # Se houver um vencedor, encerra a atualização da barra
                self.bars[bar_id] = resultado
                break

    def advance_bar(self, bar_id: int, amount: int) -> str:
        """
        Atualiza a barra de progresso de forma segura e verifica se há um vencedor.
        
        :param bar_id: Identificador da barra de progresso.
        :param amount: Quantidade a ser incrementada ou decrementada no progresso.
        :return: 'Winner' se a barra atingir 100%, 'Loser' se atingir 0%.
        """
        bar = self.query_one(f"#bar{bar_id}", ProgressBar)
        if bar.progress <= 0:
            self.bars[bar_id] = 'Loser'
            lab = self.query_one(f"#lab{bar_id}", Label)
            lab.visible = False
            bar.visible = False
            return 'Loser'
        elif bar.progress >= 100:
            return 'Winner'
        else:
            bar.advance(amount)  # Atualiza o progresso

if __name__ == "__main__":
    FundingProgressApp().run()
