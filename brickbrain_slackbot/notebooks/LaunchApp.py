# Databricks notebook source
# MAGIC %pip install -qqqq backoff databricks-langchain langgraph==0.5.3 databricks-agents pydantic databricks-sdk databricks-vectorsearch
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

app_name = dbutils.widgets.get("app_name")
ka_endpoint_name = dbutils.widgets.get("ka_endpoint_name")

assert app_name != "", "app_name notebook parameter must be specified"
assert ka_endpoint_name != "", "ka_endpoint_name notebook parameter must be specified"

# COMMAND ----------


from databricks.sdk import WorkspaceClient
from databricks.sdk.service.apps import App, AppResource, AppResourceSecret, AppResourceSecretSecretPermission, AppResourceServingEndpoint, AppResourceServingEndpointServingEndpointPermission, AppDeployment



# COMMAND ----------

w = WorkspaceClient()

serving_endpoint = AppResourceServingEndpoint(name=ka_endpoint_name,
                                              permission=AppResourceServingEndpointServingEndpointPermission.CAN_QUERY
                                              )
                                        
secret_bot_token = AppResourceSecret(scope="brickbrain-scope", key="slack-bot-token", permission=AppResourceSecretSecretPermission.CAN_READ)

app_resource = AppResource(name="brickbrain_slackbot_resource", 
                           serving_endpoint=serving_endpoint, 
                           secret=secret_bot_token
                           ) 

agent_app = App(name=app_name, 
              description="Your Databricks assistant", 
              default_source_code_path=os.getcwd(),
              resources=[app_resource])
    
try:
  app_details = w.apps.create_and_wait(app=agent_app)
  print(app_details)
except Exception as e:
  if "already exists" in str(e):
    app_details = w.apps.get(app_name)
    print(app_details)
  else:
    raise e

# COMMAND ----------

deployment = AppDeployment(
  source_code_path=os.getcwd()
)

app_details = w.apps.deploy_and_wait(app_name=app_name, app_deployment=deployment)
print(app_details)