import argparse
import subprocess
import yaml
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_file", type=str, default="project.yml", help="file to describe FL project")
    parser.add_argument("-w", "--workspace", type=str, default="workspace", help="directory used by provision")
    parser.add_argument("--client_host", type=str, default="localhost", help="")
    parser.add_argument("--client_port", type=int, default=8002, help="port number appened to client host")
    parser.add_argument("--server_host", type=str, default="0.0.0.0", help="")
    parser.add_argument("--server_port", type=int, default=8002, help="port number appened to server host")

    args = parser.parse_args()

    current_dir = os.getcwd()

    project_config_file_path = os.path.join(current_dir, args.project_file)
    
    if (os.path.isfile(project_config_file_path) == False):
        raise FileNotFoundError(project_config_file_path)

    project_config = yaml.safe_load(open(project_config_file_path, "r"))
    
    static_file_args = project_config["builders"][2]["args"]
    
    static_file_args = {
        "config_folder": "config",
        "client_port": args.client_port,
        "client_host": args.client_host,
        "server_port": args.server_port,
        "server_host": args.server_host,
        "admin_port": 8003,
        "admin_host": "localhost"
    }

    project_config["builders"][2]["args"] = static_file_args

    yaml.safe_dump(project_config, open(project_config_file_path, "w"))

    subprocess.call(["python3", "-m", "nvflare.lighter.provision", "-p", args.project_file, "-w", args.workspace])

    nvflare_dir = os.path.join(current_dir, "nvflare")

if __name__ == "__main__":
    main()