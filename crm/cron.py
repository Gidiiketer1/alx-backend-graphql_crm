from datetime import datetime

def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm the CRM app is alive.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)
