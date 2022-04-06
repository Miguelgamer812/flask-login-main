from werkzeug.security import check_password_hash #, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):
   #Clase constructora con init
    def __init__(self, id, usuario, contraseña, fullname="") -> None:
        self.id = id
        self.usuario = usuario
        self.contraseña = contraseña
        self.fullname = fullname

    @classmethod #@el decorador nos evita intanciar la clase            #password desde BD  y password en texto plano
    def check_password(self, hashed_contraseña, contraseña):
        return check_password_hash(hashed_contraseña, contraseña)

#print(generate_password_hash("soytdea"))
# Para generar una nueva clave de tipo hash  python .\src\models\entities\User.py