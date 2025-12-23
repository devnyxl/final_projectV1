from roboflow import Roboflow

rf = Roboflow(api_key="8ohHvJBVBGIDNLWLMb4y")
project = rf.workspace("indooroutdoornavigation").project("indoor-obstacle-detection")
dataset = project.version(1).download("tensorflow")  # Adjust version if needed; check on the site.