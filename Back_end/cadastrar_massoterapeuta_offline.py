# Back_end/cadastrar_massoterapeuta_offline.py
from Back_end.massoterapeuta import cadastrar_massoterapeuta

def main():
    print("Cadastro offline de massoterapeuta")

    # Valores padrão caso o usuário apenas pressione Enter
    nome = input("Nome (Higashi): ") or "Higashi"
    telefone = input("Telefone (1197748391839): ") or "1197748391839"
    sexo = input("Sexo (Masculino/Feminino): ") or "Masculino"
    data_nascimento = input("Data de nascimento (1976-10-10): ") or "1976-10-10"
    email = input("Email (higashi@gmail.com): ") or "higashi@gmail.com"
    senha = input("Senha (higashi7@): ") or "higashi7@"

    massoterapeuta_id = cadastrar_massoterapeuta(nome, telefone, sexo, data_nascimento, email, senha)

    if massoterapeuta_id:
        print(f"Massoterapeuta cadastrado com sucesso! ID: {massoterapeuta_id}")
    else:
        print("Erro ao cadastrar massoterapeuta.")

if __name__ == "__main__":
    main()
