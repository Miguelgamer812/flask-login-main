from .entities.User import User

#Funcionará como paquete por eso lleva el archivo  
class ModelUser():

    @classmethod
    def login(self, conexion, user):
        try:
            cursor = conexion.connection.cursor()
            sql = """SELECT id, usuario, contraseña, fullname FROM user 
                    WHERE usuario = '{}'""".format(user.usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # user = User(row[0], row[1], User.check_password(row[2], user.contraseña), row[3])
                if (row[2] == user.contraseña):
                    user = User(row[0], row[1], row[2], row[3])  
                else:
                    user = User(row[0], row[1], None, row[3])

                return user
            else:   
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, conexion, id):
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT id, usuario, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
