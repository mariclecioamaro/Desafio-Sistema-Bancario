import textwrap

def menu():
    menu = """\n
    ---------------------------------------------------------
    [d]\tDepositar
    [s]\tSacar
    [c]\tCriar Conta
    [u]\tNovo Usuário
    [l]\tListar Contas
    [e]\tExtrato
    [x]\tSair
    ---------------------------------------------------------
    Informe a operação que deseja realizar digitando a letra correspondente a operação: 
    """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor: .2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou. O valor informado é inválido.")
        
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, quant_saques, limit_saques):
    excedeu_saldo = valor > saldo
    excedeu_limit = valor > limite
    excedeu_saques = quant_saques >= limit_saques

    if excedeu_saldo:
        print("Operação falhou. Voçê não tem saldo suficiente.")
    elif excedeu_limit:
        print("Operação falhou. O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou. Quantidade de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor: .2f}\n"
        quant_saques += 1
    else:
        print("Operação falhou. O valor informado é inválido.")

    return saldo, extrato

def exibeExtrato(saldo, /, *, extrato):
    print("\n--------EXTRATO----------")
    print("Não foram realizadas movimentações na conta." if not extrato else extrato)
    print(f"\nSaldo:\t\tRS {saldo: .2f}")
    print("----------------------------")

def createUser(users):
    cpf = input("informe o número do CPF (Digite somente os números): ")
    user = filterUser(cpf, users)

    if user:
        print("Já existe um usuário cadastrado com esse CPF!")
        return
    
    name = input("Informe o seu nome completo: ")
    dataNascimento = input("Informe sua data de nascimneto (dd-mm-aaaa): ")
    endereco = input("Informe o seu endereço (Logradouro - número - bairro - Cidade - UF): ")

    users.append({"nome": name, "dataNascimento": dataNascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso! ")

def filterUser(cpf, users):
    usersFilter = [user for user in users if user["cpf"] == cpf]
    return usersFilter[0] if usersFilter else None

def criarConta(agencia, numConta, users):
    cpf = input("Informe o CPF do usuário cadastrado: ")
    user = filterUser(cpf, users)

    if user:
        print("Conta criada com sucesso! ")
        return {"agencia": agencia, "numConta": numConta, "user": user}
    print("Usuário não encontrado. Criação de conta interrompida...")

def listarContas(contas):
    for conta in contas:
        linha = f"""
        Agência:\t{conta["agencia"]},
        C/C:\t\t{conta["numConta"]}
        Titular:\t{conta["user"]["name"]}
        """
        print("-" * 100)
        print(textwrap.dedent(linha))

def main():

    LIMIT_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limit = 500
    extrato = ""
    quant_saques = 0
    users = []
    contas = []

    while(True):
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor a ser depositado: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor para sacar: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limit=limit,
                quant_saques=quant_saques,
                Limit_saques=LIMIT_SAQUES
            )
            
        elif opcao == "e":
            exibeExtrato(saldo, extrato=extrato)

        elif opcao == "u":
            createUser(users)

        elif opcao == "c":
            numConta = len(contas) + 1
            conta = criarConta(AGENCIA, numConta, users)

            if conta:
                contas.append(conta)

        elif opcao == "l":
            listarContas(contas)

        elif opcao == "x":
            break
        
        else:
            print("Operação inválida. Por favor selecione a operação desejada")
    
main()
