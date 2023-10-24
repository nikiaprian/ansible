import boto3
import json

# Inisialisasi klien EC2 AWS
ec2 = boto3.client('ec2', region_name='us-west-2')  # Ganti dengan wilayah yang sesuai

# Tentukan nama-nama instance EC2 yang ingin Anda cari
manual_ec2_names = ["docker01", "docker02"]

dynamic_inventory = {}

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
                    dynamic_inventory[ec2_name] = {
                        "ansible_ssh_host": ec2_ip,
                        "ansible_ssh_user": "ubuntu",  # Sesuaikan dengan pengguna SSH yang sesuai
                        "ansible_become": True,  # Jika Anda memerlukan hak istimewa root/superuser
                        "ansible_become_password": "gameover213",  # Sesuaikan dengan kata sandi yang sesuai
                        "ansible_ssh_common_args": "-o StrictHostKeyChecking=no",
                        "ansible_user": "ubuntu"  # Set ansible_user to the desired SSH user
                        #"ansible_groups": "docker"  # Add the group "docker" to the hosts
                    }

print(json.dumps(dynamic_inventory))