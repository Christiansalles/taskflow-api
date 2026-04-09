import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_notification():
    # Leitura das variáveis de ambiente — nunca hardcoded
    email_from = os.environ.get("EMAIL_FROM")
    email_to = os.environ.get("EMAIL_TO")
    email_password = os.environ.get("EMAIL_PASSWORD")
    pipeline_status = os.environ.get("PIPELINE_STATUS", "unknown")
    pipeline_url = os.environ.get("PIPELINE_RUN_URL", "N/A")

    # Valida variáveis obrigatórias
    if not all([email_from, email_to, email_password]):
        print("⚠️  Variáveis de e-mail não configuradas. Notificação ignorada.")
        sys.exit(0)

    # Define assunto baseado no status
    if pipeline_status == "success":
        subject = "✅ TaskFlow API — Pipeline com Sucesso"
    else:
        subject = "❌ TaskFlow API — Pipeline com Falha"

    # Corpo do e-mail
    now = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
    body = f"""
Notificação automática — TaskFlow API

Status:    {pipeline_status.upper()}
Projeto:   TaskFlow API
Data/Hora: {now}
Execução:  {pipeline_url}

--
Mensagem gerada automaticamente pelo pipeline CI/CD via GitHub Actions.
    """.strip()

    # Monta o e-mail
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Envia via SMTP SSL (Gmail porta 465)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, msg.as_string())
        print(f"✅ Notificação enviada para {email_to}")
    except Exception as e:
        print(f"⚠️  Falha ao enviar e-mail: {e}")
        sys.exit(0)  # Não quebra o pipeline


if __name__ == "__main__":
    send_notification()
