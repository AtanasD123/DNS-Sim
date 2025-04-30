import socket
import time
import sys

identification = 1

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
  if len(args) < 3:
    print("Run with: python3 rs.py portno hostaddress")
    exit()
  
  port = int(args[1])
  host = args[2]
  root_server = connect2server(host, port)
  #root_server = connect2server("java.cs.rutgers.edu", port)

  with open('hostnames.txt', 'r') as file:
    while True:

      hostname = file.readline().strip('\n')
      if not hostname:
          break

      domain, flag = hostname.split(' ')
      request = '0 ' + domain + " " + str(identification) + " " + flag
      root_server.send(request.encode())
      response = root_server.recv(1024).decode()

      print(response)
      status, domain, ip, identification_string, flag = response.split(" ")
      write2out("resolved.txt", response)

      if flag == "ns":
        identification += 1
        request = '0 ' + domain + " " + str(identification) + " " + flag
        ts_socket = connect2server(ip, port)
        ts_socket.send(request.encode())
        ts_response = ts_socket.recv(1024).decode()
        print(ts_response)
        write2out("resolved.txt", ts_response)

      identification +=1

