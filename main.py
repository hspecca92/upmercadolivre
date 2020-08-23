#!/python3.8

import requests
import pyodbc

#Classe principal para iniciar restartar a compilação se solicitado.
def main():
    #Função para retornar a conexão com o banco de dados
    def retornar_conexao_sql():
        server = 'localhost' 
        database = 'mercadolivre' 
        #### Autenticação de conexão com o banco de dados caso o Trusted_Connection não seja ideal
        #username = '*** ' 
        #password = '*** ' 
        string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';Trusted_Connection=yes;'
        return pyodbc.connect(string_conexao)
    
    #Aprensetação do programa
    print("@@@@  @     @@@@  @@@@  @   @   @     @@@@   @@@@  @@@@@")
    print("@  @  @     @  @  @     @  @    @       @    @       @ ")
    print("@@@   @     @@@@  @     @ @     @       @    @@@@    @ ")
    print("@  @  @     @  @  @     @  @    @       @       @    @ ")
    print("@@@@  @@@@  @  @  @@@@  @   @   @@@@  @@@@   @@@@    @ ")
    print()
    
    # Entrada de dados para realizar uma solicitação ao programa
    usr_input = input("\n Escolha uma opção: \n\n"
                    "1 - Exibir lista de IPs Maliciosos TorList \n"
                    "2 - Exibir lista de IPs Maliciosos inseridas Manualmente\n"
                    "3 - Atualizar lista de IPs TOR, restrição de 30minutos (Deletar e Inserir)\n"
                    "4 - Inserir IP na Lista Manual (ex: 172.2.4.2 / 172242)\n"
                    "5 - Deletar um IP da Lista Manual\n"
                    "6 - Sair\n\n "
                    "Opção: ")
    #Opção 1 - Exibe a lista inserida através da API do site https://www.dan.me.uk/torlist/?exit
    if usr_input == "1":
            #Função retornar_conexao_sql para abrir conexão com o banco e Variável do cursor
            conexao = retornar_conexao_sql()
            cursor = conexao.cursor()
            print ("Exibindo a lista TOR")
            cursor.execute("SELECT * FROM blacklist")
            row = cursor.fetchall()
            print("Resultado", row)
            conexao.close()
            option = int(input("\nDeseja realizar uma nova operação? \n1. Sim\n2. Sair\n Opção: "))
            if option == 1:
                main()
            else:
                print("Até logo :)")
    
    #Opção 2 - Exibe a lista inserida manualmente no sistema.
    elif usr_input == "2":
            #Variável do cursor
            conexao = retornar_conexao_sql()
            cursor = conexao.cursor()
            #Select para exibição dos valores
            print ("Exibindo a lista Manual\n")
            cursor.execute("SELECT * FROM manuallist")
            row = cursor.fetchall()
            print("Resultado: ", row, "\n") 
            conexao.close()
            option = int(input("\nDeseja realizar uma nova operação? \n1. Sim\n2. Sair\n Opção: "))
            if option == 1:
                main()
            else:
                print("Até logo :)")
   
    #Opção 3 -Limpa a tabela e Busca em um determinado site os IPs maliciosos inserindo na tabela.
    elif usr_input == "3":
            conexao = retornar_conexao_sql()
            cursor = conexao.cursor()
            cursor.execute("DELETE blacklist")
            conexao.commit()
            
            #Receber a lista
            tornode = requests.get('https://www.dan.me.uk/torlist/?exit')
            #print(tornode.text)
            #Insert dos valores na tabela do SQL obtidos da lista 
            tornode = tornode.text.split()
            for x in tornode:
                cursor.execute("INSERT INTO blacklist (ip) VALUES (?)", (x))
            conexao.commit()
            conexao.close()

            print("<-------------------------->")
            print("Dados Inseridos com Sucesso!")
            print("<-------------------------->")

            option = int(input("\nDeseja realizar uma nova operação? \n1. Sim\n2. Sair\n Opção: "))
            if option == 1:
                main()
            else:
                print("Até logo :)")
    
    #Opção 4 - Insere manualmente um IP na tabela manualip.
    elif usr_input == "4":
        conexao = retornar_conexao_sql()
        cursor = conexao.cursor()
        ipmanual = input("Digite o numero de IP que deseja adicionar: ")
        data2 = str(ipmanual)
        cursor.execute("INSERT INTO manuallist (manualip) VALUES (?)", (data2))
        conexao.commit()
        print ("IP Inserido com sucesso")
        print(" <------------------------------->")
        conexao.close()
        option = int(input("\nDeseja realizar uma nova operação? \n1. Sim\n2. Sair\n Opção: "))
        if option == 1:
            main()
        else:
            print("Até logo :)")
    
    #Opção 4 - Remove manualmente um IP na tabela manualip.
    elif usr_input == "5":
        conexao = retornar_conexao_sql()
        cursor = conexao.cursor()
        ipmanualdelete = input("Qual IP deseja remover da lista: ")
        cursor.execute("DELETE manuallist where manualip = (?) ", (ipmanualdelete))
        print ("\nDeletado com sucesso!")
        print ("<------------------->\n")
        conexao.commit()
        conexao.close()
        option = int(input("Deseja realizar uma nova operação? \n1. Sim\n2. Sair\n Opção: "))
        if option == 1:
            main()
        else:
            print("Até logo :)")
    #Opção 4 - Sai do sistema.
    elif usr_input == "6":
            print("Até logo :)")
    else:
        print("Opção inexistente, tente novamente!")
        main()
if __name__ == '__main__':
    main()