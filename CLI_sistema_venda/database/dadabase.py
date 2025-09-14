import psycopg2
from helper import time_execution, logger

class Database:
    def __init__(self, host : str, user : str, password : str, database : str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexao = None

    def conectar(self) -> bool:
        try:
            logger.info("Conectando ao banco PostgreSQL...")
            
            self.conexao = psycopg2.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            self.conexao.autocommit = True
            
            logger.info("Conexão estabelecida com sucesso!")
            return True
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return False

    def desconectar(self) -> None:
        if self.conexao:
            self.conexao.close()
            return True
        
    @time_execution
    def executar_query(self, sql: str) -> tuple[list[str], list[tuple]]:
        with self.conexao.cursor() as cursor:
            cursor.execute(sql)
            if cursor.description:
                colunas = [desc[0] for desc in cursor.description]
                linhas = cursor.fetchall()
                return colunas, linhas
            return [], []
