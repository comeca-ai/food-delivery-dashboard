# Guia de Implantação no Render

Este guia explica como implantar o Dashboard de Food Delivery no Render, um serviço de hospedagem na nuvem que oferece implantações simples e gratuitas para aplicações web.

## Preparação do Repositório

1. **Crie um repositório no GitHub**

   Primeiro, crie um novo repositório no GitHub para hospedar o código do seu projeto.

2. **Configure o repositório local**

   ```bash
   # Inicialize um repositório Git local
   git init
   
   # Adicione o repositório remoto
   git remote add origin https://github.com/seu-usuario/food-delivery-dashboard.git
   
   # Adicione todos os arquivos
   git add .
   
   # Faça o commit das mudanças
   git commit -m "Configuração inicial do Dashboard de Food Delivery"
   
   # Envie para o GitHub
   git push -u origin main
   ```

## Implantação no Render

### 1. Crie uma conta no Render

Acesse [render.com](https://render.com/) e crie uma conta gratuita se ainda não tiver uma. Você pode se cadastrar usando sua conta do GitHub para facilitar a conexão com seus repositórios.

### 2. Crie um novo Web Service

1. No painel do Render, clique em "New" e selecione "Web Service"
2. Conecte sua conta do GitHub (se ainda não estiver conectada)
3. Selecione o repositório `food-delivery-dashboard`

### 3. Configure o Web Service

Preencha os seguintes campos:

- **Name**: food-delivery-dashboard (ou outro nome de sua escolha)
- **Environment**: Python 3
- **Region**: Escolha a região mais próxima de você ou de seus usuários (São Paulo é a melhor opção para o Brasil)
- **Branch**: main (ou a branch que contém o código)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:server`
- **Plan**: Free

### 4. Configurações Avançadas (opcional)

Clique em "Advanced" se precisar configurar variáveis de ambiente adicionais. Para este projeto, as configurações padrão são suficientes.

### 5. Crie o Web Service

Clique no botão "Create Web Service". O Render começará a construir e implantar sua aplicação. Este processo pode levar alguns minutos.

### 6. Acesse sua Aplicação

Quando a implantação estiver concluída, o Render fornecerá uma URL para acessar sua aplicação, algo como:
`https://food-delivery-dashboard.onrender.com`

## Gerenciamento Contínuo

### Atualizações

Qualquer commit enviado para a branch principal (main) do seu repositório no GitHub desencadeará uma nova implantação automaticamente.

### Monitoramento

No painel do Render, você pode:
- Ver logs em tempo real
- Monitorar o uso de recursos
- Configurar domínios personalizados (planos pagos)
- Gerenciar variáveis de ambiente

## Solução de Problemas

Se encontrar problemas durante a implantação, verifique:

1. **Logs de construção e execução**: Disponíveis no painel do Render
2. **Dependências**: Verifique se todas as dependências estão listadas corretamente no `requirements.txt`
3. **Versão do Python**: Confirmada no arquivo `runtime.txt`
4. **Comando de inicialização**: Deve apontar corretamente para o servidor da sua aplicação (`app:server`)

## Recursos Adicionais

- [Documentação do Render para aplicações Python](https://render.com/docs/deploy-python)
- [Guia do Dash para implantação](https://dash.plotly.com/deployment)
- [Configurando domínios personalizados no Render](https://render.com/docs/custom-domains)