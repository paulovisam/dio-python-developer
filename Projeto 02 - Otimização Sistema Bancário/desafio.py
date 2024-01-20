import textwrap


def menu():
    menu = """\n
    --------------- MENU ---------------
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def deposit(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo, extrato


def withdraw(*, balance, amount, extract, limite, numero_saques, limite_saques):
    excedeu_saldo = amount > balance
    excedeu_limite = amount > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")

    elif amount > 0:
        balance -= amount
        extract += f"Saque:\t\tR$ {amount:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return balance, extract


def extract(balance, /, *, extract):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extract else extract)
    print(f"\nSaldo:\t\tR$ {balance:.2f}")
    print("==========================================")


def create_user(users):
    cpf = input("Informe o CPF (somente número): ")
    user = get_user(cpf, users)

    if user:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    users.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def get_user(cpf, user):
    usuarios_filtrados = [usuario for usuario in user if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def create_account(agencia, numero_conta, users):
    cpf = input("Informe o CPF do usuário: ")
    user = get_user(cpf, users)

    if user:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": user}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def get_account(accounts):
    for account in accounts:
        linha = f"""\
            Agência:\t{account['agencia']}
            C/C:\t\t{account['numero_conta']}
            Titular:\t{account['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    balance = 0
    limit = 500
    extrato = ""
    numero_saques = 0
    users = []
    accounts = []

    while True:
        opcao = menu()

        if opcao == "d":
            value = float(input("Informe o valor do depósito: "))

            balance, extrato = deposit(balance, value, extrato)

        elif opcao == "s":
            value = float(input("Informe o valor do saque: "))

            balance, extrato = withdraw(
                balance=balance,
                amount=value,
                extract=extrato,
                limite=limit,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            extract(balance, extract=extrato)

        elif opcao == "nu":
            create_user(users)

        elif opcao == "nc":
            numero_conta = len(accounts) + 1
            conta = create_account(AGENCIA, numero_conta, users)

            if conta:
                accounts.append(conta)

        elif opcao == "lc":
            get_account(accounts)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()