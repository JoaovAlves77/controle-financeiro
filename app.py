from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from datetime import date

from models import db
from models import Movimentacao

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///financeiro.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return redirect(
        url_for("dashboard")
    )


@app.route("/dashboard")
def dashboard():

    movimentacoes = \
        Movimentacao.query.order_by(
            Movimentacao.id.desc()
        ).all()

    receitas = Movimentacao.query.filter_by(
        tipo="Receita"
    ).all()

    despesas = Movimentacao.query.filter_by(
        tipo="Despesa"
    ).all()

    total_receitas = sum(
        r.valor for r in receitas
    )

    total_despesas = sum(
        d.valor for d in despesas
    )

    saldo = (
        total_receitas -
        total_despesas
    )

    return render_template(
        "dashboard.html",
        saldo=saldo,
        receitas=total_receitas,
        despesas=total_despesas,
        movimentacoes=movimentacoes
    )


@app.route(
    "/nova",
    methods=["GET", "POST"]
)
def nova():

    if request.method == "POST":

        mov = Movimentacao(
            descricao=request.form["descricao"],
            valor=float(
                request.form["valor"]
            ),
            tipo=request.form["tipo"],
            categoria=request.form["categoria"],
            data=str(date.today())
        )

        db.session.add(mov)
        db.session.commit()

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "movimentacao.html"
    )


if __name__ == "__main__":
    app.run(debug=True)