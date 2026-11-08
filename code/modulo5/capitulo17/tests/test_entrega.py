import pytest
from ecommerce.categoria import Categoria
from ecommerce.entrega import Entrega, EntregaCorreios, EntregaTransportadora
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestEntrega:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.pedido = Pedido()
        self.pedido.adicionar_item(self.notebook, 1)

    def test_entrega_e_abstrata(self) -> None:
        with pytest.raises(TypeError):
            Entrega(self.pedido, "BR000001")  # type: ignore[abstract]

    def test_correios_pac_tem_prazo_maior_que_sedex(self) -> None:
        pac = EntregaCorreios(self.pedido, "BR000001", modalidade="PAC")
        sedex = EntregaCorreios(self.pedido, "BR000002", modalidade="SEDEX")
        assert pac.prazo_estimado() > sedex.prazo_estimado()

    def test_transportadora_conhece_o_nome_da_parceira(self) -> None:
        entrega = EntregaTransportadora(self.pedido, "TR000001", transportadora="Transportadora Sul")
        assert entrega.transportadora == "Transportadora Sul"
        assert entrega.prazo_estimado() == 5

    def test_etiqueta_inclui_rastreio_e_prazo(self) -> None:
        entrega = EntregaCorreios(self.pedido, "BR000009SE", modalidade="SEDEX")
        etiqueta = entrega.etiqueta()
        assert "BR000009SE" in etiqueta
        assert "3 dias" in etiqueta
