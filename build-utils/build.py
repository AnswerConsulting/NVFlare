import argparse
from ast import Num
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_file", type=str, default="project.yml", help="file to describe FL project")
    parser.add_argument("-w", "--workspace", type=str, default="workspace", help="directory used by provision")
    parser.add_argument("-t", "--type", type=str, default="server", help="type of nvflare app to provision, server or client")
    parser.add_argument("-h", "--host", type=str, default="localhost", help="the server will listen to this host address or the client will send requests to it")
    parser.add_argument("-p", "--port", type=int, default=8002, help="port number appened to host")

    args = parser.parse_args()
    
    subprocess.call(["provision", "-p", "flip-provisioner/project.yml", "-w", "my-workspace"])

if __name__ == "__main__":
    main()