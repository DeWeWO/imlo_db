import mysql.connector
from mysql.connector import Error


# MySQL ulanish sozlamalari
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'imlo_db'
}

def save_to_word(word, position, syllable, cyrillic):
    try:
        # MySQL ulanishini ochish
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Tranzaksiyani boshlash
        connection.start_transaction()

        # Ma'lumotlarni word jadvaliga yozish
        insert_word_query = """
        INSERT IGNORE INTO word (word, position, syllable, cyrillic)
        VALUES (%s, %s, %s, %s)
        """
        word_data = (word, position, syllable, cyrillic)
        cursor.execute(insert_word_query, word_data)

        # Tranzaksiyani tasdiqlash
        connection.commit()
        return True
    except Error as e:
        print(f"save_to_word da xatolik: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
def save_category(info):
    try:
        # MySQL ulanishini ochish
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Tranzaksiyani boshlash
        connection.start_transaction()

        # Ma'lumotlarni category jadvaliga yozish
        insert_category_query = """
        INSERT IGNORE INTO category (info)
        VALUES (%s)
        """
        cursor.execute(insert_category_query, (info,))

        # Tranzaksiyani tasdiqlash
        connection.commit()
        return True
    except Error as e:
        print(f"save_category da xatolik: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def save_to_wordInfo(word_id, category_id, changed):
    try:
        # MySQL ulanishini ochish
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Tranzaksiyani boshlash
        connection.start_transaction()

        # Ma'lumotlarni word_info jadvaliga yozish
        insert_word_info_query = """
        INSERT IGNORE INTO word_info (word_id, category_id, changed)
        VALUES (%s, %s, %s)
        """

        # Agar changed ro'yxat bo'lsa, har bir elementni alohida yozuv sifatida saqlash
        if isinstance(changed, list):
            for item in changed:
                if item:  # Bo'sh elementlarni o'tkazib yuborish
                    word_info_data = (word_id, category_id, item)
                    cursor.execute(insert_word_info_query, word_info_data)
        else:
            # Agar changed ro'yxat bo'lmasa, to'g'ridan-to'g'ri yozish
            if changed:  # Bo'sh bo'lmasa
                word_info_data = (word_id, category_id, changed)
                cursor.execute(insert_word_info_query, word_info_data)

        # Tranzaksiyani tasdiqlash
        connection.commit()
        return True
    except Error as e:
        print(f"save_to_wordInfo da xatolik: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_word_id(word):
    try:
        # MySQL ulanishini ochish
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # So'z ID sini olish
        select_word_query = """
        SELECT id FROM word WHERE word = %s
        """
        cursor.execute(select_word_query, (word,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None
    except Error as e:
        print(f"get_word_id da xatolik: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_category_id(info):
    try:
        # MySQL ulanishini ochish
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Kategoriya ID sini olish
        select_category_query = """
        SELECT id FROM category WHERE info = %s
        """
        cursor.execute(select_category_query, (info,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None
    except Error as e:
        print(f"get_category_id da xatolik: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





# def get_word(word_id):
#     query = "SELECT word FROM word WHERE id = %s"
#     try:
#         with get_db_cursor() as (_, cur):
#             cur.execute(query, (word_id,))
#             result = cur.fetchone()
#             return result[0] if result else None
#     except Error as e:
#         print(f"get_word da xatolik: {e}")
#         return None

# def get_category(category_id):
#     query = "SELECT info FROM category WHERE id = %s"
#     try:
#         with get_db_cursor() as (_, cur):
#             cur.execute(query, (category_id,))
#             result = cur.fetchone()
#             return result[0] if result else None
#     except Error as e:
#         print(f"get_category da xatolik: {e}")
#         return None

# def get_word_info(word_info_id):
#     query = """
#         SELECT wi.word_id, wi.category_id, wi.changed, w.word, c.info
#         FROM word_info wi
#         JOIN word w ON wi.word_id = w.id
#         JOIN category c ON wi.category_id = c.id
#         WHERE wi.id = %s
#     """
#     try:
#         with get_db_cursor() as (_, cur):
#             cur.execute(query, (word_info_id,))
#             result = cur.fetchone()
#             if result:
#                 return {
#                     "word_id": result[0],
#                     "category_id": result[1],
#                     "changed": result[2],
#                     "word": result[3],
#                     "category": result[4]
#                 }
#             return None
#     except Error as e:
#         print(f"get_word_info da xatolik: {e}")
#         return None
