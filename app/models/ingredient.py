import sqlite3
from datetime import datetime

DATABASE_PATH = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class IngredientModel:
    
    @staticmethod
    def create(name, quantity, unit, category, expiry_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO ingredients (name, quantity, unit, category, expiry_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''',
            (name, quantity, unit, category, expiry_date)
        )
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def get_all():
        conn = get_db_connection()
        ingredients = conn.execute('SELECT * FROM ingredients ORDER BY expiry_date ASC').fetchall()
        conn.close()
        return [dict(ix) for ix in ingredients]

    @staticmethod
    def get_by_id(ingredient_id):
        conn = get_db_connection()
        ingredient = conn.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,)).fetchone()
        conn.close()
        return dict(ingredient) if ingredient else None

    @staticmethod
    def update(ingredient_id, name, quantity, unit, category, expiry_date):
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE ingredients
            SET name = ?, quantity = ?, unit = ?, category = ?, expiry_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (name, quantity, unit, category, expiry_date, ingredient_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(ingredient_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM ingredients WHERE id = ?', (ingredient_id,))
        conn.commit()
        conn.close()
