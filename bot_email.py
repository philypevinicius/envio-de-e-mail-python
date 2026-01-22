import smtplib
import re
from email.mime.text import MIMEText

def enviar_email(mensagem, EMAIL_ORIGEM, SENHA_EMAIL, EMAIL_DESTINO):
    blocos = re.split(r'\n\s*\n', mensagem.strip())
    corpo_movs = ''

    for bloco in blocos:
        if not re.search(r'Tombamento\s*:\s*\S+', bloco, re.IGNORECASE):
            continue 

        tombamento = re.search(r'Tombamento\s*:\s*(.+)', bloco, re.IGNORECASE)
        tipo = re.search(r'Tipo do Dispositivo\s*:\s*(.+)', bloco, re.IGNORECASE)
        origem = re.search(r'Local de Origem\s*:\s*(.+)', bloco, re.IGNORECASE)
        destino = re.search(r'Local de Destino\s*:\s*(.+)', bloco, re.IGNORECASE)
        motivo = re.search(r'Motivo\s*:\s*(.+)', bloco, re.IGNORECASE)

        corpo_movs += (
            f"Tombamento: {tombamento.group(1) if tombamento else ''}\n"
            f"Tipo do Dispositivo: {tipo.group(1) if tipo else ''}\n"
            f"Local de Origem: {origem.group(1) if origem else ''}\n"
            f"Local de Destino: {destino.group(1) if destino else ''}\n"
            f"Motivo: {motivo.group(1) if motivo else ''}\n"
            "----------------------------------------\n\n"
        )

    if not corpo_movs:
        return

    # CORPO DO E-MAIL 
    corpo_total = (
        "Prezados,\n\n"
        "Gostaria de informar sobre a seguinte movimentação de bens:\n\n"
        f"{corpo_movs}"
    )

    msg = MIMEText(corpo_total)
    msg['Subject'] = 'MOVIMENTAÇÃO DE BENS'
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = EMAIL_DESTINO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ORIGEM, SENHA_EMAIL)
        server.sendmail(EMAIL_ORIGEM, EMAIL_DESTINO, msg.as_string())
