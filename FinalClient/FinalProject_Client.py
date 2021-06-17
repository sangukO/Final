from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *

class LotteryClient:
    client_socket = None

    def __init__(self, ip, port): #메인함수
        self.initialize_socket(ip, port)
        self.initialize_gui()
        self.listen_thread()
    
    def initialize_socket(self, ip, port): #server에 연결
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
    
    def send_chat(self):
        '''
        message를 전송하는 callback함수
        '''
        senders_name = self.name_widget.get().strip() #사용자 이름을 가져온다
        # 각 숫자들을 가져온다.
        data1 = self.enter_number1.get()+' '
        data2 = self.enter_number2.get()+' '
        data3 = self.enter_number3.get()+' '
        data4 = self.enter_number4.get()+' '
        data5 = self.enter_number5.get()+' '
        data6 = self.enter_number6.get()+' '
        data7 = self.enter_number7.get().strip()

        data_num = (data1+data2+data3+data4+data5+data6+data7)

        send_to_server_message = (senders_name+' '+data_num).encode('utf-8') #전체 숫자 데이터를 인코딩화

        self.chat_transcript_area.yview(END)
        self.client_socket.send(send_to_server_message) 
        return 'break'

    def initialize_gui(self):
        '''
        위젯을 배치하고 초기화한다.
        '''
        self.root = Tk()
        fr = []
        for i in range(0, 5):
            fr.append(Frame(self.root))
            fr[i].pack(fill=BOTH)
        
        self.name_label = Label(fr[0], text='사용자 이름')
        self.recv_label = Label(fr[1], text='복권 추첨 서버 메시지')
        self.send_label = Label(fr[3], text='복권 번호 입력')
        self.send_btn = Button(fr[3], text='전송', command=self.send_chat)
        self.chat_transcript_area = ScrolledText(fr[2], height=20, width=60)
        self.name_widget = Entry(fr[0], width=15)
        
        self.enter_number1 = Entry(fr[4], width=5)
        self.enter_number2 = Entry(fr[4], width=5)
        self.enter_number3 = Entry(fr[4], width=5)
        self.enter_number4 = Entry(fr[4], width=5)
        self.enter_number5 = Entry(fr[4], width=5)
        self.enter_number6 = Entry(fr[4], width=5)
        self.number7th_label = Label(fr[4], text='보너스 번호')
        self.enter_number7 = Entry(fr[4], width=5)
 
        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2, pady=2)
        self.send_label.pack(side=LEFT)
        
        self.enter_number1.pack(side=LEFT, padx=2, pady=2)
        self.enter_number2.pack(side=LEFT, padx=2, pady=2)
        self.enter_number3.pack(side=LEFT, padx=2, pady=2)
        self.enter_number4.pack(side=LEFT, padx=2, pady=2)
        self.enter_number5.pack(side=LEFT, padx=2, pady=2)
        self.enter_number6.pack(side=LEFT, padx=2, pady=2)
        self.number7th_label.pack(side=LEFT)
        self.enter_number7.pack(side=LEFT, padx=2, pady=2)

    def listen_thread(self):
        '''
        Thread를 생성하고 시작한다
        '''
        
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()
        
    def receive_message(self, so):
        '''
        서버로부터 메시지를 수신하고 문서창에 표시한다
        '''
        
        while True:
            buf = so.recv(1024) #등수 출력 문자열이 길어 1024로 설정
            if not buf:
                break
            self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
        so.close()
    

if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip =='':
        ip = '127.0.0.1'
    port = 2500
    LotteryClient(ip,port)
    mainloop()
