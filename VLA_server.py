import socket
import torch
import pickle

from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image


ROS_ip = ""
ROS_port = 8000

VLA_ip = ""
VLA_port = 8001

def send_coords(coords_pickle):
    # Create a TCP/IP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ROS_ip, ROS_port))

    # Read the file in chunks and send it to the server
    coords_data = coords_pickle.read(2048)

    # Continue sending data until the end of the file
    while coords_data:
        client.send(image_data)
        coords_data = coords_pickle.read(2048)

    # Close the socket
    client.close()

# Load Processor & VLA
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
vla = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b", 
    # attn_implementation="flash_attention_2",  # [Optional] Requires `flash_attn`
    torch_dtype=torch.bfloat16, 
    low_cpu_mem_usage=True, 
    trust_remote_code=True
).to("cuda:0")

# Prompt for VLA
prompt = "In: What action should the robot take to {<INSTRUCTION>}?\nOut:"

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((VLA_ip, VLA_port))
server.listen()

print(f"Server IP: {VLA_ip}")
print(f"Server is listening on port {VLA_port}")

# Accept incoming connections
while True:
    client_socket, addr = server.accept()

    # Receive the txt data from the client and write to file
    file = open('robot_img.img', 'wb')
    image_data = client_socket.recv(2048)

    # Continue receiving data until no more is sent
    while image_data:
        file.write(image_data)
        image_data = client_socket.recv(2048)
    file.close()

    # Predict Action (7-DoF; un-normalize for BridgeData V2)
    inputs = processor(prompt, image).to("cuda:0", dtype=torch.bfloat16)
    action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)
    action_pickle = pickle.dumps(action)
    
    send_coords()

    