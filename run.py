import os
import subprocess

if __name__ == "__main__":
    web_app_module = "app:app"
    api_app_module = "api.v1.app:app"
    
    web_app_command = f"gunicorn --bind 0.0.0.0:5001 {web_app_module}"
    api_app_command = f"gunicorn --bind 0.0.0.0:5000 {api_app_module}"
    
    subprocess.run(web_app_command, shell=True)
    subprocess.run(api_app_command, shell=True)
