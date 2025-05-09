from deploy_dashboards_online import create_app, create_sample_data

data = create_sample_data()
app = create_app(data)
server = app.server
