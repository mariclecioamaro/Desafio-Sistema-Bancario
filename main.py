import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizarTransacao(self, conta, transacao):
        transacao.registrar(conta)

    def addConta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, dataNascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dataNascimento = dataNascimento
        self.cpf = cpf

class Conta:
    def __init__(self, num, cliente):
        self.saldo = 0
        self.num = num
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def novaConta(cls, cliente, num):
        return cls(num, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def num(self):
        return self._num
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    def sacar(self, valor):
        saldo = self.saldo
        excedeuSaldo = valor > saldo

        if excedeuSaldo:
            print("Operação falhou. Você não tem saldo suficiente...")
        elif valor > 0:
            self._saldo -= valor
            print("Saque efetuado com sucesso!")
            return True
        else:
            print("Operação falhou. O valor informado é inválido...")

        return False
    def depositar(self, valor):
        if valor > 0:
            self.valor += valor
            print("Depósito efetuado com sucesso!")
        else:
            print("Operação falhou. O valor informado é inválido...")
            return False
        
        return True
class ContaCorrente(Conta):
    def __init__(self, num, cliente, limite=500, limiteSaques=3):
        super().__init__(num, cliente)
        self.limite = limite
        self.limiteSaques = limiteSaques

    def sacar(self, valor):
        numSaques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
        )

        excedeuLimite = valor > self.limite
        excedeuSaques = numSaques >= self.limiteSaques

        if excedeuLimite:
            print("Operação falhou! O valor do saque excede o limite...")
        elif excedeuSaques:
            print("Operação falhou! Quantidade de saques excedido...")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.num}
            Titular:\t{self.cliente.nome}
        """
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transaçoes(self):
        return self._transacoes
    
    def addTransacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucessTransacao = conta.sacar(self.valor)

        if sucessTransacao:
            conta.historico.addTransacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        sucessTransacao = conta.depositar(self.valor)

        if sucessTransacao:
            conta.historico.addTransacao(self)

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

def filterUser(cpf, users):
    usersFilter = [user for user in users if user.cpf == cpf]
    return usersFilter[0] if usersFilter else None

def recuperarConta(user):
    if not user.contas:
        print("Cliente não possui conta...")
        return
    # FIXME: o cliente não pode escolher a conta
    return user.contas[0]

def depositar(users):
    cpf = input("Informe o número do CPF do cliente: ")
    user = filterUser(cpf, users)

    if not user:
        print("Cliente não encontrado...")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperarConta(user)
    if not conta:
        return
    
    user.realizarTransacao(conta, transacao)

def sacar(users):
    cpf = input("Informe o número do CPF do cliente: ")
    user = filterUser(cpf, users)

    if not user:
        print("Cliente não encontrado.")
        return
    valor = float(input("Informe o valor que deseja saacar: "))
    transacao = Saque(valor)

    conta = recuperarConta(user)
    if not conta:
        return
    
    user.realizarTransacao(conta, transacao)

def exibeExtrato(users):
    cpf = input("Informe o número do CPF do cliente: ")
    user = filterUser(cpf, users)

    if not user:
        print("Cliente não encontrado.")
        return
    
    conta = recuperarConta(user)
    if not conta:
        return
    
    print("\n-------------EXTRATO-------------------")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações na conta. "
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("-----------------------------------------")

def createUser(users):
    cpf = input("Informe o número do CPF do cliente: ")
    user = filterUser(cpf, users)

    if user:
        print("Cliente não encontrado.")
        return
    
    nome = input("Informe o nome completo: ")
    dataNascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro - número - bairro - cidade - estado/UF): ")

    user = PessoaFisica(nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco)
    users.append(user)

    print("Cliente cadastrado com sucesso! ")

def criarConta(numConta, users, contas):
    cpf = input("Informe o número do CPF do cliente: ")
    user = filterUser(cpf, users)

    if not user:
        print("Cliente não encontrado. Operação interrompida...")
        return
    
    conta = ContaCorrente.novaConta(user=user, num=numConta)
    contas.append(conta)

    print("Conta criada com sucesso! ")

def listarContas(contas):
    for conta in contas:
        print("-" * 100)
        print(textwrap.dedent(str(conta)))

def main():

    users = []
    contas = []

    while(True):
        opcao = menu()

        if opcao == "d":
            depositar(users)

        elif opcao == "s":
            sacar(users)
            
        elif opcao == "e":
            exibeExtrato(users)

        elif opcao == "u":
            createUser(users)

        elif opcao == "c":
            numConta = len(contas) + 1
            conta = criarConta(numConta, users)

            if conta:
                contas.append(conta)

        elif opcao == "l":
            listarContas(contas)

        elif opcao == "x":
            break
        
        else:
            print("Operação inválida. Por favor selecione a operação desejada")
    
main()
