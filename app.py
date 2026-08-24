# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)

    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        return None
    
app = Flask(__name__)
app.secret_key = "chave-secreta"





@app.route("/")
def index():

    conexao = conectar()

    if conexao is None:
        return """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <title>Banco indisponível</title>

            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                rel="stylesheet"
            >
        </head>

        <body class="bg-light">

            <div class="container">
                <div
                    class="d-flex justify-content-center align-items-center"
                    style="min-height: 100vh;"
                >

                    <div
                        class="card shadow border-0 text-center"
                        style="max-width: 500px; width: 100%;"
                    >

                        <div class="card-body p-5">

                            <div class="mb-4">
                                <span style="font-size: 60px;">
                                    ⚠️
                                </span>
                            </div>

                            <h2 class="fw-bold">
                                Banco de dados indisponível
                            </h2>

                            <p class="text-muted mt-3">
                                Não foi possível estabelecer conexão
                                com o banco de dados.
                            </p>

                            <p class="text-muted">
                                Verifique se o servidor MySQL está
                                funcionando e tente novamente.
                            </p>

                            <a
                                href="/"
                                class="btn btn-primary mt-3 px-4"
                            >
                                Tentar novamente
                            </a>

                        </div>

                    </div>

                </div>
            </div>

        </body>
        </html>
        """

    busca = request.args.get("busca", "")
    status = request.args.get("status", "")

    cursor = conexao.cursor(dictionary=True)

    query = "SELECT * FROM tarefas WHERE 1=1"
    params = []

    if busca:
        query += " AND titulo LIKE %s"
        params.append(f"%{busca}%")

    if status:
        query += " AND status = %s"
        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    tarefas = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) AS total FROM tarefas"
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS total FROM tarefas WHERE status = 'pendente'"
    )
    pendentes = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS total FROM tarefas WHERE status = 'concluida'"
    )
    concluidas = cursor.fetchone()["total"]

    cursor.close()
    conexao.close()

    return render_template(
        "index.html",
        tarefas=tarefas,
        total=total,
        pendentes=pendentes,
        concluidas=concluidas,
        busca=busca,
        status=status
    )


@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        prioridade = request.form["prioridade"]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO tarefas
            (titulo, descricao, prioridade)
            VALUES (%s, %s, %s)
            """,
            (titulo, descricao, prioridade)
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Tarefa criada com sucesso!", "success")

        return redirect(url_for("index"))

    return render_template("criar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        prioridade = request.form["prioridade"]
        status = request.form["status"]

        cursor.execute(
            """
            UPDATE tarefas
            SET titulo=%s,
                descricao=%s,
                prioridade=%s,
                status=%s
            WHERE id=%s
            """,
            (titulo, descricao, prioridade, status, id)
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Tarefa atualizada com sucesso!", "success")

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM tarefas WHERE id = %s",
        (id,)
    )

    tarefa = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("editar.html", tarefa=tarefa)


@app.route("/concluir/<int:id>")
def concluir(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE tarefas
        SET status = 'concluida'
        WHERE id = %s
        """,
        (id,)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    flash("Tarefa concluída!", "success")

    return redirect(url_for("index"))


@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id = %s",
        (id,)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    flash("Tarefa excluída.", "danger")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True)
