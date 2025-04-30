import socket
import sys
import time

def read_db():
    db = {}
    db_og = []
    with open("rsdatabase.txt", 'r') as file:
        domain_ip = None
        while True:
            domain_ip = file.readline()
            if not domain_ip:
                break
            
            domain, ip = domain_ip.split(' ')
            db.update({domain.lower(): ip.strip()})
            db_og.append(domain)

    return db, db_og

def search4domain(lower_domain, db_og):
    for domain in db_og:
        if domain.lower() == lower_domain:
            return domain

    return domain

def connect2client(hostname, port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port)) # will be ran locally i.e. on localhost

    server_socket.listen(10)
    print(f"Root server running on {hostname}:{port}...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from client: {client_address}")

    return client_socket

def connect2server(hostname, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((hostname, port))
    
    return server_socket

def write2out(textfile, response):
    with open(textfile, 'a') as file:
        response = response + '\n'
        file.write(response)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Run with: python3 rs.py portno")
        exit()

    port = int(args[1])
    rs_db, rs_og = read_db()
    
    rs_domains = list(rs_db.keys()) # edu       com         github.io       something.xyz
    rs_ips = list(rs_db.values())   # ts1_ser   ts2_ser     1.2.3.4         5.6.7.8
    ts1_domain = rs_domains[0]
    ts2_domain = rs_domains[1]
    ts1_server = rs_ips[0]
    ts2_server = rs_ips[1]

    client_socket = connect2client("", port)

    while True:
        client_request = client_socket.recv(1024).decode().strip('\n')
        print(client_request.strip('\n'))

        if not client_request:
            break
        
        status, domain, identification, flag = client_request.split(" ")
        tld = domain.split('.')[-1]  # This will not return 'co.uk'
        
        if domain.lower() in rs_db.keys():
            domain_exact = search4domain(domain.lower(), rs_og)
            response = "1 " + domain_exact + " " + rs_db[domain.lower()] + " " + identification +  " aa"

            client_socket.send(response.encode())
            write2out("rsresponses.txt", response)
            continue

        if tld.lower() in rs_db.keys():
            if flag == "it":
                response = "1 " + domain + " " + rs_db[tld.lower()] + " " + identification + " ns"
                client_socket.send(response.encode())
                write2out("rsresponses.txt", response)
                continue

            if flag == "rd":
                ts_socket = connect2server(rs_db[tld.lower()], port)
                ts_socket.send(client_request.encode())
                ts_response = ts_socket.recv(1024).decode()
                
                status, domain, ip, identification, flag = ts_response.split(" ")
                ts_response = "1 " + domain + " " + ip + " " + identification
                ts_response = ts_response + " ra" if flag == "aa" else ts_response + " " + flag
                client_socket.send(ts_response.encode())
                ts_socket.close()

                write2out("rsresponses.txt", ts_response)
                continue

        if domain.lower() not in rs_db.keys() and tld.lower() not in rs_db.keys():
            response = "1 " + domain + " " + "0.0.0.0" + " " + identification + " nx"
            client_socket.send(response.encode())
            write2out("rsresponses.txt", response)
            continue

    ts1_socket = connect2server(ts1_server, port) 
    ts1_socket.send("".encode())

    ts2_socket = connect2server(ts2_server, port) 
    ts2_socket.send("".encode())
    