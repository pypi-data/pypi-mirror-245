from torpy import TorClient
from multiprocessing.pool import ThreadPool
from torpy.http.requests import tor_requests_session

def request_tor(hostname='ifconfig.me', port=80):
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
        # Create tor stream to host
        # Now we can communicate with the host

        with tor.create_circuit(3) as circuit:
         
            with circuit.create_stream((hostname, port)) as stream:
        
                stream.send(f'GET / HTTP/1.0\r\nHost: {hostname}\r\n\r\n'.encode())
                recv = stream.recv(1024)

    return recv.decode()

def request_multiprocessing(links, num_threads=1):
    """
    Perform HTTP GET requests using Tor for multiple links in parallel.

    Parameters:
    - links: A list of target URLs to perform GET requests.
    - num_threads: The number of threads to use in the ThreadPool (default is 3).

    Returns:
    - A list of responses received from the target URLs.
    """
    with tor_requests_session() as s:
        # Use ThreadPool for parallel GET requests
        # Map the get method over the links

        with ThreadPool(num_threads) as pool:
            
            responses = pool.map(s.get, links)

    return responses
