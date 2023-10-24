#!/usr/bin/python
import json
import subprocess

# Jalankan Terraform untuk mendapatkan alamat IP dari output
terraform_command = "terraform output -json"
output = subprocess.check_output(terraform_command, shell=True)
terraform_output = json.loads(output)

# Definisikan nama EC2 secara manual
manual_ec2_names = ["docker01", "docker02"]

dynamic_inventory = {}

# Iterasi melalui nama EC2 yang telah Anda definisikan secara manual
for ec2_name in manual_ec2_names:
    # Dapatkan alamat IP dari output Terraform
    ec2_ip = terraform_output["ec2_name_to_ip"]["value"][ec2_name]
    
    dynamic_inventory[ec2_name] = {
        "ansible_ssh_host": ec2_ip,
        "ansible_ssh_user": "ubuntu",
        "ansible_become": True,
        "ansible_become_password": "gameover213",
        "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
    }

print(json.dumps(dynamic_inventory))