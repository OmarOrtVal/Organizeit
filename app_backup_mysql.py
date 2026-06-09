# app.py - Versión modificada para PyInstaller
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys
from werkzeug.utils import secure_filename

# Obtener la ruta base del ejecutable (para PyInstaller)
def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(get_base_path(), 'templates'),
            static_folder=os.path.join(get_base_path(), 'static'))

app.secret_key = 'organizeit_secret_key_2024'

# Configuración de MySQL (asegúrate de tener MySQL instalado en el sistema)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia si tu MySQL tiene contraseña
app.config['MYSQL_DB'] = 'organizeit'

# Configuración de uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.expanduser("~"), "OrganizeIt_Data", "uploads")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Crear directorios necesarios
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crear_tablas():
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                contraseña VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id_tarea INT AUTO_INCREMENT PRIMARY KEY,
                nombre_tarea VARCHAR(255) NOT NULL,
                categoria ENUM('trabajo', 'hogar', 'personal') NOT NULL,
                prioridad ENUM('alta', 'media', 'baja') NOT NULL,
                fecha_limite DATE,
                usuario_email VARCHAR(100) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completada BOOLEAN DEFAULT FALSE,
                imagen_url TEXT,
                FOREIGN KEY (usuario_email) REFERENCES usuarios(email) 
                    ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        
        try:
            cursor.execute('ALTER TABLE tareas ADD COLUMN imagen_url TEXT')
            print("Columna imagen_url añadida exitosamente")
        except Exception:
            pass  
        
        mysql.connection.commit()
        print("Tablas creadas/actualizadas exitosamente")
    except Exception as e:
        print(f"Error creando tablas: {e}")

@app.route('/')
def index():
    if 'user_email' in session:
        try:
            cursor = mysql.connection.cursor()
            
            cursor.execute('''
                SELECT categoria, COUNT(*) as total 
                FROM tareas 
                WHERE usuario_email = %s AND completada = FALSE
                GROUP BY categoria
            ''', (session['user_email'],))
            
            categorias_count = cursor.fetchall()
            
            cursor.execute('''
                SELECT 
                    id_tarea,
                    nombre_tarea,
                    categoria,
                    prioridad,
                    COALESCE(DATE_FORMAT(fecha_limite, '%%Y-%%m-%%d'), 'Sin fecha') as fecha_limite,
                    DATE_FORMAT(fecha_creacion, '%%Y-%%m-%%d %%H:%%i') as fecha_creacion,
                    completada,
                    imagen_url
                FROM tareas 
                WHERE usuario_email = %s AND prioridad = 'alta' AND completada = FALSE
                ORDER BY fecha_limite ASC
                LIMIT 5
            ''', (session['user_email'],))
            
            tareas_prioritarias = cursor.fetchall()
            
            cursor.execute('''
                SELECT 
                    id_tarea,
                    nombre_tarea,
                    categoria,
                    prioridad,
                    COALESCE(DATE_FORMAT(fecha_limite, '%%Y-%%m-%%d'), 'Sin fecha') as fecha_limite,
                    DATE_FORMAT(fecha_creacion, '%%Y-%%m-%%d') as fecha_creacion,
                    completada,
                    imagen_url
                FROM tareas 
                WHERE usuario_email = %s
                ORDER BY fecha_creacion DESC
                LIMIT 5
            ''', (session['user_email'],))
            
            ultimas_tareas = cursor.fetchall()
            
            return render_template('index.html', 
                                categorias_count=categorias_count,
                                tareas_prioritarias=tareas_prioritarias,
                                ultimas_tareas=ultimas_tareas)
        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'error')
    
    return render_template('index.html')

@app.route('/crear_tarea')
def crear_tarea():
    return render_template('crear_tarea.html')

