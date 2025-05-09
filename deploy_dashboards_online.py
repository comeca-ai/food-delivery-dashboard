import os
import re
import json
import pandas as pd
import numpy as np
import io
import base64
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Dados de amostra (para ser executado sem acesso aos arquivos originais)
def create_sample_data():
    data = {
        'market_share': {'iFood': 80, 'Rappi': 15, 'Outros': 5},
        'market_share_projection': {
            'current': {'iFood': 80, 'Rappi': 15, 'Outros': 5},
            '2025_q4': {'iFood': 70, 'Rappi': 18, '99Food': 7, 'Outros': 5},
            '2026_q2': {'iFood': 65, 'Rappi': 20, '99Food': 10, 'Meituan': 2, 'Outros': 3}
        },
        'growth_projections': [
            {'year': '2019', 'revenue': 92},
            {'year': '2023', 'revenue': 139},
            {'year': '2024', 'revenue': 148},
            {'year': '2025', 'revenue': 159},
            {'year': '2026', 'revenue': 170},
            {'year': '2027', 'revenue': 181},
            {'year': '2028', 'revenue': 194}
        ],
        'metrics': {
            'ticket_range': [50, 100],
            'delivery_time': [30, 45],
            'nps': {'iFood': 60, 'Rappi': 44}
        },
        'swot': {
            'iFood': {
                'strengths': ['escala', 'marca forte', 'tecnologia avançada', 'vasta rede de restaurantes', 
                              'ecossistema em expansão', 'rentabilidade crescente'],
                'weaknesses': ['altas comissões', 'vulnerabilidade à guerra de preços', 
                               'gargalos logísticos', 'dependência do mercado brasileiro'],
                'opportunities': ['diversificação', 'mercado em crescimento', 'expansão para novas verticais',
                                 'desenvolvimento de serviços B2B', 'monetização de dados'],
                'threats': ['rivais com taxa zero', 'entrada da Meituan', 'mudanças regulatórias',
                           'instabilidade econômica', 'aumento de custos operacionais']
            },
            'Rappi': {
                'strengths': ['super‑app', 'Prime', 'marca forte em outros segmentos', 
                             'investimento robusto', 'entregas ultrarrápidas'],
                'weaknesses': ['menor cobertura', 'dependência de promoções', 
                              'complexidade operacional', 'rentabilidade desafiadora'],
                'opportunities': ['crescimento via taxa zero', 'expansão da base', 
                                 'fortalecimento do Rappi Turbo', 'serviços financeiros'],
                'threats': ['reação do iFood', 'sustentabilidade financeira', 
                           'concorrência da 99Food', 'entrada da Meituan']
            },
            '99Food': {
                'strengths': ['base da 99 mobilidade', 'isenção de taxas por 2 anos',
                             'respaldo da Didi', 'acesso à rede logística existente'],
                'weaknesses': ['histórico de saída do mercado', 'marca menos estabelecida',
                              'necessidade de reconquistar confiança', 'viabilidade a longo prazo'],
                'opportunities': ['conquistar restaurantes insatisfeitos', 'consumidores sensíveis a preço',
                                 'expansão rápida via infraestrutura da 99', 'refeições mais acessíveis'],
                'threats': ['concorrência do iFood e Rappi', 'saturação de ofertas taxa zero',
                           'retenção após período promocional', 'desafios na execução']
            },
            'Meituan': {
                'strengths': ['recursos massivos', 'expertise tecnológica', 
                             'eficiência logística', 'experiência em mercados emergentes'],
                'weaknesses': ['desconhecimento da cultura local', 'novidade no mercado brasileiro',
                              'necessidade de construir base de zero', 'adaptação regulatória'],
                'opportunities': ['mercado sedento por alternativas', 'transferência de know-how da China',
                                 'disrupção via inovação', 'mercado ainda em crescimento'],
                'threats': ['barreiras regulatórias', 'reação agressiva de incumbentes',
                           'adaptação cultural', 'dificuldades operacionais iniciais']
            }
        },
        'recommendations': [
            'Defender base de restaurantes com redução temporária de taxas e serviços de valor agregado',
            'Expandir verticais (iFood Mercado, farmácia, pet) e investir em IA, lockers e drones',
            'Reforçar Clube iFood com níveis Gold/Platinum e benefícios externos',
            'Parcerias estratégicas com varejistas e fintechs; aquisições de apps regionais'
        ],
        'players': {
            'iFood': {'cities': 1530, 'users': 56000000, 'restaurants': 350000, 'active_monthly_users': 22000000, 'subscription_users': 11000000},
            'Rappi': {'cities': 300, 'users': 5500000, 'restaurants': 30000, 'active_monthly_users': 3000000, 'subscription_users': 3850000},
            '99Food': {'cities': 0, 'users': 0, 'restaurants': 0, 'active_monthly_users': 0, 'subscription_users': 0},
            'Aiqfome': {'cities': 1600, 'users': 6000000, 'restaurants': 30000, 'active_monthly_users': 1200000, 'subscription_users': 800000}
        },
        'commission_rates': [
            {'player': 'iFood', 'base_rate': 12, 'max_rate': 27, 'monthly_fee': 115, 'payment_fee': 3.5, 'notes': 'Taxas tradicionais mantidas'},
            {'player': 'Rappi', 'base_rate': 0, 'max_rate': 0, 'monthly_fee': 0, 'payment_fee': 3.5, 'notes': 'Isenção até 31/07/2025'},
            {'player': '99Food', 'base_rate': 0, 'max_rate': 0, 'monthly_fee': 0, 'payment_fee': 0, 'notes': 'Isenção por 2 anos'}
        ],
        'revenue_diversification': [
            {'source': 'Comissões', 'current': 65, 'target': 45},
            {'source': 'Taxas de Entrega', 'current': 15, 'target': 15},
            {'source': 'Publicidade', 'current': 10, 'target': 15},
            {'source': 'Serviços Financeiros', 'current': 5, 'target': 15},
            {'source': 'Clube iFood', 'current': 5, 'target': 5},
            {'source': 'B2B/Tecnologia', 'current': 0, 'target': 5}
        ],
        'price_war_scenarios': [
            {'scenario': 'Resposta agressiva', 'market_share_impact': -5, 'revenue_impact': -25, 'long_term_viability': 'Baixa'},
            {'scenario': 'Resposta seletiva', 'market_share_impact': -10, 'revenue_impact': -10, 'long_term_viability': 'Média'},
            {'scenario': 'Diferenciação por valor', 'market_share_impact': -15, 'revenue_impact': -5, 'long_term_viability': 'Alta'}
        ],
        'penetration_rate': {
            'overall': 63, # 63% dos smartphones com iFood instalado
            'by_region': {
                'Sudeste': 72,
                'Sul': 65,
                'Nordeste': 58,
                'Centro-Oeste': 61,
                'Norte': 52
            },
            'by_age': {
                '18-24': 81,
                '25-34': 75,
                '35-44': 62,
                '45-54': 48,
                '55+': 32
            }
        },
        'loyalty_programs': {
            'iFood': {
                'name': 'Clube iFood',
                'users': 11000000,
                'penetration': 20, # % da base total
                'benefits': ['Frete grátis', 'Descontos exclusivos', 'Cashback'],
                'monthly_cost': 19.90,
                'retention_rate': 75
            },
            'Rappi': {
                'name': 'Rappi Prime',
                'users': 3850000,
                'penetration': 70, # % da base total
                'benefits': ['Frete grátis', 'Cashback', 'Entrega prioritária', 'Descontos em outras categorias'],
                'monthly_cost': 29.90,
                'retention_rate': 68
            }
        }
    }
    return data

