import requests
import json
import time
import subprocess 


BASE_URL = "https://kd674s-8082.csb.app"
GROUP = "my_consumer_group"
INSTANCE = "my_consumer"

headers_json = {"Content-Type": "application/vnd.kafka.v2+json"}
headers_accept = {"Accept": "application/vnd.kafka.json.v2+json"}

# 1. Criar consumer
resp = requests.post(
    f"{BASE_URL}/consumers/{GROUP}",
    headers=headers_json,
    data=json.dumps({
        "name": INSTANCE,
        "format": "json",
        "auto.offset.reset": "earliest"
    })
)
resp.raise_for_status()
print("Consumer criado:", resp.json())

# 2. Assinar tópico
resp = requests.post(
    f"{BASE_URL}/consumers/{GROUP}/instances/{INSTANCE}/subscription",
    headers=headers_json,
    data=json.dumps({"topics": ["github_webhooks"]})
)
resp.raise_for_status()
print("Inscrito no tópico github_webhooks")

# 3. Polling de mensagens
while True:
    resp = requests.get(
        f"{BASE_URL}/consumers/{GROUP}/instances/{INSTANCE}/records",
        headers=headers_accept
    )
    resp.raise_for_status()
    msgs = resp.json()
    if msgs:
        for m in msgs:
            print("Mensagem recebida:", m)
            value = m.get("value", {})
            event = value.get("event")
            ref = value.get("payload", {}).get("ref")

            if event == "push" and ref in ["refs/heads/main", "refs/heads/develop"]:
                print(f"Evento push detectado em {ref}, chamando script...")
                # Executa script bash
                subprocess.run(["./cicd.sh"], check=True)




    time.sleep(60)
