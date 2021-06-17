from socket import *
from threading import *
import random # 랜덤 모듈

class LotteryServer:
    clients = []
    final_received_message = ""
    senders_num = 0
    draw_num = 5
    lot1 = []
    lot2 = []
    lot3 = []
    lot4 = []
    lot5 = []
    lots = []
    message = ""
    lot_score = ['0', '0', '0', '0', '0']
    

    def __init__(self): #메인 함수
        self.s_sock = socket(AF_INET, SOCK_STREAM) #소켓 생성
        self.ip = ''
        self.port = 2500
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("Waiting for clients...")
        self.s_sock.listen(100)
        self.accept_client()
    
    def accept_client(self): #클라이언트와 연결
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)
            self.senders_num += 1
            print (self.senders_num,'번째 클라이언트, ',ip, ' : ', str(port), '가 연결되었습니다.')
            t = Thread(target=self.receive_messages, args=(c_socket,)) #쓰레드 생성
            t.start()
            

    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = c_socket.recv(1024)
                if not incoming_message:
                    break
            except:
                continue
            else: #클라이언트가 보낸 데이터를 받아서 각 변수에 삽입
                self.final_received_message = incoming_message.decode('utf-8')
                sender = self.final_received_message.split()[0]
                num1 = self.final_received_message.split()[1]
                num2 = self.final_received_message.split()[2]
                num3 = self.final_received_message.split()[3]
                num4 = self.final_received_message.split()[4]
                num5 = self.final_received_message.split()[5]
                num6 = self.final_received_message.split()[6]
                num7 = self.final_received_message.split()[7]
                
                self.final_received_message = (sender+"이(가) 선택한 번호 : {0} {1} {2} {3} {4} {5} {6}\n".format(num1, num2, num3, num4, num5, num6, num7))
                if self.draw_num == 1:
                    self.lot1.append(sender)         
                    self.lot1.append(num1)         
                    self.lot1.append(num2)         
                    self.lot1.append(num3)         
                    self.lot1.append(num4)         
                    self.lot1.append(num5)         
                    self.lot1.append(num6)         
                    self.lot1.append(num7)         
                    print(self.lot1)
                if self.draw_num == 2:
                    self.lot2.append(sender)         
                    self.lot2.append(num1)         
                    self.lot2.append(num2)         
                    self.lot2.append(num3)         
                    self.lot2.append(num4)         
                    self.lot2.append(num5)         
                    self.lot2.append(num6)         
                    self.lot2.append(num7)         
                    print(self.lot2)
                if self.draw_num == 3:
                    self.lot3.append(sender)         
                    self.lot3.append(num1)         
                    self.lot3.append(num2)         
                    self.lot3.append(num3)         
                    self.lot3.append(num4)         
                    self.lot3.append(num5)         
                    self.lot3.append(num6)         
                    self.lot3.append(num7)         
                    print(self.lot3)
                if self.draw_num == 4:
                    self.lot4.append(sender)         
                    self.lot4.append(num1)         
                    self.lot4.append(num2)         
                    self.lot4.append(num3)         
                    self.lot4.append(num4)         
                    self.lot4.append(num5)         
                    self.lot4.append(num6)         
                    self.lot4.append(num7)         
                    print(self.lot4)
                if self.draw_num == 5:
                    self.lot5.append(sender)         
                    self.lot5.append(num1)         
                    self.lot5.append(num2)         
                    self.lot5.append(num3)         
                    self.lot5.append(num4)         
                    self.lot5.append(num5)         
                    self.lot5.append(num6)         
                    self.lot5.append(num7)         
                    print(self.lot5)
                self.send_all_clients(self.final_received_message)
                self.draw_num -= 1
                
                if self.draw_num != 0: #복권 수가 남았을 경우
                    self.final_received_message = ('추첨까지 남은 복권 : '+str(self.draw_num)+'개\n')
                    self.send_all_clients(self.final_received_message)
                
                else: #복권 수가 남지 않았을 경우
                    self.final_received_message = ('복권 추첨을 시작합니다!\n\n')
                    self.send_all_clients(self.final_received_message)
                    self.drawing_of_Lots(c_socket)
                
        c_socket.close()
    
    def send_all_clients(self, senders_socket): #서버에게 보내는 메시지
        for client in self.clients:
            socket, (ip, port) = client
            if socket is not senders_socket:
                try:
                    socket.sendall(self.final_received_message.encode('utf-8'))
                except:
                    pass

    def drawing_of_Lots(self, senders_socket): #복권 추첨
        win_number_list = []
        win_number = 0

        self.lots.append(self.lot1)
        self.lots.append(self.lot2)
        self.lots.append(self.lot3)
        self.lots.append(self.lot4)
        self.lots.append(self.lot5) 
   
        for i in range(0, 7):
            while True:
                win_number = random.randrange(1,46) #랜덤 모듈 이용
                if win_number not in win_number_list:
                    break
            win_number_list.append(win_number)  

        for i in range(0, 7): #이중 for문을 이용하여 해당 숫자가 있을 경우 win 문자 삽입
            for j in range(0, 5):
                if str(win_number_list[i]) not in self.lots[j]:
                    pass
                else:
                    self.lots[j].append('win')
                
        self.final_received_message = ('당첨 번호는 ') #당첨 번호 출력
        for i in range(0, 7):
            self.final_received_message += str(win_number_list[i])+' '
        self.final_received_message += ('입니다!\n')
        self.send_all_clients(self.final_received_message)

        #복권의 값에 맞은 개수 삽입
        for i in range(0, 5):
            if self.lots[i].count('win') >= 6:
                self.lot_score[i] = '6'
                continue         
 
            elif self.lots[i].count('win') == 5:
                self.lot_score[i] = '5'
                continue         

            elif self.lots[i].count('win') == 4:        
                self.lot_score[i] = '4'
                continue
                
            elif self.lots[i].count('win') == 3:
                self.lot_score[i] = '3'
                continue

            elif self.lots[i].count('win') == 2:
                self.lot_score[i] = '2'         
                continue

        #이중 for문으로 등수 출력
        for i in range(0, 5):
            for j in range(2, 7):
                if self.lot_score[i] == str(j):
                    msg = ""
                    if(i == 2):
                        msg = '5개의 복권 중 '+self.lots[i][0]+'님이 선택하신 '+str(5-i)+'번째 복권이 '+str(j)+'개를 맞혀 '
                        msg += '5등에 당첨되셨습니다!\n'
                    if(i == 3):
                        msg = '5개의 복권 중 '+self.lots[i][0]+'님이 선택하신 '+str(5-i)+'번째 복권이 '+str(j)+'개를 맞혀 '
                        msg += '4등에 당첨되셨습니다!\n'
                    if(i == 4):
                        msg = '5개의 복권 중 '+self.lots[i][0]+'님이 선택하신 '+str(5-i)+'번째 복권이 '+str(j)+'개를 맞혀 '
                        msg += '3등에 당첨되셨습니다!\n'
                    if(i == 5):
                        msg = '5개의 복권 중 '+self.lots[i][0]+'님이 선택하신 '+str(5-i)+'번째 복권이 '+str(j)+'개를 맞혀 '
                        msg += '2등에 당첨되셨습니다!\n'
                    if(i >= 6):
                        msg = '5개의 복권 중 '+self.lots[i][0]+'님이 선택하신 '+str(5-i)+'번째 복권이 '+str(j)+'개를 맞혀 '
                        msg += '1등에 당첨되셨습니다!\n'
                    self.final_received_message = msg
                    self.send_all_clients(self.final_received_message)         
                
                

if __name__ == "__main__":
    LotteryServer()
