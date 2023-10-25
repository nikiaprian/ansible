import boto3
import json
import os

# Inisialisasi klien EC2 AWS
ec2 = boto3.client('ec2', region_name='us-west-2')  # Ganti dengan wilayah yang sesuai

# Tentukan nama-nama instance EC2 yang ingin Anda cari
manual_ec2_names = ["docker01", "docker02"]

inventory_content = "[docker]\n"

for ec2_name in manual_ec2_names:
    # Dapatkan alamat IP publik berdasarkan nama instance
    response = ec2.describe_instances(Filters=[
        {'Name': 'tag:Name', 'Values': [ec2_name]}
    ])

    if 'Reservations' in response:
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                ec2_ip = instance.get('PublicIpAddress')
                if ec2_ip:
                    inventory_content += (
                        f"{ec2_name} ansible_ssh_host={ec2_ip} "
                        f"ansible_ssh_private_key_file=/home/ubuntu/key/terrakey "
                        f"ansible_user=ubuntu ansible_ssh_common_args='-o " 
                        f"StrictHostKeyChecking=no' "
                        f"ansible_become=True\n"
                    )

# Menyimpan hasil ke berkas inventory
output_file = os.path.join(os.path.dirname(__file__), "ansible_inventory.ini")
with open(output_file, "w") as outfile:
    outfile.write(inventory_content)