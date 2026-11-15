from ecommerce.dominio.canal_notificacao import CanalNotificacao
from ecommerce.aplicacao.notificacao import Notificacao
from ecommerce.infraestrutura.notificacao import NotificacaoEmail, NotificacaoSMS


class CriadorNotificacao:

    def criar(self, canal: CanalNotificacao) -> Notificacao:
        if canal == CanalNotificacao.EMAIL:
            return NotificacaoEmail()
        if canal == CanalNotificacao.SMS:
            return NotificacaoSMS()
        raise ValueError(f"Canal de notificacao desconhecido: {canal}")


if __name__ == "__main__":
    criador = CriadorNotificacao()
    for canal in CanalNotificacao:
        notificacao = criador.criar(canal)
        print(f"{canal.name}: {type(notificacao).__name__}")