# Função para gerar a aplicação Dash com os dashboards
def create_app(data):
    # Inicializar aplicação Dash
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server  # Expor o servidor para deploy
    
    # Layout do Dashboard
    app.layout = dbc.Container([
        html.Div([
            html.Img(src='/assets/delivery-icon.png', height='60px', style={'float': 'left', 'margin-right': '15px'}),
            html.H1("Mercado Brasileiro de Food Delivery", className="display-4"),
            html.P("Análise Estratégica do Setor de Food Service e Delivery no Brasil (2024-2025)", className="lead")
        ], className="text-center my-4 py-3 bg-light rounded"),
        
        # Abas para diferentes dashboards
        dbc.Tabs([
            # Aba 1: Visão Geral do Mercado
            dbc.Tab(label="Visão do Mercado", tab_id="mercado", children=[
                dbc.Row([
                    # Market Share
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Participação de Mercado - Food Delivery", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="market-share-pie")
                            ])
                        ], className="shadow")
                    ], width=6),
                    
                    # Evolução projetada do Market Share
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H4("Evolução Projetada do Market Share", className="text-center"),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Atual", "value": "current"},
                                        {"label": "Q4 2025", "value": "2025_q4"},
                                        {"label": "Q2 2026", "value": "2026_q2"}
                                    ],
                                    value="current",
                                    id="market-share-period",
                                    inline=True,
                                    className="d-flex justify-content-center my-2"
                                )
                            ]),
                            dbc.CardBody([
                                dcc.Graph(id="market-share-projection")
                            ])
                        ], className="shadow")
                    ], width=6)
                ], className="mb-4"),
                
                dbc.Row([
                    # Crescimento do Mercado
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Crescimento do Mercado (R$ Bilhões)", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="market-growth-line")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4"),
                
                dbc.Row([
                    # Cobertura dos Players
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Cobertura de Mercado", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="market-coverage")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4")
            ]),
            
            # Aba 2: Análise Competitiva
            dbc.Tab(label="Análise Competitiva", tab_id="competitivo", children=[
                dbc.Row([
                    # Comparativo de Taxas
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Comparativo de Taxas e Comissões (Q2 2025)", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="commission-rates")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4"),
                
                dbc.Row([
                    # Radar Chart - Comparação de Forças
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Comparativo de Players - Fatores-Chave", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="radar-comparison")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4"),
                
                dbc.Row([
                    # Notas sobre Taxas
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Notas sobre Políticas de Taxas", className="text-center")),
                            dbc.CardBody([
                                html.Ul([
                                    html.Li([
                                        html.Strong(f"{item['player']}: "), 
                                        f"{item['notes']}",
                                        html.Br(),
                                        html.Small(f"Taxa base: {item['base_rate']}% | Taxa máxima: {item['max_rate']}% | " + 
                                                f"Mensalidade: R${item['monthly_fee']} | Taxa processamento: {item['payment_fee']}%")
                                    ]) for item in data['commission_rates']
                                ], className="list-group")
                            ])
                        ], className="shadow")
                    ], width=12)
                ])
            ]),
            
            # Aba 3: Análise SWOT
            dbc.Tab(label="Análise SWOT", tab_id="swot", children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H4("Análise SWOT por Player", className="text-center"),
                                dbc.Tabs([
                                    dbc.Tab(label="iFood", tab_id="tab-ifood"),
                                    dbc.Tab(label="Rappi", tab_id="tab-rappi"),
                                    dbc.Tab(label="99Food", tab_id="tab-99food"),
                                    dbc.Tab(label="Meituan", tab_id="tab-meituan")
                                ], id="swot-tabs", active_tab="tab-ifood")
                            ]),
                            dbc.CardBody([
                                html.Div(id="swot-content")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4")
            ]),
            
            # Aba 4: Recomendações Estratégicas
            dbc.Tab(label="Recomendações Estratégicas", tab_id="recomendacoes", children=[
                dbc.Row([
                    # Diversificação de Receitas
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Diversificação de Fontes de Receita (iFood)", className="text-center")),
                            dbc.CardBody([
                                dcc.Graph(id="revenue-diversification")
                            ])
                        ], className="shadow")
                    ], width=12)
                ], className="mb-4"),
                
                dbc.Row([
                    # Recomendações
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Plano Estratégico para o iFood", className="text-center")),
                            dbc.CardBody([
                                html.Div(id="recommendations-content")
                            ])
                        ], className="shadow")
                    ], width=12)
                ])
            ])
        ], id="main-tabs", active_tab="mercado"),
        
        html.Footer([
            html.Hr(),
            html.P("Fonte: Análise Estratégica do Mercado de Food Service e Delivery no Brasil (2024-2025)", 
                   className="text-center text-muted")
        ], className="mt-4")
    ], fluid=True, className="px-4 py-3")
    return app
    
    # Callbacks
    @app.callback(Output("market-share-pie", "figure"),
                  Input("market-share-pie", "id"))
    def update_market_share(id):
        labels = list(data['market_share'].keys())
        values = list(data['market_share'].values())
        colors = ['#EA1D2C', '#FF6900', '#DDDDDD']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        
        fig.update_layout(
            margin=dict(t=30, b=60, l=30, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            annotations=[
                dict(
                    text="Fonte: Euromonitor, 2024",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2,
                    font=dict(size=10, color="gray")
                )
            ]
        )
        
        return fig
    
    @app.callback(Output("market-share-projection", "figure"),
                  Input("market-share-period", "value"))
    def update_market_share_projection(period):
        labels = list(data['market_share_projection'][period].keys())
        values = list(data['market_share_projection'][period].values())
        
        # Cores personalizadas para os players
        colors = {
            'iFood': '#EA1D2C',
            'Rappi': '#FF6900',
            '99Food': '#9D4EDD',
            'Meituan': '#3B0086',
            'Outros': '#DDDDDD'
        }
        
        # Criar lista de cores na ordem dos labels
        color_list = [colors.get(label, '#DDDDDD') for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker=dict(colors=color_list),
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        
        # Título dinâmico baseado no período selecionado
        title_map = {
            "current": "Market Share Atual",
            "2025_q4": "Projeção Q4 2025 (pós 99Food)",
            "2026_q2": "Projeção Q2 2026 (com Meituan)"
        }
        
        period_text = {
            "current": "(Maio 2025)",
            "2025_q4": "(Outubro-Dezembro 2025)",
            "2026_q2": "(Abril-Junho 2026)"
        }
        
        fig.update_layout(
            title=dict(
                text=title_map.get(period, "Market Share Projetado"),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(t=50, b=60, l=30, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            annotations=[
                dict(
                    text=f"Fonte: Análise Interna {period_text.get(period, '')}",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2,
                    font=dict(size=10, color="gray")
                )
            ]
        )
        
        return fig
    
    @app.callback(Output("market-growth-line", "figure"),
                  Input("market-growth-line", "id"))
    def update_market_growth(id):
        years = [item['year'] for item in data['growth_projections']]
        revenues = [item['revenue'] for item in data['growth_projections']]
        
        fig = go.Figure()
        
        # Dados históricos
        hist_end = 2  # Assumindo que os primeiros pontos são históricos (2019, 2023)
        fig.add_trace(go.Scatter(
            x=years[:hist_end], 
            y=revenues[:hist_end],
            mode='lines+markers',
            name='Histórico',
            line=dict(color='#EA1D2C', width=3),
            marker=dict(size=10)
        ))
        
        # Projeções
        fig.add_trace(go.Scatter(
            x=years[hist_end-1:], 
            y=revenues[hist_end-1:],
            mode='lines+markers',
            name='Projeção',
            line=dict(color='#EA1D2C', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        # Adicionar anotações para contextualizar
        fig.add_annotation(
            x="2019", y=92,
            text="Base pré-pandemia",
            showarrow=True,
            arrowhead=1,
            ax=0, ay=-40
        )
        
        fig.add_annotation(
            x="2023", y=139,
            text="+50,8% vs. 2019",
            showarrow=True,
            arrowhead=1,
            ax=0, ay=-40
        )
        
        fig.add_annotation(
            x="2028", y=194,
            text="CAGR +6,9% (2023-2028)",
            showarrow=True,
            arrowhead=1,
            ax=0, ay=-40
        )
        
        fig.update_layout(
            title="Crescimento do Mercado Brasileiro de Food Delivery",
            xaxis_title="Ano",
            yaxis_title="Faturamento (R$ Bilhões)",
            margin=dict(t=50, b=60, l=30, r=30),
            annotations=[
                dict(
                    text="Fonte: IMARC Group, Mordor Intelligence, Grand View Research (Dados até 2023: históricos; 2024-2028: projeções)",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2,
                    font=dict(size=10, color="gray")
                )
            ]
        )
        
        return fig
    
    @app.callback(Output("market-coverage", "figure"),
                  Input("market-coverage", "id"))
    def update_market_coverage(id):
        # Preparar dados de cobertura
        players = []
        cities = []
        restaurants = []
        users = []
        
        for player, data_player in data['players'].items():
            if 'cities' in data_player and 'restaurants' in data_player and 'users' in data_player:
                players.append(player)
                cities.append(data_player['cities'])
                restaurants.append(data_player['restaurants'])
                users.append(data_player['users'] / 1000000)  # Converter para milhões
        
        # Criar figura
        fig = go.Figure()
        
        # Adicionar barras para cada métrica
        fig.add_trace(go.Bar(
            x=players,
            y=cities,
            name='Cidades',
            marker_color='#3B0086'
        ))
        
        fig.add_trace(go.Bar(
            x=players,
            y=restaurants,
            name='Restaurantes (x1.000)',
            marker_color='#EA1D2C',
            text=[f"{r/1000:.1f}k" for r in restaurants],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=players,
            y=users,
            name='Usuários (milhões)',
            marker_color='#FF6900',
            text=[f"{u:.1f}M" for u in users],
            textposition='auto'
        ))
        
        # Layout
        fig.update_layout(
            title="Cobertura de Mercado dos Principais Players",
            barmode='group',
            xaxis_title="Players",
            margin=dict(t=50, b=60, l=30, r=30),
            annotations=[
                dict(
                    text="Fonte: Relatórios corporativos, Prosus Annual Report 2024, Magazine Luiza Investor Relations (Maio 2025)",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2,
                    font=dict(size=10, color="gray")
                )
            ]
        )
        
        return fig
    
    @app.callback(Output("commission-rates", "figure"),
                  Input("commission-rates", "id"))
    def update_commission_rates(id):
        players = [item['player'] for item in data['commission_rates']]
        base_rates = [item['base_rate'] for item in data['commission_rates']]
        max_rates = [item['max_rate'] for item in data['commission_rates']]
        payment_fees = [item['payment_fee'] for item in data['commission_rates']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=players,
            y=base_rates,
            name='Taxa Base (%)',
            marker_color='#8884d8'
        ))
        
        fig.add_trace(go.Bar(
            x=players,
            y=max_rates,
            name='Taxa Máxima (%)',
            marker_color='#82ca9d'
        ))
        
        fig.add_trace(go.Bar(
            x=players,
            y=payment_fees,
            name='Taxa Processamento (%)',
            marker_color='#ffc658'
        ))
        
        fig.update_layout(
            title="Comparativo de Taxas e Comissões (Q2 2025)",
            barmode='group',
            margin=dict(t=50, b=60, l=30, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            annotations=[
                dict(
                    text="Fonte: Valores oficiais divulgados pelas empresas, ABRASEL, Relatórios à imprensa (Maio 2025)",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.3,
                    font=dict(size=10, color="gray")
                )
            ]
        )
        
        return fig
    
    @app.callback(Output("radar-comparison", "figure"),
                  Input("radar-comparison", "id"))
    def update_radar_comparison(id):
        # Dados para comparação de fatores-chave
        factors = [
            'Marca', 'Base de Usuários', 'Variedade de Restaurantes', 
            'Qualidade Logística', 'Tecnologia & IA', 'Diversificação',
            'Poder Financeiro', 'Experiência do Usuário'
        ]
        
        # Valores em uma escala de 1-10 (subjetivos)
        ifood_values = [9, 9, 9, 8, 8, 7, 8, 8]
        rappi_values = [7, 6, 6, 7, 7, 9, 7, 7]
        food99_values = [5, 4, 3, 6, 5, 5, 8, 6]
        meituan_values = [4, 3, 3, 9, 10, 8, 10, 9]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=ifood_values,
            theta=factors,
            fill='toself',
            name='iFood',
            line=dict(color='#EA1D2C')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=rappi_values,
            theta=factors,
            fill='toself',
            name='Rappi',
            line=dict(color='#FF6900')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=food99_values,
            theta=factors,
            fill='toself',
            name='99Food',
            line=dict(color='#9D4EDD')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=meituan_values,
            theta=factors,
            fill='toself',
            name='Meituan (Potencial)',
            line=dict(color='#3B0086')
        ))
