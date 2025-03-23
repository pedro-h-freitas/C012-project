from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll, Middle, ItemGrid, Grid, HorizontalGroup, Vertical, Horizontal, HorizontalScroll, Container
from textual.widgets import Button, Header, Label, ProgressBar
from threading import Thread
from time import sleep
from textual.color import Gradient

class FundingProgressApp(App[None]):
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
    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.items = 60
        self.vencedor = ['Ganhou']*self.items
        self.gradient = Gradient.from_colors(
            "#881177",
            "#aa3355",
            "#cc6666",
            "#ee9944",
            "#eedd00",
            "#99dd55",
            "#44dd88",
            "#22ccbb",
            "#00bbcc",
            "#0099cc",
            "#3366bb",
            "#663399",
        )
    def compose(self) -> ComposeResult:
        yield Header()
        with Middle():
            with Center():
                with Center():
                    yield Button("Start Progress", id='reset')
                with ItemGrid():
                    for i in range(self.items):
                        with Container():
                            yield Label(f'Barra {i}', id=f'lab{i}')
                            yield ProgressBar(id=f"bar{i}", total=100, show_eta=False, show_percentage=False)
    def on_mount(self):
        pass

    def on_button_pressed(self) -> None:
        # Inicia threads para cada barra
        count = 0
        for vencedor in self.vencedor:
            if vencedor == "Ganhou":
                count += 1

        if count <= 1:
            for i in range(self.items):
                bar = self.query_one(f"#bar{i}", ProgressBar)
                lab = self.query_one(f"#lab{i}", Label)
                lab.visible = True
                bar.visible = True
                bar.update(progress=50)
                self.vencedor[i] = 'Ganhou'
    
        for i in range(self.items):
            if self.vencedor[i] == 'Ganhou':
                bar = self.query_one(f"#bar{i}", ProgressBar)
                bar.update(progress=50)
        
            Thread(target=self.update_progress, args=(i,10)).start()
            Thread(target=self.update_progress, args=(i,-10)).start()
            
    
    def update_progress(self, bar_id: int, amount: int) -> None:
        """Simula uma atualização contínua da barra de progresso."""
        while True:
            vencedor = self.call_from_thread(self.advance_bar, bar_id, amount)  # Atualiza a UI na thread principal
            if vencedor:
                self.vencedor[bar_id] = vencedor
                break

    def advance_bar(self, bar_id: int, amount: int) -> str:
        """Atualiza a barra de progresso de forma segura."""
        bar = self.query_one(f"#bar{bar_id}", ProgressBar)
        if(bar.progress <= 0):
            self.vencedor[bar_id] = 'Perdeu'
            lab = self.query_one(f"#lab{bar_id}", Label)
            lab.visible = False
            bar.visible = False
            return 'Perdeu'
        elif(bar.progress >= 100):
            return 'Ganhou'
        else:
            bar.advance(amount)

if __name__ == "__main__":
    FundingProgressApp().run()
