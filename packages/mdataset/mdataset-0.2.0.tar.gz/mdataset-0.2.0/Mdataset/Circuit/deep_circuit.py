from torpy import TorClient

def get_with_tor(hostname='ifconfig.me', port=80):
    """
    Perform an HTTP GET request using Tor for anonymity.

    Parameters:
    - hostname: The target hostname (default is 'ifconfig.me').
    - port: The target port (default is 80).

    Returns:
    - The response received from the target.
    """
    with TorClient() as tor:
        # Choose random guard node and create 3-hops circuit
        with tor.create_circuit(3) as circuit:
            # Create tor stream to host
            with circuit.create_stream((hostname, port)) as stream:
                # Now we can communicate with the host
                stream.send(f'GET / HTTP/1.0\r\nHost: {hostname}\r\n\r\n'.encode())
                recv = stream.recv(1024)

    return recv.decode()

