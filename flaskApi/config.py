import psycopg2
def create_connection():
    try:
        connection = psycopg2.connect(host="localhost", port="5432",  dbname="bears", user="postgres", password="0622")
        return connection
    except psycopg2.Error as e:
        print(f"Error to connect with PostgreSQL: {e}")
        return None