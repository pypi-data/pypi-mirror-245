from typing import Any

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult, App
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Checkbox, Button, TabbedContent, TabPane, Static, Header, Footer

from src.cluster_info import ClusterNode, cluster_info
from src.config import Config
from src.slurm_viewer import Loading
from src.sortable_data_table import SortableDataTable


class ClusterWidget(Widget):
    CSS = """
    #horizontal {
        height: auto;
    }
    
    #spacer {
        width: 1fr;
    }
    
    #data_table {
        width: 1fr;
        height: 1fr;
        border: panel limegreen;
    }
    """

    def __init__(self, config: Config, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.config = config
        self.cluster_info = cluster_info(self.config)

    def compose(self) -> ComposeResult:
        with Horizontal(id='horizontal'):
            yield Checkbox(label='GPU only', id='show_gpu')
            yield Checkbox(label='GPU available', id='show_gpu_available')
            yield Static(id='spacer')
            yield Button(label='Select columns', id='show_columns')
            yield Button(label='Refresh', id='refresh')
        yield SortableDataTable(id='data_table')

    def on_mount(self) -> None:
        self._cluster_data_table()

    @staticmethod
    def _filter_nodes(nodes: list[ClusterNode], gpu: bool, gpu_available: bool) -> list[ClusterNode]:
        result = []
        for node in nodes:
            if node.gpu_tot == 0 and gpu:
                continue

            if node.gpu_avail == 0 and gpu_available:
                continue

            result.append(node)
        return result

    @on(Checkbox.Changed, '#show_gpu')
    @on(Checkbox.Changed, '#show_gpu_available')
    def show_gpu(self, _: Checkbox.Changed) -> None:
        data_table = self.query_one('#data_table', SortableDataTable)
        data_table.clear()

        gpu = self.query_one('#show_gpu', Checkbox).value
        gpu_available = self.query_one('#show_gpu_available', Checkbox).value

        self._update_data_table(self._filter_nodes(self.cluster_info, gpu, gpu_available), data_table)

    @on(Button.Pressed, '#show_columns')
    def show_columns(self, _: Checkbox.Changed) -> None:
        pass

    @work(thread=True)
    @on(Button.Pressed, '#cluster_refresh')
    def refresh_info(self, _: Checkbox.Changed) -> None:
        data_table = self.query_one('#cluster_data_table', SortableDataTable)
        data_table.clear()

        with Loading(data_table):
            self.cluster_info = cluster_info(self.config)

        gpu = self.query_one('#cluster_show_gpu', Checkbox).value
        gpu_available = self.query_one('#cluster_show_gpu_available', Checkbox).value

        self._update_data_table(self._filter_nodes(self.cluster_info, gpu, gpu_available), data_table)

    def _update_data_table(self, nodes: list[ClusterNode], table: SortableDataTable) -> None:
        for index, row in enumerate(nodes, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = [getattr(row, key) for key in self.config.node_columns]
            table.add_row(*data, label=label)

    def _cluster_data_table(self) -> None:
        data_table = self.query_one('#data_table', SortableDataTable)
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.node_columns)
        data_table.border_title = f'{len(self.cluster_info)} nodes'

        self._update_data_table(self.cluster_info, data_table)


class ClusterApp(App[None]):
    def __init__(self, config: Config, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.config = config

    def compose(self) -> ComposeResult:
        yield Header(name=self.config.server, show_clock=True)
        with TabbedContent():
            with TabPane('Cluster', id='tab_cluster'):
                with Vertical():
                    yield ClusterWidget(self.config)
        yield Footer()
