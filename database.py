# database.py (Versão 2.0 com Projetos e Cenários)

import sqlite3
import json
from datetime import datetime

DB_NAME = 'plataforma_hidraulica.db'

def setup_database():
    """Cria a nova tabela 'scenarios' se ela não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # ALTERADO: A tabela agora se chama 'scenarios' e tem uma estrutura hierárquica.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            project_name TEXT NOT NULL,
            scenario_name TEXT NOT NULL,
            scenario_data TEXT NOT NULL, -- Armazenará os dados do cenário como um JSON
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(username, project_name, scenario_name) -- A combinação dos três deve ser única
        )
    ''')
    conn.commit()
    conn.close()

# ALTERADO: Função renomeada e adaptada para salvar cenários.
def save_scenario(username, project_name, scenario_name, scenario_data):
    """Salva ou atualiza um cenário dentro de um projeto para um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    scenario_data_json = json.dumps(scenario_data)
    timestamp = datetime.now()

    # Lógica para inserir um novo cenário ou substituir um existente.
    cursor.execute('''
        INSERT OR REPLACE INTO scenarios (id, username, project_name, scenario_name, scenario_data, last_modified)
        VALUES ((SELECT id FROM scenarios WHERE username = ? AND project_name = ? AND scenario_name = ?), ?, ?, ?, ?, ?)
    ''', (username, project_name, scenario_name, username, project_name, scenario_name, scenario_data_json, timestamp))
    
    conn.commit()
    conn.close()
    return True

# ALTERADO: Função renomeada e adaptada para carregar cenários.
def load_scenario(username, project_name, scenario_name):
    """Carrega os dados de um cenário específico de um projeto."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT scenario_data FROM scenarios WHERE username = ? AND project_name = ? AND scenario_name = ?", (username, project_name, scenario_name))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])
    return None

# ALTERADO: A query agora busca por nomes de projetos distintos.
def get_user_projects(username):
    """Retorna uma lista com os nomes únicos de todos os projetos de um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT project_name FROM scenarios WHERE username = ? ORDER BY project_name ASC", (username,))
    projects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return projects

# NOVO: Função para buscar todos os cenários de um projeto específico.
def get_scenarios_for_project(username, project_name):
    """Retorna uma lista com os nomes de todos os cenários de um projeto específico."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT scenario_name FROM scenarios WHERE username = ? AND project_name = ? ORDER BY last_modified DESC", (username, project_name))
    scenarios = [row[0] for row in cursor.fetchall()]
    conn.close()
    return scenarios

# ALTERADO: Função renomeada e adaptada para deletar cenários.
def delete_scenario(username, project_name, scenario_name):
    """Deleta um cenário específico de um projeto."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scenarios WHERE username = ? AND project_name = ? AND scenario_name = ?", (username, project_name, scenario_name))
    conn.commit()
    conn.close()
    return True
