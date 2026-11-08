import pytest
from ecommerce.notificacao import Notificacao, NotificacaoEmail, NotificacaoSMS


class TestNotificacao:

    def test_notificacao_e_abstrata(self) -> None:
        with pytest.raises(TypeError):
            Notificacao()  # type: ignore[abstract]

    def test_email_envia_para_o_destinatario(self, capsys: pytest.CaptureFixture[str]) -> None:
        NotificacaoEmail().enviar("maria@email.com", "Pedido confirmado")
        saida = capsys.readouterr().out
        assert "E-MAIL" in saida
        assert "maria@email.com" in saida
        assert "Pedido confirmado" in saida

    def test_sms_corta_mensagem_no_limite(self, capsys: pytest.CaptureFixture[str]) -> None:
        mensagem_longa = "a" * 300
        NotificacaoSMS().enviar("+55 47 90000-0000", mensagem_longa)
        saida = capsys.readouterr().out
        assert "a" * NotificacaoSMS.LIMITE in saida
        assert "a" * (NotificacaoSMS.LIMITE + 1) not in saida
