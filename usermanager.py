import sqlite3
import warnings
from blinker import signal

class UserManager:
    def __init__(self):
        self.current_user = None
        
        self.usermanager_database_name = "usermanager"

        self.usermanager_database = sqlite3.connect(f'{self.usermanager_database_name}.db')
        self.usermanager_database_cursor = self.usermanager_database.cursor()
        
        self.users_table_name = 'users'
        self.usermanager_database_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.users_table_name}
                                            (username TEXT PRIMARY KEY, password TEXT)''')
        
        self.on_user_created = signal('user_created')
        self.on_user_deleted = signal('user_deleted')
        self.on_user_logged_in = signal('user_logged_in')
        self.on_user_logged_out = signal('user_logged_out')

    def create_user(self, username, password = ""):
        self.usermanager_database_cursor.execute(f'SELECT (username) FROM {self.users_table_name} Where username = ?', (username,))
        user_already_exists = self.usermanager_database_cursor.fetchone()

         
        if username and not user_already_exists:
                if password:
                    self.usermanager_database_cursor.execute(f'INSERT INTO {self.users_table_name} VALUES (?, ?)', (username, password))
                    self.usermanager_database.commit()
                    self.on_user_created.send(self,User(username, password))
                else:
                    warnings.warn('called create user function with a "None" password, user not created')
        else:
            warnings.warn('called called create user function with a "None" username, user not created')

    def delete_user(self, user:User):
        if user:
            if user.username:
                self.usermanager_database_cursor.execute(f'DELETE FROM {self.users_table_name} WHERE username = ?', (user.username,))
                self.usermanager_database.commit()
                self.on_user_deleted.send(self,user)
            else:
                 warnings.warn('called delete_user function with "None" username, no users were deleted')
        else:
           warnings.warn('called delete_user function with "None" user, no users were deleted')
    
    def login(self, user):
        if user:
            self.current_user = user
            self.on_user_logged_in.send(self,user)
        else:
            warnings.warn("login function called with no user set, not loged in")

    def logout(self):
        old_user = self.current_user 
        self.current_user = None
        self.on_user_logged_out.send(self,old_user)
        
    def get_user(self, username):
        self.usermanager_database_cursor.execute(f'SELECT * FROM {self.users_table_name} WHERE username = ?',(username,))
        row = self.usermanager_database_cursor.fetchone()
        if row:
            user = User(row[0],row[1])
            return user
        else:
            return None
    
    def get_all_users(self):
        self.usermanager_database_cursor.execute(f"SELECT * FROM {self.users_table_name}")
        users_tuple_list = self.usermanager_database_cursor.fetchall()
        users_list = []
        for user_tuple in users_tuple_list:
            user = User(user_tuple[0], user_tuple[1])
            users_list.append(user)
        return users_list

    
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password