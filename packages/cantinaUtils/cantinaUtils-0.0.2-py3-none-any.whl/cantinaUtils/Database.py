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

    def exec(self, body, args):  # Fonction permettant d'inserer des données dans la base de donnée
        self.connection()  # Connection avec la base de données.
        self.cursor.execute(body, args)  # Execution de la query.
        self.cursor.close()  # Fermeture du curseur.
        self.connector.close()  # Fermeture de la connexion.

    def select(self, body, args, number_of_data=None):  # Fonction permettant d'obtenir des données de la base de donnée
        self.connection()  # Connection avec la base de données.
        self.cursor.execute(body, args)  # Execution de la query.
        self.cursor.close()  # Fermeture du curseur.
        self.connector.close()  # Fermeture de la connexion.

        if not number_of_data:  # Si aucune valeur n'est défini, alors on prends toute les valeurs
            data = self.cursor.fetchall()
        elif number_of_data == 1:  # Si la variable est sur 1, alors on prends qu'une seul valeur
            data = self.cursor.fetchone()
        else:  # Si la variable est autre chose que 1 ou undefined, alors on renvoie le nombre de valeurs demandé.
            data = self.cursor.fetchmany(number_of_data)

        return data
