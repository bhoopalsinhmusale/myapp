#import socket
import  os
import socketserver

def load_database(database_name):
    
    records = {}
    with open(database_name) as file:
        for line in file:
            if(line.strip().split('|')[0]==''):
                continue
            key= line.strip().split('|')[0]
            print("{}:{}".format(key,line.strip().split('|')[1:] or ''))
            values=[i or '' for i in line.strip().split('|')[1:]]  
            records[key] = values
    return records

class Server(socketserver.BaseRequestHandler):
    
    def handle(self):
        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(5000).decode().strip()
            print("{}:{}".format(self.client_address[0],self.data))
            if str(self.data).strip()=="Good bye" or str(self.data).strip()=="":
                break
            #print ("Client:" + str(self.data))
            server_response=server_send(self.data)
            # just send back the same data, but upper-cased
            self.request.sendall(bytes(server_response + "\n", "utf-8"))
    
def server_send(client_msg):
    client_msg=str(client_msg)
    server_msg="Good bye"
    if client_msg.startswith("find$"):
        server_msg=str(find_customer(client_msg.split('$')[1].title()))
    elif client_msg.startswith("add$"):
        server_msg=str(add_customer(client_msg))
    elif client_msg.startswith("delete$"):
        server_msg=str(delete_customer(client_msg.strip()))
    elif client_msg.startswith("age$"):
        server_msg=str(update_customer_age(client_msg.strip()))
    elif client_msg.startswith("address$"):
        server_msg=str(update_customer_address(client_msg.strip()))
    elif client_msg.startswith("phone$"):
        server_msg=str(update_customer_phone(client_msg.strip()))
    elif client_msg.startswith("print"):
        server_msg=str(print_report())
    return server_msg#self.request.sendall(server_msg.strip().encode())#conn.send(server_msg.strip().encode())

def find_customer(customer_name):
    if records.get(customer_name,0)==0:
        return str("Customer not found")
    server_response=str('-'*70)+"\n"
    server_response+=("| {:<15} | {:<8} | {:<25} | {:<10}\n".format('Name','Age','Address','Phone#'))
    server_response+=str('-'*70)+"\n"
    server_response+=str("| {:<15} | {:<8} | {:<25} | {:<10}\n".format(customer_name,records[customer_name][0],records[customer_name][1],records[customer_name][2]))

    return str(server_response)


def add_customer(client_msg):
    customer_name=str(client_msg.strip().split('$')[1]).title()
    print(customer_name)
    #new_record={}
    if records.get(customer_name.title(),0)!=0:
        return str("{} Already exist".format(customer_name))
    details_list=list()
    for i in client_msg.strip().split('$')[2:]:
        if i=='%':
            details_list.append('')
            continue    
        #print("l{i}".format(str(i)))
        details_list.append(str(i))
    records[customer_name]=details_list
    #unload_data()
    return str("{}:{}\nAdded!".format(customer_name.title(),records.get(customer_name.title())))

def delete_customer(customer_name):

    if records.get(str(customer_name.strip().split('$')[1]).title(),0)==0:
        return str("{} Customer does not exist".format(str(customer_name.strip().split('$')[1]).title()))
    records.pop(str(customer_name.strip().split('$')[1]).title())
    #unload_data()
    return str(str(customer_name.strip().split('$')[1]).title()+" deleted")   

def update_customer_age(client_msg):
    customer_name=str(client_msg.strip().split('$')[1]).title()
    updated_age=str(client_msg.strip().split('$')[2])
    if records.get(customer_name,0)==0:
        return str("{} Customer does not exist".format(customer_name))
    records[customer_name][0]=updated_age
    #unload_data()
    return str("{} age updated {}".format(customer_name,str(records[customer_name])))

def update_customer_address(client_msg):
    customer_name=str(client_msg.strip().split('$')[1]).title()
    updated_address=str(client_msg.strip().split('$')[2])
    if records.get(customer_name,0)==0:
        return str("{} Customer does not exist".format(customer_name))
    records[customer_name][1]=updated_address
    #unload_data()
    return str("{} address updated {}".format(customer_name,str(records[customer_name])))

def update_customer_phone(client_msg):
    customer_name=str(client_msg.strip().split('$')[1]).title()
    updated_phone=str(client_msg.strip().split('$')[2])
    if records.get(customer_name,0)==0:
        return str("{} Customer does not exist".format(customer_name))
    records[customer_name][2]=updated_phone
    #unload_data()
    return str("{} phone updated {}".format(customer_name,str(records[customer_name])))

def print_report():
    '''with open(database_name) as file:
        for line in file:
            if(line.strip().split('|')[0]==''):
                continue
            key= line.strip().split('|')[0]
            print("{}:{}".format(key,line.strip().split('|')[1:]))
            values=[i for i in line.strip().split('|')[1:]]  
            records[key] = values'''
    print('-'*70)
    server_response=str('-'*70)+"\n"

    print("| {:<15} | {:<8} | {:<25} | {:<10}".format('Name','Age','Address','Phone#'))
    server_response+=("| {:<15} | {:<8} | {:<25} | {:<10}\n".format('Name','Age','Address','Phone#'))
    for k, v in records.items():
        print('-'*70)
        server_response+=str('-'*70)+"\n"
        print("| {:<15} | {:<8} | {:<25} | {:<10}".format(k,v[0] if len(v) > 0 else '' ,v[1] if len(v) > 1 else '' ,v[2] if len(v) > 2 else '' ))
        server_response+=str("| {:<15} | {:<8} | {:<25} | {:<10}\n".format(k,v[0] if len(v) > 0 else '' ,v[1] if len(v) > 1 else '' ,v[2] if len(v) > 2 else '' ))
    return str(server_response)

def unload_data():
    f= open(database_name,"w")
    for k,v in records.items():
        f.write(str(k+"|"+v[0]+"|"+v[1]+"|"+v[2]+"\n"))
    f.close()

if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 9999
    database_name=os.path.dirname(__file__)+"/data.txt"
    
    with socketserver.TCPServer((HOST, PORT), Server) as server:
    
        records=load_database(database_name)
        print("\n{} records loaded in memory".format(len(records)))
        print("\nSERVER RUNNING...")
        server.serve_forever()
