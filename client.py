import socket

def Start():
        HOST = "localhost"
        PORT = 9998

        mySocket = socket.socket()
        mySocket.connect((HOST,PORT))
        print("\nCONNECTED TO {}:{}...\n".format(HOST,PORT))
        CONENCTED=True
        while CONENCTED:
                menu_str="Python DB Menu\n1. Find customer\n2. Add customer\n3. Delete customer\n4. Update customer age\n5. Update customer address\n6. Update customer phone\n7. Print report\n8. Exit\nSelect:"
                print(menu_str)
                message = str(input(" -> ").strip())
                if message=="1":
                        customer_name=str(input("Enter customer name:").strip())
                        if customer_name=='':
                                print("Invalid name")
                                print("#"*80)
                                continue
                        message="find$"+customer_name
                        mySocket.send(message.strip().encode())
                elif message=="2":
                        customer_name=str(input("Enter customer name:").strip())
                        customer_age=str(input("Enter customer age:").strip())
                        customer_address=str(input("Enter customer address:").strip())
                        customer_phone=str(input("Enter customer phone#:").strip())
                        if customer_name=='':
                                print("Invalid details")
                                print("#"*80)
                                continue
                        if customer_age!='' and not customer_age.replace(' ','').replace('-','').isdigit():
                                print("Invalid age")
                                print("#"*80)
                                continue
                        if customer_phone!='' and not customer_phone.replace(' ','').replace('-','').isdigit():
                                print("Invalid phone#")
                                print("#"*80)
                                continue
                        message="add${}${}${}${}".format(customer_name,customer_age or '%',customer_address or '%',customer_phone or '%')
                        mySocket.send(message.encode())
                elif message=="3":
                        customer_name=str(input("Enter customer name to delete:").strip())
                        if customer_name=='':
                                print("Invalid details")
                                print("#"*80)
                                continue
                        message="delete${}".format(customer_name)
                        mySocket.send(message.strip().encode())
                elif message=="4":
                        customer_name=str(input("Enter customer name to update age:").strip())
                        customer_updated_age=str(input("Enter updated age:").strip())
                        if customer_name=='' or customer_updated_age=='' or not customer_updated_age.replace(' ','').replace('-','').isdigit():
                                print("Invalid details")
                                print("#"*80)
                                continue
                        message="age${}${}".format(customer_name,customer_updated_age)
                        mySocket.send(message.strip().encode())
                elif message=="5":
                        customer_name=str(input("Enter customer name to update address:").strip())
                        customer_updated_address=str(input("Enter updated address:").strip())
                        if customer_name=='' or customer_updated_address=='':
                                print("Invalid details")
                                print("#"*80)
                                continue
                        message="address${}${}".format(customer_name,customer_updated_address)
                        mySocket.send(message.strip().encode())
                elif message=="6":
                        customer_name=str(input("Enter customer name to update phone:").strip())
                        customer_updated_phone=str(input("Enter updated phone:").strip())
                        if customer_name=='' or customer_updated_phone=='' or not customer_updated_phone.replace(' ','').replace('-','').isdigit():
                                print("Invalid details")
                                print("#"*80)
                                continue
                        message="phone${}${}".format(customer_name,customer_updated_phone)
                        mySocket.send(message.strip().encode())
                elif message=="7":
                        message="print"
                        mySocket.send(message.strip().encode())
                elif message=="8":
                        #CONENCTED=False
                        message="Good bye"
                        print(message)
                        mySocket.send(message.strip().encode())
                        break
                else:
                        print("Invalid option")
                        print("#"*80)
                        continue
                server_msg = mySocket.recv(5000).decode()
                print ("Server:\n" + server_msg)
                print("#"*80)
                print()
        mySocket.close()

if __name__ == '__main__':
    Start()
    exit(code=0)