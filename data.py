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
    
    def get_drink_by_id(self, drink_id):
        try:
            self.cursor.execute(f"SELECT title FROM drink WHERE id = {drink_id}")

        except error:
            print("ОШИБКА! " + str(error))
    
    def get_fauvorite_drink(self, user_id):
        try:
            self.cursor.execute(f"""SELECT drink_title
                                    FROM events_drink
                                    WHERE user_id = {user_id}
                                    GROUP BY drink_title
                                    ORDER BY COUNT(*) DESC
                                    LIMIT 1;""")
            
            fauvorite_drink = self.cursor.fetchone()

            return fauvorite_drink
             
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
    
    def update_name(self, user_id, new_name):
        try:
            self.cursor.execute(f"UPDATE user SET nickname = '{new_name}' WHERE id = {user_id} ")
            self.db.commit()
        
        except error:
                print("ОШИБКА! " + str(error))
    
    def update_password(self, user_id, new_password):
        try:
            psw = generate_password_hash(new_password)
            self.cursor.execute(f"UPDATE user SET psw = '{psw}' WHERE id = {user_id} ")    
            self.db.commit()
        
        except error:
                print("ОШИБКА! " + str(error))
    
    def get_statistic(self, user_id):
        try:
            self.cursor.execute(f"SELECT SUM(price), SUM(volume) FROM events_drink WHERE user_id = {user_id}")
            stats = self.cursor.fetchone()
            return stats
        
        except error:
                print("ОШИБКА! " + str(error))
     

    def add_event(self, user_id, title, event_date, place, description):
        try:
            self.cursor.execute(f"INSERT INTO events VALUES(NULL, ?, ?, ?, ?, ?)", (user_id, title, event_date, place, description))
            self.db.commit()
        except error:
            print("ОШИБКА! " + str(error))
        
    
    def add_drink_in_event(self, user_id, event_id, drink, volume, price):
        try:
            self.cursor.execute(f"SELECT id, alcohol FROM drink WHERE title = '{drink}' AND user_id = {user_id}")
            drink_id = self.cursor.fetchone()
            
            self.cursor.execute(f"INSERT INTO events_drink VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (user_id, event_id, drink_id[0], drink, drink_id[1], volume, price))
            self.db.commit()
        except error:
            print("ОШИБКА! " + str(error))
    
    def get_drinks_in_event(self, event_id):
        try:
            self.cursor.execute(f"SELECT drink_id, drink_title, drink_alcohol, volume, price FROM events_drink WHERE event_id = {event_id}")
            drinks_in_event = self.cursor.fetchall()
            return drinks_in_event
        except error:
            print("ОШИБКА! " + str(error))
        
    def get_sum_of_volume(self, event_id):
        try:
            self.cursor.execute(f"SELECT SUM(volume) FROM events_drink WHERE event_id = {event_id}")
            volume_sum = self.cursor.fetchone()
            return volume_sum
        except error:
            print("ОШИБКА! " + str(error))

    def get_sum_of_price(self, event_id):
        try:
            self.cursor.execute(f"SELECT SUM(price) FROM events_drink WHERE event_id = {event_id}")
            price_sum = self.cursor.fetchone()
            return price_sum
        except error:
            print("ОШИБКА! " + str(error))

    def get_events(self, user_id):
        try:
            self.cursor.execute(f"SELECT id, title, event_date, place, descript FROM events WHERE user_id = {user_id} ORDER BY event_date DESC")
            events = self.cursor.fetchall()
            return events
        
        except error:
                print("ОШИБКА! " + str(error))
    
    def get_description(self, event_id):
        try:
            self.cursor.execute(f"SELECT descript FROM events WHERE id = {event_id}")
            description = self.cursor.fetchone()
            return description
        except error:
                print("ОШИБКА! " + str(error))
    
    def get_event_info(self, event_id):
        try:
            self.cursor.execute(f"SELECT event_date, title, place, descript FROM events WHERE id = {event_id}")
            event_info = self.cursor.fetchone()
            
            return event_info
        except error:
                print("ОШИБКА!" + str(error))

    def delete_event(self, event_id):
        try:
            self.cursor.execute(f"DELETE FROM events WHERE id = {event_id}")
            self.db.commit()

            return redirect(url_for('history'))
        
        except error:
            print("ОШИБКА! " + str(error))

    
         
    

