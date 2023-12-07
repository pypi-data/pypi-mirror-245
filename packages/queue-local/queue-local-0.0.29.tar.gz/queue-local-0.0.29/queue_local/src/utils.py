import socket
import threading


def get_ipv4():
    # Get the local machine's IPv4 and IPv6 addresses
    try:
        ipv4_address = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        ipv4_address = None
        print("Error getting IPv4 address " + str(e))
    return ipv4_address


def get_ipv6():
    try:
        ipv6_address = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]
    except Exception as e:
        ipv6_address = None
        print("Error getting IPv6 address " + str(e))
    return ipv6_address


def get_thread_id():
    # Get the current thread ID
    return threading.current_thread().ident


# Example usage
if __name__ == "__main__":
    # Get and print the IPv4 and IPv6 addresses
    ipv4_address = get_ipv4()
    ipv6_address = get_ipv6()
    print(f"IPv4 Address: {ipv4_address}")
    print(f"IPv6 Address: {ipv6_address}")

    # Get and print the thread ID
    thread_id = get_thread_id()
    print(f"Thread ID: {thread_id}")
