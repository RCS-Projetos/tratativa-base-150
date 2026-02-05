import os
import requests as rq
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
TIMEOUT = int(os.getenv('TIMEOUT'))

url_path = lambda x: f'{BASE_URL}{x}'

headers = {
    "Content-Type": "application/json" # Remova se não usar auth
}

def searc_ctrcs_registers(ctrcs: list[str]) -> rq.Response:
    
    url = url_path('455/get-by-keys/')
    
    response = rq.post(
        url,
        json={             
            'keys': ctrcs
        },
        timeout=TIMEOUT
    )
  
    return response

def ctrcs_list(df: DataFrame)-> list[str]:
    return df['Key'].to_list()

def merge_ctrcs(df_file: DataFrame, df_response: DataFrame) -> DataFrame:
    try:       
        df = df_file.merge(
                df_response,
                left_on='Key',
                right_on='key',
                how='left'
        )
        return df
    except Exception as e:
        print(f"Erro ao processar ao fazer merge: {str(e)}")
        
    
        
def new_ctrcs(df: DataFrame) -> DataFrame:
    df_new_registers = df[(df['id'].isna()) & (df['Prefix'].notna())].copy()
    return df_new_registers

def old_ctrcs(df: DataFrame) -> DataFrame:
    df_registered = df[df['id'].notna()].copy()
    df_registered_to_update = df_registered[
        (df_registered['Current location description'] != df_registered['current_location']) |
        (pd.to_datetime(df_registered['Delivery due'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d').fillna('') != df_registered['delivery_due'].fillna(''))
        ]
    return df_registered_to_update


def clean_decimal(value):
    if pd.isna(value) or str(value).strip() == '': return 0.0
    return float(str(value).strip().replace('.', '').replace(',', '.'))

def clean_text(value):
    if pd.isna(value) or str(value).strip() == '': return None
    return str(value).strip()

def clean_date(value, is_datetime=False):
    if pd.isna(value) or str(value).strip() == '': return None
    try:
        # Converte para datetime e depois para string ISO
        dt = pd.to_datetime(value, dayfirst=True)
        fmt = '%Y-%m-%dT%H:%M:%SZ' if is_datetime else '%Y-%m-%d'
        return dt.strftime(fmt)
    except:
        return None

     
def build_payload(row):
        record = {
            "key": row.get('Key'),
            "current_location_description": clean_text(row.get('Current location description')),
            "delivery_due": clean_date(row.get('Delivery due')),
            "receiving_unit": {"code": clean_text(row.get('Receiving unit'))} if row.get('Receiving unit') else None,
        }
        
        record = {k: v for k, v in record.items() if v is not None}
        return record
    

def send_registers(df: pd.DataFrame, url: str, method: str):
    total_rows = len(df)
    
    if total_rows == 0:
        print("Nenhum registro para enviar.")
        return
    
    print(f"Iniciando envio de {total_rows} registros...")
    
    for start_idx in range(0, total_rows, BATCH_SIZE):
        end_idx = start_idx + BATCH_SIZE
        batch_df = df.iloc[start_idx:end_idx]
        
        # Converte as linhas do lote atual para a lista de JSONs
        payload_list = [build_payload(row) for _, row in batch_df.iterrows()]
        
        try:
            # Envia o POST
            if method == 'post':
                response = rq.post(url_path(url), json=payload_list, headers=headers)
            elif method == 'patch':
                response = rq.patch(url_path(url), json=payload_list, headers=headers)
            else:
                raise 'Nenhum metodo selecionado.' 
            
            # Verifica sucesso
            if response.status_code in [200, 201]:
                print(f"Lote {start_idx}-{end_idx} enviado com sucesso. {"Atualizado"}")
            else:
                print(f"Erro no lote {start_idx}-{end_idx}: {response.status_code}")
                with open('error.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("Resposta de erro salva em 'error.html'")
        except Exception as e:
            print(f"Exceção crítica no lote {start_idx}-{end_idx}: {str(e)}") 
