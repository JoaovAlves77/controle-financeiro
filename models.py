from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(
        db.String(100),
        nullable=False
    )

    valor = db.Column(
        db.Float,
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    categoria = db.Column(
        db.String(50),
        nullable=False
    )

    data = db.Column(
        db.String(20),
        nullable=False
    )