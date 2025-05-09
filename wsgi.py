
from deploy_dashboards_online import create_sample_data, create_app

data = create_sample_data()

app = create_app(data)
server = app.server
