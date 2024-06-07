import socket

def udp_server():
    """A simple UDP server to receive data.
    一个简单的UDP服务器接收数据。
    """
    local_ip = "127.0.0.1"
    local_port = 12345
    buffer_size = 1024

    # Create a datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind to address and port
    sock.bind((local_ip, local_port))
    
    print("UDP server up and listening at {}:{}".format(local_ip, local_port))
    
    # Listen for incoming datagrams
    while True:
        bytes_address_pair = sock.recvfrom(buffer_size)
        message = bytes_address_pair[0]
        address = bytes_address_pair[1]

        print("Message from Client:{}".format(message))
        print("Client IP Address:{}".format(address))

if __name__ == "__main__":
    udp_server()
