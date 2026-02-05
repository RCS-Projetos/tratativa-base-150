import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv('BASE_URL')

url_path = lambda x: f'{BASE_URL}{x}'

HEADERS = {
    "Content-Type": "application/json" # Remova se não usar auth
}

def make_report_log(
    report: str, 
    status: Literal['STARTED', 'FINISHED', 'ERROR'], 
    req_type: Literal['post', 'patch'], 
    report_id: Optional[int] = None
) -> requests.Response:
    """
    Registra ou atualiza um log de relatório via API.
    """
    
    # Prepara os dados (Payload)
    data = {
        "report_type": report,
        "status": status
    }

    # Define a URL e o método dinamicamente
    if req_type == 'post':
        url = f"{BASE_URL}report-log/"
        method = requests.post
    else:
        if not report_id:
            raise ValueError("O 'report_id' é obrigatório para requisições do tipo PATCH.")
        url = f"{BASE_URL}report-log/{report_id}/"
        method = requests.patch

    # Realiza a chamada única
    response = method(url, json=data, headers=HEADERS)
    
    # Opcional: Levanta exceção se o status code for 4xx ou 5xx
    response.raise_for_status() 
    
    return response
    