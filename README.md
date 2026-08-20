# Atividade – Backdoor que abre a porta 30041

**Disciplina:** Segurança da Informação
**Objetivo:** demonstrar, em laboratório, como um *backdoor* abre uma porta TCP
na máquina e a usa como canal de acesso remoto — e, principalmente, como
**detectar e se defender** desse tipo de ameaça.

> ⚠️ **Uso ético/legal:** rode apenas na sua própria máquina ou numa VM isolada
> de aula. Expor isto na rede de terceiros configura crime (art. 154-A do Código
> Penal – invasão de dispositivo informático). O propósito é aprender a defender.

---

## 1. O que é um backdoor / bind shell

Um **backdoor** é um canal de acesso remoto não autorizado a um sistema. O tipo
mais simples é o **bind shell**: um programa que **escuta** numa porta TCP e
executa na máquina qualquer comando que chegar por ela.

Fluxo do que acontece com a porta 30041:

```
socket()  ->  bind(("127.0.0.1", 30041))  ->  listen()  ->  accept()
   |               |                            |             |
 cria o        associa e ABRE               fica em      aceita a conexão
 socket        a porta 30041                estado LISTEN   do atacante
```

A partir do `accept()`, tudo que o cliente enviar é executado via
`subprocess.run(comando, shell=True)` e a saída volta pela rede.

---

## 2. Arquivos

| Arquivo             | Papel                                                        |
|---------------------|-------------------------------------------------------------|
| `backdoor.py`       | O backdoor. Abre a porta **30041** e executa comandos.      |
| `cliente_teste.py`  | O "atacante": conecta na 30041 e envia comandos.            |
| `README.md`         | Esta documentação (teoria + demonstração + defesa).         |

---

## 3. Como executar (demonstração em laboratório)

Precisa de **Python 3** instalado. Abra **dois terminais na mesma máquina**:

**Terminal 1 – sobe o backdoor (abre a porta):**
```bash
python backdoor.py
```
Saída esperada:
```
[+] Backdoor escutando em 127.0.0.1:30041
[+] Aguardando conexão... (Ctrl+C para encerrar)
```

**Terminal 2 – conecta como atacante:**
```bash
python cliente_teste.py
```
Depois digite comandos, por exemplo `whoami`, `hostname`, `dir` (Windows) /
`ls` (Linux). Digite `sair` para encerrar.

> Alternativa clássica sem o cliente próprio: usar o **Netcat**
> `ncat 127.0.0.1 30041` — vale citar no relatório.

---

## 4. Como PROVAR que a porta 30041 foi aberta

Com o `backdoor.py` rodando, em outro terminal:

- **Windows:** `netstat -ano | findstr 30041`
- **Linux/Mac:** `ss -tlnp | grep 30041`  (ou `netstat -tlnp | grep 30041`)

Você verá a porta em estado **LISTENING**. Tire um print disso para o relatório.

---

## 5. Detecção e Defesa (parte que a disciplina valoriza)

Como um administrador/analista descobre e neutraliza um backdoor assim:

1. **Portas em escuta:** `netstat -ano` / `ss -tlnp` revelam portas suspeitas
   (uma porta alta e "aleatória" como 30041, sem serviço legítimo associado).
2. **Processo dono da porta:** o PID do `netstat` leva ao processo
   (`tasklist /FI "PID eq <pid>"` no Windows) — identifica o executável malicioso.
3. **Firewall:** bloquear conexões de entrada na porta (regra *inbound deny*).
   Firewalls bem configurados negam por padrão portas não autorizadas.
4. **IDS/IPS** (ex.: Snort/Suricata) detectam padrões de bind/reverse shell.
5. **Antivírus/EDR** sinalizam o padrão "socket + subprocess/shell".
6. **Princípio do menor privilégio** e monitoramento de novos processos que
   chamam `bind()`/`listen()` dificultam a persistência do backdoor.

### Por que `127.0.0.1` no código?
No `backdoor.py` o `HOST` é `127.0.0.1` (loopback) de propósito: assim a porta
só é acessível da própria máquina, mantendo a demonstração contida. Um backdoor
"de verdade" usaria `0.0.0.0` para escutar em todas as interfaces — justamente
o comportamento que o firewall e o IDS devem barrar. Isso mostra, na prática,
a diferença entre um teste controlado e uma exposição real.

---

## 6. Conclusão sugerida para o relatório

Um bind shell demonstra que "abrir uma porta" é trivial em poucas linhas de
código — o que torna a **defesa em profundidade** (firewall + IDS/IPS + EDR +
monitoramento de portas e processos + menor privilégio) indispensável. Conhecer
o funcionamento do ataque é o que permite reconhecê-lo e bloqueá-lo.
