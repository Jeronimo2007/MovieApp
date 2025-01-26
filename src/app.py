from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import get_supabase_client, config


from models.ModelUser import ModelUser


from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()

supabase_client = get_supabase_client()


login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(supabase_client, id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(supabase_client, user)
        if logged_user is not None:
            if logged_user.password:  # Contraseña válida
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
                return render_template('auth/login.html')
        else:
            flash('User not found')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            user = [
                request.form['username'],
                request.form['password'],
                request.form['fullname']
            ]
            ModelUser.register(supabase_client, user)
            return redirect(url_for('login'))
        except Exception as e:
            return f"Error al registrar usuario: {e}", 500
    else:
        return render_template('auth/register.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1> ESTA ES UNA VISTA PROTEGIDA SOLO PARA USUARIOS</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return '<h1>Pagina no encontrada</h1>', 404


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/filter', methods=['POST'])
def filter_movies():
    data = request.json
    selected_genres = data.get('genres', [])  

    if not selected_genres:
        return jsonify({'error': 'No genres selected'}), 400

    # Filtrar películas
    try:
        recommendations = ModelUser.filter_by_genres(selected_genres)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.debug = True
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()