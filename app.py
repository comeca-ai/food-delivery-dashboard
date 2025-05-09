import os
import json
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Importar a função para criar o app e dados de amostra
from deploy_dashboards_online import create_app, create_sample_data, setup_assets_folder

# Configurar pasta assets se não existir
if not os.path.exists('assets'):
    setup_assets_folder()

# Verificar se há dados processados disponíveis
data_file = 'data/processed_data.json'

if os.path.exists(data_file):
    # Carregar dados processados
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Carregando dados processados do arquivo...")
    except Exception as e:
        print(f"Erro ao carregar dados processados: {e}")
        print("Usando dados de amostra...")
        data = create_sample_data()
else:
    # Criar pasta data se não existir
    os.makedirs('data', exist_ok=True)
    
    # Usar dados de amostra
    print("Arquivo de dados processados não encontrado. Usando dados de amostra...")
    data = create_sample_data()
    
    # Salvar dados de amostra para uso futuro
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Criar aplicação
app = create_app(data)
server = app.server  # Para deploy no Render

# Garantir que o app tenha título e metadados
app.title = "Dashboard de Food Delivery Brasil"

# Ajuste para implantação no Render
if __name__ == '__main__':
    # Pegar porta do ambiente ou usar 8050 como padrão
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)
