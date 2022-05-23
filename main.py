from ui import GameControl
from ai import Minimax
import pygame
import time
if __name__ == "__main__":
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
      bot = Minimax(head.matrix, head.firstPlayer2)
   head.aiEllo = depth
   head.yourEllo = 0
   running = True

   while running:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running ==False
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
               bot.setNode(head.matrix)
               bot.humanFirst = head.firstPlayer2
         else:
            pygame.quit()
            exit(0)
      
      #switch lượt, dành cho Minimax
      if not(head.turnPlayer2) and depth > 0:
         # Tới lượt máy, đo thời gian thực thi của máy.
         if depth > 0:
            if not(head.gg):
               executeTime = time.time() 
               bot.countPlayer1, bot.countPlayer1King, bot.countPlayer2, bot.countPlayer2King = countPlayer1, countPlayer1King, countPlayer2, countPlayer2King
               bot.botTurn(depth)
               executeTime = time.time() - executeTime
               print("bot Time: ", str(executeTime))
               head.turnPlayer2 = True
      head.display()
      pygame.display.update()





      