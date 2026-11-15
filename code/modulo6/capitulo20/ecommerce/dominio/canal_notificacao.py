from enum import Enum


class CanalNotificacao(Enum):
    EMAIL = "email"
    SMS = "sms"


if __name__ == "__main__":
    for canal in CanalNotificacao:
        print(canal.name, "->", canal.value)
