import redis
import sqlite3
import logging
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Database:
    """Clase para manejar la conexión a SQLite y registrar consultas."""
    def __init__(self, db_name="products.db"):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def insert_product(self, name):
        """Inserta un nuevo producto en la base de datos."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
            conn.commit()

    def get_product(self, product_id, manual=False):
        """Obtiene un producto de la base de datos y registra acceso si es manual."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()

            if manual:
                cursor.execute("INSERT INTO logs (action) VALUES (?)", 
                               (f"Consulta manual en SQLite a producto ID {product_id}",))
                conn.commit()

            return result[0] if result else "Producto no encontrado"

    def log_manual_queries(self):
        """Muestra las últimas consultas manuales registradas."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10")
            logs = cursor.fetchall()
            for log in logs:
                logging.info(f" {log[1]} - {log[2]}")

class CacheAside:
    """Implementación del patrón Cache-Aside con Redis y SQLite."""
    def __init__(self, db, host="localhost", port=6379, db_index=0, ttl=30):
        self.db = db
        self.ttl = ttl

        try:
            self.cache = redis.StrictRedis(host=host, port=port, db=db_index, decode_responses=True)
            self.cache.ping()
            logging.info("Conectado a Redis correctamente.")
        except redis.ConnectionError:
            logging.error("No se pudo conectar a Redis. Asegúrate de que Redis esté en ejecución.")
            self.cache = None

    def get_product(self, product_id):
        """Busca un producto en caché, si no está, lo obtiene de la BD y lo almacena."""
        if self.cache:
            product = self.cache.get(product_id)
            if product:
                logging.info(f"Cache HIT: Producto '{product}' encontrado en Redis.")
                return product

        logging.info(" Cache MISS. Consultando base de datos...")
        product = self.db.get_product(product_id)

        if self.cache:
            self.cache.setex(product_id, self.ttl, product)
            logging.info(f"Producto '{product}' almacenado en caché por {self.ttl} segundos.")

        return product

if __name__ == "__main__":
    db = Database()
    productos = [
        "Laptop Lenovo", "Mouse Logitech", "Teclado mecánico", "Monitor Samsung", "Silla gamer",
        "Escritorio de madera", "Auriculares Sony", "Disco SSD 1TB", "Procesador Ryzen 7", "Tarjeta gráfica RTX 3060"
    ]

    if db.get_product(1) == "Producto no encontrado":
        for producto in productos:
            db.insert_product(producto)

    cache_aside = CacheAside(db, ttl=20)

    while True:
        print("\nMenú:")
        print("1. Consultar producto (usando caché)")
        print("2. Consultar producto manualmente en la BD")
        print("3. Mostrar últimos logs")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            product_id = input("Ingresa el ID del producto: ")
            print(f"Resultado: {cache_aside.get_product(product_id)}")

        elif opcion == "2":
            product_id = input("Ingresa el ID del producto: ")
            print(f"Resultado: {db.get_product(product_id, manual=True)}")
        
        elif opcion == "3":
            db.log_manual_queries()

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")
