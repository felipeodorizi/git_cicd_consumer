#!/bin/bash

echo "################################################################"
echo "#######   START of the bash script   (git_pull_ecflow).  #######"
echo "################################################################"

cd /scripts/ioper/caem/develop/SMNA/ecflow || { echo "❌ Diretório não encontrado"; exit 1; }

echo "Executando git pull..."
if ! git pull origin develop; then
  echo "❌ Erro ao executar git pull"
  conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "❌ Erro ao executar git pull"
  exit 1
fi
echo "✅ git pull concluído com sucesso"
conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "✅ git pull concluído com sucesso"

# --- Valida suite ---
echo "Validando suite..."
if ! conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/validatesuite.py SMNA_PRE_OPER.def; then
  echo "❌ Falha na validação da suite"
  conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "❌ Falha na validação da suite"
  exit 1
fi
echo "✅ Suite validada com sucesso"
conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "✅ Suite validada com sucesso"


# --- Executa ecflow_client ---
echo "Executando ecflow_client..."
export ECF_HOST=caem.cptec.inpe.br
export ECF_PORT=3141

if ! ecflow_client --replace=/SMNA_PRE_OPER SMNA_PRE_OPER.def; then
  echo "❌ Erro ao executar ecflow_client"
  conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "❌ Erro ao executar ecflow_client"
  exit 1
fi
echo "✅ ecflow_client executado com sucesso"
conda run -n cicd python /scripts/ioper/caem/develop/SMNA/git_cicd_consumer/send_telegram_message.py "✅ ecflow_client executado com sucesso"


echo "################################################################"
echo "#######   END of the bash script   (git_pull_ecflow).   #######"
echo "################################################################"
