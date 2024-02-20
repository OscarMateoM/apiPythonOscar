from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'productos.db'

# Crea la tabla 'productos' si no existe
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Obtén la conexión a la base de datos
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint para obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        conn.close()
        return jsonify([dict(producto) for producto in productos])

# Endpoint para obtener un producto por ID
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
    producto = cursor.fetchone()
    conn.close()

    if producto is not None:
        return jsonify(dict(producto))

# Endpoint para agregar un nuevo producto
@app.route('/productos', methods=['POST'])
def agregar_producto():
    nuevo_producto = request.json

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)', (nuevo_producto['nombre'], nuevo_producto['precio'], nuevo_producto['categoria']))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto agregado correctamente"})


# Endpoint para actualizar un producto por ID
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    conn = get_db()
    cursor = conn.cursor()
    producto = cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()

    if producto is not None:
        datos_actualizados = request.json
        cursor.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?', (datos_actualizados['nombre'], datos_actualizados['precio'], producto_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto actualizado correctamente"})

# Endpoint para eliminar un producto por ID
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto eliminado correctamente"})

@app.route("/")
def hello_world():
    return "<p>Hola, Mundo!</p>"

if __name__ == '__main__':
    create_table()
    app.run(debug=True)