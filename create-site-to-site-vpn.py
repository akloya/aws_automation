import boto3
import sys
import xml.etree.ElementTree as ET

client = boto3.client('ec2')

# VALUES WHICH WE NEED FROM CUSTOMER
customer_name = "ABC Inc."
customer_vpn_gateway_ip = "X.Y.Z.A"
project = "APP"
customer_host_ips=["x.y.z.a/32","a.b.c.d/32"]

# DO NOT EDIT ANY THING BELOW THIS LINE WITH OUT AJAYA's APPROVAL.
vgw_id = ''
vpc_id = ''




def create_tags(resource_id):
    response = client.create_tags(
        Resources=[resource_id],
        Tags=[
            {
                'Key': 'Name',
                'Value': customer_name + "-CG"
            },
            {
                'Key': 'Environment',
                'Value': "VPN"
            },
            {
                'Key': 'Application-Group',
                'Value': project
            }
        ]
    )
    return response


def create_customer_gateway(customer_gateway_ip):
    response = client.create_customer_gateway(
        BgpAsn=65000,
        PublicIp=customer_gateway_ip,
        Type='ipsec.1'
    )
    return response


def create_site_to_site_vpn(customer_gateway_id):
    vpn_connection = client.create_vpn_connection(
        CustomerGatewayId=customer_gateway_id,
        Type="ipsec.1",
        VpnGatewayId=vgw_id,
        Options={
            'StaticRoutesOnly': True
        }
    )
    print(vpn_connection)
    vpn_xml = vpn_connection['VpnConnection']['CustomerGatewayConfiguration']
    root = ET.fromstring(vpn_xml)
    return root.attrib

def create_vpn_connection_static_routes(vpn_connection_id,dest_cidr_block):
    response = client.create_vpn_connection_route(
        DestinationCidrBlock=dest_cidr_block,
        VpnConnectionId=vpn_connection_id
    )
    return response

def create_virtual_gateway():
    print("code to create virtual gateway will be adding for now i am hardcoding the value"
    return "True"

if vpc_id == "":
    print("NO VPC ID HARDCODED")
    sys.exit(1)


if vgw_id == "":
    print("NO VIRTUAL GATEWAY ID HARDCODED SO GENERATING A VIRTUAL GATEWAY")
    create_virtual_gateway()

# Create Customer Gateway
customer_gateway_response = create_customer_gateway(customer_vpn_gateway_ip)
print(customer_gateway_response)

# Add tags to Customer Gateway
tag_response = create_tags(customer_gateway_response['CustomerGateway']['CustomerGatewayId'])
print(tag_response)

# Create Site to Site VPN Connection
vpn_connection_id=create_site_to_site_vpn(customer_gateway_response['CustomerGateway']['CustomerGatewayId'])
print(vpn_connection_id)

# Add tags to Site to Site VPN Connection
tag_response = create_tags(vpn_connection_id['id'])
print(tag_response)

# Add static routes to created VPN Connection (Adding Gateway IP useful for PING and initial setup testing with client

print(create_vpn_connection_static_routes(vpn_connection_id['id'], customer_vpn_gateway_ip + "/32"))

# Adding Customer Host IPs

for i in customer_host_ips:
    print(create_vpn_connection_static_routes(vpn_connection_id['id'], i))

