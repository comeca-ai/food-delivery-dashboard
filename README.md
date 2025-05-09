# Dashboard de Mercado Brasileiro de Food Delivery

Um dashboard interativo para análise estratégica do mercado brasileiro de food delivery, mostrando market share, projeções, análise SWOT e recomendações estratégicas.

## Visão geral

Este projeto apresenta um dashboard interativo para análise do mercado brasileiro de food delivery. Ele inclui:
- Participação de mercado atual e projeções
- Análise comparativa dos principais players (iFood, Rappi, 99Food, Meituan)
- Análise SWOT detalhada
- Recomendações estratégicas para o iFood

## Imagens do Dashboard

![Dashboard Food Delivery](https://i.ibb.co/ySZGrnt/market-overview.png)

## Tecnologias utilizadas

- Python 3.11
- Dash
- Plotly
- Pandas
- Bootstrap

## Implantação no Render

Este dashboard está configurado para implantação no [Render](https://render.com/). Para implantar:

1. Crie uma conta no Render (se ainda não tiver)
2. Conecte sua conta GitHub ao Render
3. Crie um novo Web Service no Render
4. Selecione o repositório com o código deste dashboard
5. Configure o serviço:
   - Nome: food-delivery-dashboard (ou outro nome de sua escolha)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:server`
6. Clique em "Create Web Service"

O deploy será automático e a aplicação estará disponível em alguns minutos em uma URL fornecida pelo Render.

### Configurações Ambientais

Este projeto usará as seguintes variáveis de ambiente no Render:

- `PORT`: Automaticamente configurado pelo Render
- `PYTHON_VERSION`: 3.11.8 (configurado pelo arquivo runtime.txt)

## Executando Localmente

Para executar este dashboard localmente:

1. Clone o repositório
   ```bash
   git clone https://github.com/seu-usuario/food-delivery-dashboard.git
   cd food-delivery-dashboard
   ```

2. Crie e ative um ambiente virtual
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação
   ```bash
   python app.py
   ```

5. Acesse o dashboard em [http://localhost:8050](http://localhost:8050)

## Estrutura do Projeto

```
food-delivery-dashboard/
├── app.py                 # Ponto de entrada principal da aplicação
├── deploy_dashboards_online.py  # Funções para criar o dashboard e componentes
├── requirements.txt       # Dependências do projeto
├── Procfile               # Configuração para deploy no Render
├── runtime.txt            # Versão do Python para o deploy
├── README.md              # Este arquivo
├── assets/                # Arquivos estáticos (CSS, imagens)
│   ├── custom.css         # Estilos personalizados
│   └── delivery-icon.png  # Ícone do projeto
└── data/                  # Diretório para armazenar dados
    └── processed_data.json  # Dados do dashboard (gerados automaticamente)
```

## Funcionalidades

- **Visão do Mercado**: Visualização do market share atual e projetado, crescimento do mercado e cobertura dos players.
- **Análise Competitiva**: Comparação de taxas e comissões, análise radar de fatores-chave.
- **Análise SWOT**: Visão detalhada de forças, fraquezas, oportunidades e ameaças para cada player.
- **Recomendações Estratégicas**: Iniciativas defensivas e ofensivas, cronograma de implementação e objetivos estratégicos.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para dúvidas ou sugestões, entre em contato pelo email: seu-email@exemplo.com
