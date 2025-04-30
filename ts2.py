import socket
import sys

def read_db():
    db = {}
    db_og = []
    with open("ts2database.txt", 'r') as file:
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
        
def run_ts2_server(hostname, port, ts2_db, ts2_og):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))

    while True:

        server_socket.listen(10)
        print(f"TS2 server running on {hostname}:{port}...")
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        request = connection.recv(1024).decode()

        if request:
            print(request)
            status, domain, identification, flag = request.split(" ")
            response = ""

            if domain.lower() in ts2_db:
                domain_exact = search4domain(domain.lower(), ts2_og)
                response = "1 " + domain_exact + " " + ts2_db[domain.lower()] + " " + identification + " aa"
                connection.send(response.encode())

            if domain.lower() not in ts2_db:
                response = "1 " + domain.lower() + " " + "0.0.0.0" + " " + identification + " nx"
                connection.send(response.encode())

            write2out("ts2responses.txt", response)

        else:
            connection.close()
            exit()

if __name__ == "__main__":
    args = sys.argv
    port = int(args[1])
    if len(args) < 2:
        print("Run with: python3 ts2.py portno")
        exit()
    ts2_db, ts2_og = read_db()
    run_ts2_server("", port, ts2_db, ts2_og)
