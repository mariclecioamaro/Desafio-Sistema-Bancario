menu = """
---------------------------------------------------------
[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair
---------------------------------------------------------
Digite a letra correspondente a operação que deseja fazer:
---------------------------------------------------------
"""

saldo = 0
limit = 500
extrato = ""
quant_saques = 0
LIMIT_SAQUE = 3

while(True):
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor: .2f}\n"

        else:
            print("Operação falhou. O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor para sacar: "))

        excedeu_saldo = valor > saldo
        excedeu_limit = valor > limit
        excedeu_saques = quant_saques >= LIMIT_SAQUE

        if excedeu_saldo:
            print("Operação falhou. Voçê não tem saldo suficiente.")
        elif excedeu_limit:
            print("Operação falhou. O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou. Quantidade de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor: .2f}\n"
            quant_saques += 1
        else:
            print("Operação falhou. O valor informado é inválido.")
    elif opcao == "e":
        print("\n--------EXTRATO----------")
        print("Não foram realizadas movimentações na conta." if not extrato else extrato)
        print(f"\nSaldo: RS {saldo: .2f}")
        print("----------------------------")
    elif opcao == "x":
        break
    else:
        print("Operação inválida. Por favor selecione a operação desejada")
    