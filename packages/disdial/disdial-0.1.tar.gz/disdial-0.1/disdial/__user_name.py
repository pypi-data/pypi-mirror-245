from .__utils import *
from .__constants import *

# def _run_command(command, power_shell=False):
#         try:
#             startupinfo = subprocess.STARTUPINFO()
#             startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#             process = subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, 
#                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=power_shell, text=True).stdout.read()
#             return str(process)+"\n"
        
#         except subprocess.CalledProcessError as e:
#                 return f"Error: {e}"

# def extract_name_from_cli():
#     command = ["systeminfo"]
#     sys_info = _run_command(command)
#     username = sys_info.split("\n")[4].split(":")[1].strip()

#     return username

def read_name():
    with open(JSON_FILE_PATH, "r") as f:
        return json.load(f)["name"]

def change_name(username):
    with open(JSON_FILE_PATH, "w") as f:
        json.dump({"name": username}, f)
        return "-> username set to {username}"
    
def get_user_name():
    with open(JSON_FILE_PATH, "r") as f:
        name = json.load(f)["name"]

    if name=="None":
        name = input("Please enter your name: ")
    
    return name