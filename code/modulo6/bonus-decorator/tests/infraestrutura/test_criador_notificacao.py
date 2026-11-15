import pytest
from ecommerce.dominio.canal_notificacao import CanalNotificacao
from ecommerce.infraestrutura.criador_notificacao import CriadorNotificacao
from ecommerce.infraestrutura.notificacao import NotificacaoEmail, NotificacaoSMS


class TestCriadorNotificacao:

    def setup_method(self) -> None:
        self.criador = CriadorNotificacao()

    def test_cria_notificacao_email(self) -> None:
        assert isinstance(self.criador.criar(CanalNotificacao.EMAIL), NotificacaoEmail)

    def test_cria_notificacao_sms(self) -> None:
        assert isinstance(self.criador.criar(CanalNotificacao.SMS), NotificacaoSMS)

    def test_canal_desconhecido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            self.criador.criar("email")  # type: ignore[arg-type]
