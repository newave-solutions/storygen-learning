
import os
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from story_agent.agent import root_agent as story_agent
from story_image_agent.agent import root_agent as image_agent

load_dotenv()

APP_NAME = "storygen_new_app"

project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT_ID")

if project_id:
    try:
        story_runner = InMemoryRunner(app_name=APP_NAME, agent=story_agent)
        image_runner = InMemoryRunner(app_name=APP_NAME, agent=image_agent)
        print("Runners initialized successfully")
    except Exception as e:
        print(f"Error initializing runners: {e}")
else:
    print("Project ID not set")
