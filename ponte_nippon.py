from guia_cultural import (
    pesquisar_dicionario,
    exibir_guia_cultural,
    checklist_para_viagem,
)

def exibir_menu():
    print("\n" + "="*20)
    print("  MENU PRINCIPAL")
    print("="*20)
    print("1 - Documentação")
    print("2 - Dicionário Japonês-Português")
    print("3 - Guia Cultural")
    print("4 - Sair")
    print("="*20)
     
def menu_principal():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-4): ")

        if opcao == "1":
            print("\n-> Olá, usuário! Aqui você encontra todos os seus documentos e requisitos.")
            checklist_para_viagem()

        elif opcao == "2":
            pesquisar_dicionario()

        elif opcao == "3":
            print("\n-> Este é o guia cultural sobre o Japão.")
            print("-> Aqui você encontrará informações sobre costumes, tradições e etiqueta japonesa.")
            print("=-" * 25)
            exibir_guia_cultural()

        elif opcao == "4":
            print("\nEncerrando o programa... Até logo!")
            break

        else:
            print("\nDígito incorreto. Digite um número válido entre 1 e 4.")


if __name__ == "__main__":
    menu_principal()
