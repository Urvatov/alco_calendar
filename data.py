from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash

from sqlite3 import Error as error


class Data:
    def __init__(self, database):
        self.db = database
        self.cursor = database.cursor()
    
    def add_drink(self, title, price, alcohol, volume, user_id):
        try:
            self.cursor.execute(f"INSERT INTO drink VALUES(NULL, ?, ?, ?, ?, ?)", (title, price, alcohol, volume, user_id))
            self.db.commit()
        except error:
            print("ОШИБКА! " + str(error))
    
    def get_drinks(self, user_id):
        try:
            self.cursor.execute(f"SELECT id, title, alcohol, volume, price FROM drink WHERE user_id = {user_id} ORDER BY title")
            drinks = self.cursor.fetchall()

            return drinks
        except error:
            print("ОШИБКА! " + str(error))
    
    def delete_drink(self, drink_id):
        try:
            self.cursor.execute(f"DELETE FROM drink WHERE id = {drink_id}")
            self.db.commit()

            return redirect(url_for('drinks'))
        
        except error:
            print("ОШИБКА! " + str(error))
    
    

    def add_user(self, nickname, hash):
            try:
                self.cursor.execute(f"SELECT COUNT() as 'count' FROM user WHERE nickname LIKE '{nickname}' ")
                res = self.cursor.fetchone()
                if res['count'] > 0:
                    print("ПОЛЬЗОВАТЕЛЬ С ТАКИМ ИМЕНЕМ УЖЕ СУЩЕСТВУЕТ")

                self.cursor.execute("INSERT INTO user VALUES(NULL, ?, ?)", (nickname, hash))
                self.db.commit()

            except error:
                print("ОШИБКА! " + str(error))
    
    def get_user_by_nickname(self, nickname):
        try:
            self.cursor.execute(f"SELECT * FROM user WHERE nickname = '{nickname}' LIMIT 1")
            res = self.cursor.fetchone()
            
            return res
        except error:
                print("ОШИБКА! " + str(error))

    def get_user(self, user_id):
        try:
            self.cursor.execute(f"SELECT * FROM user WHERE id = {user_id} LIMIT 1")
            user = self.cursor.fetchone()
            return user
        
        except error:
                print("ОШИБКА! " + str(error))
    
    def update(self, user_id, type, new_name, new_password):
        try:
            if type == "name":
                self.cursor.execute(f"UPDATE user SET nickname = '{new_name}' WHERE id = {user_id} ")

            if type == "password":
                self.cursor.execute(f"UPDATE user SET psw = '{new_password}' WHERE id = {user_id} ")  
                 
            self.db.commit()
        
        except error:
                print("ОШИБКА! " + str(error))
         
    
    def get_statistic(self, user_id):
        try:
            self.cursor.execute(f"SELECT SUM(money_spent), SUM(volume) FROM events WHERE user_id = {user_id}")
            stats = self.cursor.fetchone()
            return stats
        
        except error:
                print("ОШИБКА! " + str(error))
     

    def add_event(self, user_id, drink_id, drink_title, title, event_date, volume, money, description):
        try:
            self.cursor.execute(f"INSERT INTO events VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, drink_id, drink_title, title, event_date, volume, money, description))
            self.db.commit()
        except error:
            print("ОШИБКА! " + str(error))

    def get_events(self, user_id):
        try:
            self.cursor.execute(f"SELECT title, drink_title, event_date, volume, money_spent, descript FROM events WHERE user_id = {user_id} ORDER BY event_date DESC")
            events = self.cursor.fetchall()

            return events
        
        except error:
                print("ОШИБКА! " + str(error))
         
    

