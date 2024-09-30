import json

import quart
import quart_cors
from quart import request

import subprocess
import os

from pathlib import Path

def read_file_if_exists(file_path):
    path = Path(file_path)
    if path.exists():
        with path.open('r') as file:
            return file.read()
    else:
        return ""

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

def is_num(x):
    # only nonnegative numbers, float or int
    return x.replace('.','',1).isdigit()

def check_param_num(request, k, v):
    x = str(request.get(k, v))
    if is_num(x):
        return x, ""
    else:
        return v, f"Warning: ignoring parameter {k}, because {x} is not a number -- using default {v} instead.\n"

@app.post("/run")
async def run():
    stderr_text = ""

    request = await quart.request.get_json(force=True)
    ka = request["ka"]
    param_l, l_err = check_param_num(request, "l", "100")
    param_p, p_err = check_param_num(request, "p", "1.0")

    stderr_text += l_err
    stderr_text += p_err

    project_path = "/home/namin/KappaTools"

    with open(f'{project_path}/input.ka', 'w') as file:
        file.write(ka)
    delete_file(f'{project_path}/output.csv')
    
    env = os.environ.copy()

    venv_path = f'{project_path}/kappa-env'
    env['VIRTUAL_ENV'] = venv_path
    env['PATH'] = f"{venv_path}/bin:{env['PATH']}"

    result = subprocess.run([f'{project_path}/bin/KaSim', '-i', 'input.ka', '-l', param_l, '-p', param_p, '-o', f'{project_path}/output.csv'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = result.stdout.decode('utf-8')
    stderr_text += result.stderr.decode('utf-8')

    with open(f'{project_path}/run.txt', 'w') as file:
        file.write(text)
    with open(f'{project_path}/run_err.txt', 'w') as file:
        file.write(stderr_text)
    output = read_file_if_exists('output.csv')

    response = json.dumps({'stdout': text, 'stderr': stderr_text, 'output': output})
    return quart.Response(response=response, mimetype="text/json", status=200)

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    s = '' if host == 'localhost' else 's'
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"http{s}://{host}")
        return quart.Response(text, mimetype="text/yaml")

@app.get("/")
async def index():
    with open("index.html") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/html")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
