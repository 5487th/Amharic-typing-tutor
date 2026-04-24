import sqlite3
import warnings
from blinker import signal

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

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

        self.on_user_change_password = signal('user_changed_password')
        self.on_user_changed_username = signal('user_changed_username')

    def create_user(self, username, password = ""):
        self.usermanager_database_cursor.execute(f'SELECT (username) FROM {self.users_table_name} Where username = ?', (username,))
        user_already_exists = self.usermanager_database_cursor.fetchone()

         
        if username and not user_already_exists:
                if password!=None:
                    self.usermanager_database_cursor.execute(f'INSERT INTO {self.users_table_name} VALUES (?, ?)', (username, password))
                    self.usermanager_database.commit()
                    self.on_user_created.send(self, user=User(username, password))
                else:
                    warnings.warn('called create user function with a "None" password, user not created')
        else:
            warnings.warn('called called create user function with a "None" username, user not created')

    def delete_user(self, username_of_user_to_be_deleted):
        if username_of_user_to_be_deleted:
            self.usermanager_database_cursor.execute(f"SELECT * FROM {self.users_table_name} WHERE username = ?",(username_of_user_to_be_deleted,))
            row = self.usermanager_database_cursor.fetchone() 
            deleted_user=None
            if row:
                deleted_user = User(row[0], row[1])

            self.usermanager_database_cursor.execute(f'DELETE FROM {self.users_table_name} WHERE username = ?', (username_of_user_to_be_deleted,))
            self.usermanager_database.commit()

            if deleted_user:
                self.on_user_deleted.send(self,user=deleted_user)
        else:
                warnings.warn('called delete_user function with "None" username, no users were deleted')
    
    def login(self, user_to_login):
        if user_to_login:
            self.current_user = user_to_login
            self.on_user_logged_in.send(self,user=user_to_login)
        else:
            warnings.warn("login function called with no user set, not loged in")

    def logout(self):
        user_to_be_signed_out = self.current_user 
        self.current_user = None
        self.on_user_logged_out.send(self, signed_out_user=user_to_be_signed_out)
        
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

    def change_user_password(self,username, new_password):
        self.usermanager_database_cursor.execute(f"SELECT * FROM {self.user_table_name} WHERE username = ?", (username,))
        row = self.usermanager_database_cursor.fetchone()
        user = User(row[0],row[1])

        if user.username:
            if new_password:
                self.usermanager_database_cursor.execute(F'UPDATE {self.user_table_name} SET password = ? WHERE username = ?',(new_password, username))
                self.usermanager_database.commit()
                self.on_user_change_password.send(self,user=User(user.username, new_password))
            else:
                warnings.warn("called change password with no new password, did not change password")
        else:
            warnings.warn("called change password with non-existant user, did not change password")

    def change_username(self, old_username, new_username):
        if not old_username:
            warnings.warn("called change useraname with empty username, did not change username")
            return
        
        if not new_username:
            warnings.warn("called change user name with empty new username, username not changed")
            return
        
        self.usermanager_database_cursor.execute(f"SELECT username FROM {self.user_table_name} WHERE username = ?", (old_username,))
        old_username_exists = self.usermanager_database_cursor.fetchone()

        self.usermanager_database_cursor.execute(f"SELECT username FROM {self.user_table_name} WHERE username = ?", (new_username,))
        self.new_username_exists = self.usermanager_database_cursor.fetchone()
        
        if old_username_exists:
            if not self.new_username_exists:
                self.usermanager_database_cursor.execute(f"UPDATE {self.user_table_name} SET username = ? where username = ?",(new_username, old_username))
                self.usermanager_database.commit()
                self.on_user_changed_username.send(self, old_username=old_username, new_username=new_username)
            else:
                warnings.warn("called change user name with user name that already exist, did not change user name")
        else:
            warnings.warn("called change user name with non existant user, did not change Username")
