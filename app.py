from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/robo_monitoramento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela no banco de dados
class RoboLog(db.Model):
    __tablename__ = 'robo001'  # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True)
    DH_INSERT = db.Column(db.DateTime)  # Data/hora da execução
    NOME_ROBO = db.Column(db.String(100))  # Nome do robô
    USUARIO = db.Column(db.String(50))
    LOG = db.Column(db.Text)
    VIDA = db.Column(db.String(50))
    COR = db.Column(db.String(50))
    NO_HOST = db.Column(db.String(50))


@app.route('/dashboard')
def dashboard():
    # Filtrar apenas os logs do robô "redes_sociais"
    logs = RoboLog.query.filter_by(NOME_ROBO="redes_sociais").all()

    # Processar os dados
    relatorios_sucesso = sum(1 for log in logs if "sucesso" in log.LOG.lower())
    relatorios_erro = sum(1 for log in logs if "erro" in log.LOG.lower())
    ultima_execucao = max(log.DH_INSERT for log in logs) if logs else None
    total_execucoes = len(logs)
    dias_capturados = len(set(log.DH_INSERT.date() for log in logs))

    # Dados para exibir no frontend
    data = {
        "relatorios_sucesso": relatorios_sucesso,
        "relatorios_erro": relatorios_erro,
        "ultima_execucao": ultima_execucao.strftime("%H:%M (%d/%m/%Y)") if ultima_execucao else "N/A",
        "total_execucoes": total_execucoes,
        "dias_capturados": dias_capturados,
        "logs": [{"data": log.DH_INSERT.strftime("%d/%m/%Y %H:%M"), "mensagem": log.LOG} for log in logs]
    }
    return render_template('dashboard.html', data=data)

@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

