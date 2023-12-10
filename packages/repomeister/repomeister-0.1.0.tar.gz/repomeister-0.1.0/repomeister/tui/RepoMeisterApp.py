from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class RepoMeisterApp(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

