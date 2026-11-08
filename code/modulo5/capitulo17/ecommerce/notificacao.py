from abc import ABC, abstractmethod


class Notificacao(ABC):

    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        ...


class NotificacaoEmail(Notificacao):

    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[E-MAIL -> {destinatario}] {mensagem}")


class NotificacaoSMS(Notificacao):

    # SMS tem limite de caracteres; mensagens longas sao cortadas.
    LIMITE = 160

    def enviar(self, destinatario: str, mensagem: str) -> None:
        texto = mensagem[: self.LIMITE]
        print(f"[SMS -> {destinatario}] {texto}")


if __name__ == "__main__":
    NotificacaoEmail().enviar("maria@email.com", "Seu pedido foi confirmado.")
    NotificacaoSMS().enviar("+55 47 99999-0000", "Seu pedido foi enviado.")
