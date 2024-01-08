documentList = [
  {
    "id": 'id do documento na kind Document',
    "patientId": 'id do paciente vinculado ao Document',
    "documentName": 'nome do documento',
    "eSignatureId": 'id da assinatura na kind Global_EletronicSignatureLink',
    "patientName": 'nome do paciente'
  }
]

import os
import requests

download_folder = "documents"
os.makedirs(download_folder, exist_ok=True)

total_files = len(documentList)
files_downloaded = 0

for document in documentList:
    is_digital_certificate = document.get('eDigitalSignatureClinicSigned') == "X" or document.get('eDigitalSignatureSigned') == "X"

    base_url = "https://solution.clinicorp.com/api/digital_certificate/download_document" if is_digital_certificate else "https://solution.clinicorp.com/api/digital_certificate/view_document_with_signatures"

    with open("token.txt", "r") as file:
        token = file.read().strip()

    headers = {"Authorization": f"Bearer {token}"}

    try:
        if is_digital_certificate:
            url = f"{base_url}?id={document['id']}"
            response = requests.get(url, headers=headers)
        else:
            data = {"id": document['id'], "multipleSignatures": True}
            response = requests.post(base_url, json=data, headers=headers)

        if response.status_code == 200:
            intarray = response.json().get('data', [])
            nome_arquivo = os.path.join(download_folder, f"{document['patientName']}-{document['eSignatureId']}.pdf")

            with open(nome_arquivo, "wb") as file:
                for i in intarray:
                    file.write(i.to_bytes(1, byteorder='big'))

            files_downloaded += 1
            print(f"Download do arquivo {nome_arquivo} concluído com sucesso! ({files_downloaded}/{total_files} files downloaded)")
        else:
            print(f"Falha ao baixar o arquivo para o código {document['eSignatureId']}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

print(f"\nTodos os arquivos foram baixados. Total de arquivos: {files_downloaded}/{total_files}")

