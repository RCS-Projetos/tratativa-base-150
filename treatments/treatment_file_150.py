import pandas as pd
import numpy as np
from functions import ctrcs_list,searc_ctrcs_registers, merge_ctrcs, old_ctrcs, send_registers
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Robo-150")

def treat_file_150(new_file: str):
    try:
        
        df = pd.read_csv(
            new_file, 
            sep=';',
            dtype=str, 
            encoding='latin-1'
        )
    
        mapa_colunas = {
            'CTRC': 'Key',
            'UNID_ENTREGA': 'Receiving unit',
            'LOCALIZACAO': 'Current location description',
            'PREV_ENTREGA': 'Delivery due'
        }

        df.rename(columns=mapa_colunas, inplace=True, errors='ignore')
        df_tratado = \
            df[
                [
                # --- Itens Originais (Inglês) ---
                'Key',
                'Receiving unit',
                'Delivery due',
                'Current location description'
                ]
            ]
        
        df_tratado = df_tratado.replace({np.nan: None})

        response = searc_ctrcs_registers(
                ctrcs_list(df_tratado)
            )

        if response.status_code != 200 or not response.json():
            os.remove(new_file)
            logger.error(f"Nenhum Registro encontrado")
            return

        response_data = response.json()

        df_response = pd.DataFrame(response_data)

        df_registers = merge_ctrcs(
            df_tratado,
            df_response
        )
        
        df_old_registers = old_ctrcs(df_registers)
        
        qtde_registros = len(df_old_registers)
        
        if qtde_registros == 0:
            os.remove(new_file)
            logger.info("Nenhum registro para enviar.")
            return
        
        logger.info(f"Enviando {qtde_registros} registros antigos")
        send_registers(df_old_registers, '455/bulk-update/', 'patch')

        os.remove(new_file)
    
    except Exception as e:
        logger.error(f"Erro ao processar o 455: {str(e)}, File: {new_file}")