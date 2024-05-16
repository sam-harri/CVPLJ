from roboflow import Roboflow
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ROBOFLOW_API_KEY")

rf = Roboflow(api_key=api_key)
project = rf.workspace("cvplj").project("computer-vision-powerlifting")
version = project.version(1)
dataset = version.download("yolov8")
