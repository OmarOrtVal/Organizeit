from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'organizeit_secret_key_2024'  # Clave secreta para sesiones y mensajes flash

# Simulación de base de datos de usuarios (en memoria)
usuarios_registrados = {
    'demo@organizeit.com': {
        'nombre': 'Demo',
        'password': 'demo123',
        'fecha_registro': '2024-01-01'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editar')
def editar():
    return render_template('editar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email_login')
        password = request.form.get('password_login')
        
        # Validar campos vacíos
        if not email or not password:
            return render_template('login.html', 
                                error='⚠️ Por favor completa todos los campos')
        
        # Verificar si el usuario existe
        if email in usuarios_registrados:
            usuario = usuarios_registrados[email]
            if usuario['password'] == password:
                flash(f'✅ ¡Bienvenido/a de nuevo, {usuario["nombre"]}!', 'success')
                return redirect(url_for('index'))
            else:
                return render_template('login.html', 
                                    error='❌ Contraseña incorrecta. Intenta nuevamente.')
        else:
            return render_template('login.html', 
                                error='❌ El correo electrónico no está registrado')
    
    # Método GET: mostrar formulario
    return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('contacto')
        password = request.form.get('contrasena')
        confirm_password = request.form.get('confirmaContraseña')
        
        # Validaciones
        if not all([nombre, apellido, email, password, confirm_password]):
            return render_template('registrar.html', 
                                error='⚠️ Por favor completa todos los campos obligatorios')
        
        if password != confirm_password:
            return render_template('registrar.html', 
                                error='❌ Las contraseñas no coinciden')
        
        if len(password) < 6:
            return render_template('registrar.html', 
                                error='❌ La contraseña debe tener al menos 6 caracteres')
        
        if email in usuarios_registrados:
            return render_template('registrar.html', 
                                error='❌ Este correo electrónico ya está registrado')
        
        # Registrar usuario
        usuarios_registrados[email] = {
            'nombre': nombre,
            'apellido': apellido,
            'password': password,
            'fecha_registro': '2024-01-01'  # En producción usarías datetime.now()
        }
        
        flash(f'✅ ¡Cuenta creada exitosamente! Bienvenido/a, {nombre}', 'success')
        return redirect(url_for('login'))
    
    # Método GET: mostrar formulario
    return render_template('registrar.html')

@app.route('/logout')
def logout():
    flash('👋 Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
