import socket
import sys

def read_db():
    db = {}
    db_og = []
    with open("ts1database.txt", 'r') as file:
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

def write2out(textfile, response):
    with open(textfile, 'a') as file:
        response = response + '\n'
        file.write(response)
        
def run_ts1_server(hostname, port, ts1_db, ts1_og):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))

    while True:

        server_socket.listen(10)
        print(f"TS1 server running on {hostname}:{port}...")
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        request = connection.recv(1024).decode()

        if request:
            print(request)
            status, domain, identification, flag = request.split(" ")
            response = None

            if domain.lower() in ts1_db:
                domain_exact = search4domain(domain.lower(), ts1_og)
                response = "1 " + domain_exact + " " + ts1_db[domain.lower()] + " " + identification + " aa"
                connection.send(response.encode())

            if domain.lower() not in ts1_db:
                response = "1 " + domain + " " + "0.0.0.0" + " " + identification + " nx"
                connection.send(response.encode())

            write2out("ts1responses.txt", response)

        else:
            connection.close()
            exit()

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Run with: python3 ts1.py portno")
        exit()
    port = int(args[1])
    ts1_db, ts1_og = read_db()
    run_ts1_server("", port, ts1_db, ts1_og) 