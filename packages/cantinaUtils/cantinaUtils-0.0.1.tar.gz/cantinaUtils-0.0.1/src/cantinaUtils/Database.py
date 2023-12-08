import pymysql


class DataBase:
    def __init__(self, user, password, host, port, database=None):
        self.database = database
        self.port = port
        self.host = host
        self.password = password
        self.user = user
        self.cursor = None
        self.connector = None

    def connection(self):
        self.connector = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                                         database=self.database)  # Connection à la base de donnée.
        self.cursor = self.connector.cursor()  # Création du curseur.

    def exec(self, body, args):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute(body, args)  # Execution de la query.
        self.cursor.close()  # Fermeture du curseur.
        self.connector.close()  # Fermeture de la connexion.