@app.route('/gestor_tareas')
def gestor_tareas():
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute('''
            SELECT 
                id_tarea,
                nombre_tarea,
                categoria,
                prioridad,
                COALESCE(DATE_FORMAT(fecha_limite, '%%Y-%%m-%%d'), 'Sin fecha') as fecha_limite,
                DATE_FORMAT(fecha_creacion, '%%Y-%%m-%%d %%H:%%i') as fecha_creacion,
                completada,
                imagen_url
            FROM tareas 
            WHERE usuario_email = %s 
            ORDER BY fecha_creacion DESC
        ''', (session['user_email'],))
        
        tareas = cursor.fetchall()
        
        return render_template('gestor_tareas.html', tareas=tareas)
    except Exception as e:
        flash(f'Error al cargar tareas: {str(e)}', 'error')
        return render_template('gestor_tareas.html', tareas=[])

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():    
    try:
        tarea_texto = request.form.get('tarea')
        categoria = request.form.get('categoria')
        prioridad = request.form.get('prioridad')
        fecha_limite = request.form.get('fecha_limite')
        
        imagen_url = None
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo and archivo.filename and allowed_file(archivo.filename):
                timestamp = datetime.now().timestamp()
                filename = secure_filename(f"{session['user_email']}_{timestamp}_{archivo.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                archivo.save(filepath)
                imagen_url = url_for('static', filename=f'uploads/{filename}')
        
        if not all([tarea_texto, categoria, prioridad]):
            flash('Por favor completa todos los campos obligatorios', 'error')
            return redirect(url_for('crear_tarea'))
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO tareas (nombre_tarea, categoria, prioridad, fecha_limite, usuario_email, imagen_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (tarea_texto, categoria, prioridad, 
            fecha_limite if fecha_limite else None, session['user_email'], imagen_url))
        
        mysql.connection.commit()
        flash('Tarea agregada exitosamente', 'success')
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al agregar tarea: {str(e)}', 'error')
    
    return redirect(url_for('gestor_tareas'))

@app.route('/eliminar_tarea/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT imagen_url FROM tareas WHERE id_tarea = %s AND usuario_email = %s', 
                    (tarea_id, session['user_email']))
        resultado = cursor.fetchone()
        
        cursor.execute('''
            DELETE FROM tareas 
            WHERE id_tarea = %s AND usuario_email = %s
        ''', (tarea_id, session['user_email']))
        
        mysql.connection.commit()
        
        if resultado and resultado[0]:
            try:
                imagen_path = resultado[0].replace(url_for('static', filename=''), '')
                imagen_path = os.path.join('static', imagen_path)
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
            except Exception:
                pass  
        
        flash('Tarea eliminada correctamente', 'success')
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar tarea: {str(e)}', 'error')
    
    return redirect(url_for('gestor_tareas'))

@app.route('/limpiar_agenda', methods=['POST'])
def limpiar_agenda():
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT imagen_url FROM tareas WHERE usuario_email = %s', (session['user_email'],))
        imagenes = cursor.fetchall()
        
        cursor.execute('''
            DELETE FROM tareas WHERE usuario_email = %s
        ''', (session['user_email'],))
        
        mysql.connection.commit()
        
        for imagen in imagenes:
            if imagen[0]:
                try:
                    imagen_path = imagen[0].replace(url_for('static', filename=''), '')
                    imagen_path = os.path.join('static', imagen_path)
                    if os.path.exists(imagen_path):
                        os.remove(imagen_path)
                except Exception:
                    pass  
        
        flash('Agenda limpiada completamente', 'success')
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al limpiar agenda: {str(e)}', 'error')
    
    return redirect(url_for('gestor_tareas'))

@app.route('/toggle_tarea/<int:tarea_id>', methods=['POST'])
def toggle_tarea(tarea_id):
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute('''
            SELECT completada FROM tareas 
            WHERE id_tarea = %s AND usuario_email = %s
        ''', (tarea_id, session['user_email']))
        
        tarea = cursor.fetchone()
        
        if tarea:
            nuevo_estado = not tarea[0]
            cursor.execute('''
                UPDATE tareas SET completada = %s 
                WHERE id_tarea = %s AND usuario_email = %s
            ''', (nuevo_estado, tarea_id, session['user_email']))
            
            mysql.connection.commit()
            return jsonify({'success': True, 'completada': nuevo_estado})
        
        return jsonify({'success': False, 'error': 'Tarea no encontrada'})
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email_login')
        password = request.form.get('password_login')
        
        if not email or not password:
            return render_template('login.html', 
                                error='Por favor completa todos los campos')
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                SELECT id_usuario, nombre_usuario, email, contraseña 
                FROM usuarios 
                WHERE email = %s
            ''', (email,))
            
            usuario = cursor.fetchone()
            
            if usuario and check_password_hash(usuario[3], password):
                session['user_id'] = usuario[0]
                session['user_email'] = usuario[2]
                session['user_nombre'] = usuario[1]
                
                flash(f'¡Bienvenido/a de nuevo, {usuario[1]}!', 'success')
                return redirect(url_for('index'))
            else:
                return render_template('login.html', 
                                    error='Credenciales incorrectas')
        except Exception as e:
            return render_template('login.html', 
                                error=f'Error: {str(e)}')
    
    return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('contacto')
        password = request.form.get('contrasena')
        confirm_password = request.form.get('confirmaContraseña')
        
        if not all([nombre, apellido, email, password, confirm_password]):
            return render_template('registrar.html', 
                                error='Completa todos los campos')
        
        if password != confirm_password:
            return render_template('registrar.html', 
                                error='Las contraseñas no coinciden')
        
        if len(password) < 6:
            return render_template('registrar.html', 
                                error='Mínimo 6 caracteres')
        
        try:
            cursor = mysql.connection.cursor()
            
            cursor.execute('SELECT id_usuario FROM usuarios WHERE email = %s', (email,))
            if cursor.fetchone():
                return render_template('registrar.html', 
                                    error='Este correo ya está registrado')
            
            hashed_password = generate_password_hash(password)
            nombre_completo = f"{nombre} {apellido}"
            
            cursor.execute('''
                INSERT INTO usuarios (nombre_usuario, email, contraseña)
                VALUES (%s, %s, %s)
            ''', (nombre_completo, email, hashed_password))
            
            mysql.connection.commit()
            
            flash(f'¡Cuenta creada! Bienvenido/a, {nombre}', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            mysql.connection.rollback()
            return render_template('registrar.html', 
                                error=f'Error: {str(e)}')
    
    return render_template('registrar.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

@app.context_processor
def inject_user():
    return {
        'user_logged_in': 'user_email' in session,
        'user_nombre': session.get('user_nombre', 'Invitado')
    }

if __name__ == '__main__':
    app.run(debug=False)