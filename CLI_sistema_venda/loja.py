from database import Database
from helper import logger
import importlib
import consultas
import os
import sys
from tabulate import tabulate
from colorama import Fore, init
init(autoreset=True)

class SistemaVendasCLI:
    def __init__(self, db : Database):
        self.db = db
        logger.info("Sistema de Vendas - CLI Inicializado \n")

    def limpar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        

    def exibir_resultado(self, colunas: list[str], linhas: list[tuple], descricao: str = "") -> None:
        if linhas:
            tabela = tabulate(linhas, headers=colunas, tablefmt="fancy_grid", showindex=False)
            largura_tabela = len(tabela.splitlines()[0])
            print(descricao.center(largura_tabela))
            print(tabela)
        else:
            print(descricao.center(50))
            logger.info("consulta realizada com sucesso, mas sem retorno")
            

    def menu_exercicios(self):
        while True:
            importlib.reload(consultas)
            Consulta = consultas.Consulta 
            
            opcoes = []
            for _, consulta in enumerate(Consulta, 1):
                opcoes.append(consulta.value[1])
            
            opcoes.append("0. Voltar ao Menu Principal")
            
            col1 = opcoes[:8]
            col2 = opcoes[8:16]
            
            linhas = []
            for i in range(max(len(col1), len(col2))):
                l1 = col1[i] if i < len(col1) else ""
                l2 = col2[i] if i < len(col2) else ""
                linhas.append((l1, l2))
                
            tabela = tabulate(
                linhas,
                tablefmt="fancy_grid",
                stralign="left"
            )
            print("MENU DE CONSULTAS".center(len(tabela.splitlines()[0])))
            print(f"{tabela} \n")
            
            opcao = input("Escolha uma opção > ").strip()
            
            if opcao == "0":
                break

            opcoes = {str(i+1): c for i, c in enumerate(Consulta)}
            consulta = opcoes.get(opcao)

            if consulta:
                self.limpar_terminal()
                try:
                    colunas, linhas = self.db.executar_query(consulta.value[0])
                except Exception as e:
                    logger.error(e, exc_info=True)
                    print("")
                else:
                    self.exibir_resultado(colunas, linhas, consulta.value[1])
                    
            else: logger.error("Operação não reconhecida")

            input("\nPressione [ENTER] para continuar... \n")
            self.limpar_terminal()


if __name__ == "__main__":
    db = Database(
        host = "localhost",
        user = "postgres",
        password = "postgres",
        database = "postgres"
    )
    
    if not db.conectar():
        logger.critical("Falha ao se conectar com o banco de dados!")
        sys.exit(1)

    try:
        cli = SistemaVendasCLI(db)
        cli.menu_exercicios()
    finally:
        db.desconectar()
