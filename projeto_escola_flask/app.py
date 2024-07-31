from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="fnlj1984",
        database="escola"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/professores', methods=['GET', 'POST'])
def professores():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute("INSERT INTO professores (nome) VALUES (%s)", (nome,))
        conn.commit()
        return redirect(url_for('professores'))
    
    cursor.execute("SELECT * FROM professores")
    professores = cursor.fetchall()
    conn.close()
    return render_template('professores.html', professores=professores)

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nome = request.form['nome']
        nota = float(request.form['nota'])
        frequencia = float(request.form['frequencia'])
        professor_id = int(request.form['professor_id'])
        cursor.execute("INSERT INTO alunos (nome, nota, frequencia, professor_id) VALUES (%s, %s, %s, %s)", 
                       (nome, nota, frequencia, professor_id))
        conn.commit()
        return redirect(url_for('alunos'))
    
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    cursor.execute("SELECT * FROM professores")
    professores = cursor.fetchall()
    conn.close()
    return render_template('alunos.html', alunos=alunos, professores=professores)

@app.route('/delete_professor/<int:id>')
def delete_professor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professores WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('professores'))

@app.route('/delete_aluno/<int:id>')
def delete_aluno(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('alunos'))

if __name__ == '__main__':
    app.run(debug=True)
