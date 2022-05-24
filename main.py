from gettext import ngettext
from tkinter import N, Y
from turtle import ycor
from ui import GameControl, get_key
from ai import Minimax
from ml import DecisionTree
import pygame
import time
import random

if __name__ == "__main__":
   btl = input("Chon btl: so 2 hoac so 3 (Nhap: 2 hoac 3): ")
   if btl == "2":
      print("=================================================================================")
      print("|                         ^^Checkers game^^                                     |")
      print("=================================================================================")
      print("Luu y:")
      print("       - 2 che do duoi day danh den khi nao nguoi choi met khong muon dau nua")
      print("         thi dung")
      print("       - Chuong trinh gom 2 che do:")
      print("         + Ngau nhien  : do kho o muc cao nhat va khong thay doi")
      print("         + Phan cap    : do kho theo level (nguoi choi duoc chon level lan dau. ")
      print("           O cac lan ke, bot tu dong tang giam do kho theo nang luc nguoi choi  ")
      print("         + Nap data    : cung chinh la che do 2 nguoi choi. Game se luu lai nuoc")
      print("           di cua ca 2 player de su dung machine learning")
      print("================================================================================")
      t1 = input("Ban chon dau ngau nhien(Y) hay phan cap(N) hay 2 nguoi choi(2): ")
      if t1 == "Y" or t1 == "y":
         print("---------------------------------")
         print("-----------MINIMAX--------------<")
         print(">-----Che do dau ngau nhien-----<")
         print("---------------------------------")
         depth = 3
         s = False
      elif t1 == "2":
         print("---------------------------------")
         print(">--------2 nguoi choi ----------<")
         print("---------------------------------")
         depth = 0
      else:
         print("-------------------------------")
         print("------------MINIMAX-----------<")
         print(">-----Che do dau phan cap-----<")
         print("-------------------------------")
         print("Choose level: ")
         print("1: beginner")
         print("2: quite easily!")
         print("3: immediate")
         print("4...: hard")
         s = True
         depth = int(input("Your choice is: "))
      first = input("Ban (player2) co muon di truoc? (Y/N): ")
      if(first =="Y" or first =="y"):
         firstChoose = True
      else:
         firstChoose = False
      head = GameControl([150,150], 50, firstChoose)
      if depth > 0:
         player1 = Minimax(head.matrix, head.firstPlayer2)
      head.aiEllo = depth
      head.yourEllo = 0
      running = True

      while running:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
               pygame.quit()
               exit(0)
         countPlayer1, countPlayer1King, countPlayer2, countPlayer2King = head.countPlayer()
         # Nếu người chơi đầu hàng => set countPlayer2 = 0
         if head.gg == True:
            countPlayer2 = 0
         
         # Nếu 1 trong 2 bên có countPlayer = 0. Xét dừng trò chơi
         if (countPlayer1 == 0 or countPlayer2 == 0):
            if countPlayer1 == 0:
               # Đánh giá ello nếu người chơi thắng
               #pygame.display.flip()

               if depth < 5 and depth > 0:
                  if head.yourEllo <= depth:
                     head.yourEllo += 0.5
                  else: 
                     head.yourEllo += 0.2
                  if s:
                     depth += 1
                     head.aiEllo = depth
               else:
                  head.yourEllo += 1
               print("==================================================================================")
               print("==================================================================================")
               print("----------------------------------------------------------------------------------")
               print("Ban(player2) da chien thang, Dang cap hien tai cua ban la " + str(head.yourEllo))
               print("Hay nho, cac doi thu manh dang cho o phia truoc")
               print("==================================================================================")
            elif countPlayer2 == 0:
               # Đánh giá ello nếu người chơi thua
               #pygame.display.flip()
               head.gg = False
               if depth > 0:
                  if s:
                     if depth > 1:
                        depth -= 1
                        head.aiEllo = depth
                  if head.yourEllo > 0.5:
                     head.yourEllo -= 0.5
               print("===============================================")
               print("===============================================")  
               print("-----------------------------------------------")
               print("Ban(player2) da thua, hay luyen tap them!")
               print("Mot best checker se khong bao gio tu bo dam me")
               print("Dang cap cua ban la: "+ str(head.yourEllo))
               print("===============================================")
            temp = input("Ban co muon choi tiep ? (Y/N):")
            if temp == "Y" or temp == "y":
               head.firstPlayer2 = not(head.firstPlayer2)
               head.setDefaultGame()
               head.setInterfaceMatrix()
               if head.firstPlayer2:
                  head.turnPlayer2 = True
               else:
                  head.turnPlayer2 = False
               if depth > 0:
                  player1.setNode(head.matrix)
                  player1.humanFirst = head.firstPlayer2
            else:
               pygame.quit()
               exit(0)

         #switch lượt, dành cho Minimax
         if not(head.turnPlayer2) and depth > 0:
            # Tới lượt máy, đo thời gian thực thi của máy.
            if depth > 0:
               if not(head.gg):
                  executeTime = time.time() 
                  player1.countPlayer1, player1.countPlayer1King, player1.countPlayer2, player1.countPlayer2King = countPlayer1, countPlayer1King, countPlayer2, countPlayer2King
                  player1.playerTurn(1, depth)
                  executeTime = time.time() - executeTime
                  print("bot Time: ", str(executeTime))
                  head.turnPlayer2 = True
         head.display()
         pygame.display.update()
   else:
      '''
      Nhập data 
         thủ công
         tự động -> minimax 2 tg đấu 50 ván 
      đấu với máy huấn luyện:
         Người đấu máy 
         máy đấu minimax 
      '''
      print("--------------------------------------------")
      print(">-----Checkers voi Machine learning--------<")
      print("--------------------------------------------")
      dataOrfight = input("Nhap data hay dau voi bot (I/F): ")
      if dataOrfight in ["i", "I"]:
         print("Nhap thu cong hay tu dong:")
         print("1. Thu cong: ")
         print("2. Tu dong: ")
         tcOrTd = input("Your choice (1 or 2): ")
         if tcOrTd == "2":
            timeToFight = int(input("Nhap so lan chien dau: "))
            if timeToFight <= 0:
               print("Error")
               exit(0)

         running = True
         first = input("Ban (player2) co muon di truoc? (Y/N): ")
         if(first =="Y" or first =="y"):
            firstChoose = True
         else:
            firstChoose = False
         head = GameControl([150,150], 50, firstChoose)
         if tcOrTd == "2":
            player = Minimax(head.matrix, head.firstPlayer2)
            print("Luu y: trong qua trinh auto, ban ko duoc dung vao board")
            print("vi co the lam hong du lieu va crash chuong trinh")
         while running:
            if tcOrTd == "2" and timeToFight < 0:
               print("Data da sinh xong. Ket thuc chuong trinh!")
               exit(0)
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  running = False
                  pygame.quit()
                  exit(0)
            countPlayer1, countPlayer1King, countPlayer2, countPlayer2King = head.countPlayer()
            # Nếu người chơi đầu hàng => set countPlayer2 = 0
            if head.gg == True:
               countPlayer2 = 0
            
            # Nếu 1 trong 2 bên có countPlayer = 0. Xét dừng trò chơi
            if (countPlayer1 == 0 or countPlayer2 == 0):
               if head.his2 != ",":
                  head.saveTempHis()
               if tcOrTd == "2": 
                  timeToFight -= 1
               if countPlayer1 == 0:
                  print("============================")
                  print("============================")
                  print("---------------------------")
                  print("Ban(player2) da chien thang")
                  print("===========================")
                  head.history += ", player2"
               elif countPlayer2 == 0:
                  print("=====================")
                  print("=====================")  
                  print("---------------------")
                  print("Ban(player2) da thua")
                  print("====================")
                  head.history += ", player1"
               head.gg = False
               temp = "Y"
               if tcOrTd == "1":
                  temp = input("Ban co muon luu du lieu (N: No, other: Yes")
               if (temp != "N" or temp != "n"):
                  with open('dataset.txt', 'a') as f:
                     f.write(head.history)
                     f.write('\n')
               if tcOrTd == "1":
                  temp = input("Ban co muon choi tiep ? (Y/N):")
               if temp == "Y" or temp == "y":
                  head.firstPlayer2 = not(head.firstPlayer2)
                  head.setDefaultGame()
                  head.setInterfaceMatrix()
                  player.setNode(head.matrix)
                  player.humanFirst = head.firstPlayer2
                  if head.firstPlayer2:
                     head.turnPlayer2 = True
                  else:
                     head.turnPlayer2 = False
                  head.resetHis()
               else:
                  pygame.quit()
                  exit(0)
            if head.turnPlayer2 and tcOrTd == "2":
               temp = player.playerTurn(2,3)
               head.his2 += " "+str(get_key(temp[0][0])) +" " + str(get_key(temp[1][0])) 
               if not(head.firstPlayer2):
                  head.saveTempHis()
               head.turnPlayer2 = not(head.turnPlayer2)
            elif tcOrTd == "2" and not(head.turnPlayer2):
               temp = player.playerTurn(1,random.choice([1,2,3]))
               head.his2 += " "+str(get_key(temp[0][0])) +" " + str(get_key(temp[1][0])) 
               if head.firstPlayer2:
                  head.saveTempHis()
               head.turnPlayer2 = not(head.turnPlayer2)               
            head.display()
            pygame.display.update()            
      else:
         print("-----------------------------------------")
         print(">--------ML vs Person, Minimax----------<")
         print("-----------------------------------------")
         print("Co hai che do:")
         print("    1. nguoi dau voi may(machine learning): ")
         print("    2. may(machine learning) (player 2) dau may(minimax) (player1): ")
         choose = input("Nhap 1 hoac 2:")
         if choose == "2":
            print("Chon level cua bot(Minimax):")
            print("1: beginner")
            print("2: quite easily!")
            print("3: immediate")
            print("4...: hard")
            depth = int(input("Your choose: "))
            if depth < 0 or depth > 4:
               print("Error")
               exit(0)
         firstChoose = input("Ban co di truoc ? (Y/N): ")
         if firstChoose == "Y" or firstChoose == "y":
            firstChoose = True
         else:
            firstChoose = False
         running = True
         head = GameControl([150,150], 50, firstChoose)
         '''
         Lưu ý:
         - Nếu là người đấu với Machinelearning: choose = "1" và player1 (Thêm đk j tùy)
         - Nếu là machinelearning đấu với minimax: choose = "2" và
            player2 là minimax --> player2
            player1 là DecisionTree --> player1
         '''

         if choose == "1":
            player1 = Minimax(head.matrix, head.firstPlayer2)
         else:
            player2 = Minimax(head.matrix, head.firstPlayer2)
            player1 = DecisionTree()

         while running:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  running = False
                  pygame.quit()
                  exit(0)
            countPlayer1, countPlayer1King, countPlayer2, countPlayer2King = head.countPlayer()
            # Nếu người chơi đầu hàng => set countPlayer2 = 0
            if head.gg == True:
               countPlayer2 = 0
            
            # Nếu 1 trong 2 bên có countPlayer = 0. Xét dừng trò chơi
            if (countPlayer1 == 0 or countPlayer2 == 0):
               if countPlayer1 == 0:
                  # Đánh giá ello nếu người chơi thắng
                  #pygame.display.flip()
                  if choose == "2":
                     if depth < 5 and depth > 0:
                        if head.yourEllo <= depth:
                           head.yourEllo += 0.5
                        else: 
                           head.yourEllo += 0.2
                        depth += 1
                        head.aiEllo = depth
                  else:
                     head.yourEllo += 1
                  print("==================================================================================")
                  print("==================================================================================")
                  print("----------------------------------------------------------------------------------")
                  print("Ban(player2) da chien thang, Dang cap hien tai cua ban la " + str(head.yourEllo))
                  print("Hay nho, cac doi thu manh dang cho o phia truoc")
                  print("==================================================================================")
               elif countPlayer2 == 0:
                  # Đánh giá ello nếu người chơi thua
                  #pygame.display.flip()
                  head.gg = False
                  if choose == "2":
                     if depth > 0:
                        if depth > 1:
                           depth -= 1
                           head.aiEllo = depth
                     if head.yourEllo > 0.5:
                        head.yourEllo -= 0.5
                  print("===============================================")
                  print("===============================================")  
                  print("-----------------------------------------------")
                  print("Ban(player2) da thua, hay luyen tap them!")
                  print("Mot best checker se khong bao gio tu bo dam me")
                  print("Dang cap cua ban la: "+ str(head.yourEllo))
                  print("===============================================")
               temp = input("Ban co muon choi tiep ? (Y/N):")
               if temp == "Y" or temp == "y":
                  head.firstPlayer2 = not(head.firstPlayer2)
                  head.setDefaultGame()
                  head.setInterfaceMatrix()
                  if head.firstPlayer2:
                     head.turnPlayer2 = True
                  else:
                     head.turnPlayer2 = False

                  # Nạp lại ma trận cho minimax khi chuyển màn chơi (từ trắng sang đỏ và ngược lại)
                  if choose == "2":
                     if depth > 0:
                        player1.setNode(head.matrix)
                        player1.humanFirst = head.firstPlayer2
                  ## C
               else:
                  pygame.quit()
                  exit(0)

            #switch lượt, dành cho Minimax
            if head.turnPlayer2:
               # Nếu chế độ máy vs máy, player2 là minimax. 
               if choose == "2":
                  if not(head.gg):
                     player2.countPlayer1, player2.countPlayer1King, player2.countPlayer2, player2.countPlayer2King = countPlayer1, countPlayer1King, countPlayer2, countPlayer2King
                     player2.playerTurn(2, depth)
                     head.turnPlayer2 = False

            else:
               # Nếu chế độ người vs máy hoặc máy vs máy: player1 luôn là machine learning
               current, next = player1.playerTurn()
               if head.movePlayer1(current, next):
                  head.turnPlayer2 = not(head.turnPlayer2)
               else:
                  print("Di chuyen loi: ", end = '')
                  print(current, next)
            head.display()
            pygame.display.update()            


      




      