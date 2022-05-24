import string
from rule import *
from data import data

''''
player = True: lấy max
player = False: lấy min
heuristics = số quân cờ còn lại(player1) - số quân cờ con lại(player2)
'''
class Node:
   def __init__(self, player: bool, playerFirst: bool, path) -> None:
      '''
      self.child: là danh sách các node kế lưu trữ dựa trên [currentPos,nextPos]
      '''
      self.child = []
      self.path = path
      self.player = player
      self.playerFirst = playerFirst
   def generate(self, matrix):
      '''
      sinh ra tất cả các node dưới dạng [currentPos, nextPost] trong child
      '''
      if self.player:
         for i in range(8):
            for j in range(8):
               temp = showsuggestPlayer1([i,j], matrix, self.playerFirst)
               if len(temp) != 0:
                  for item in temp:
                     self.child.append([[i,j],item])
      else:
         for i in range(8):
            for j in range(8):
               temp = showsuggestPlayer2([i,j], matrix, self.playerFirst)
               if len(temp) != 0:
                  for item in temp:
                     self.child.append([[i,j], item])




class Minimax: 
   def __init__(self, matrix, humanFirst: bool) -> None:
      self.root = None
      self.setNode(matrix)
      self.humanFirst = humanFirst
      self.countPlayer1 = 12
      self.countPlayer2 = 12
      self.countPlayer1King = 0
      self.countPlayer2King = 0
   def setNode(self, matrix):
      self.root = matrix
      self.countPlayer1 = 12
      self.countPlayer2 = 12
      self.countPlayer1King = 0
      self.countPlayer2King = 0
      

   def minimax(self,node: Node, depth, maximizingPlayer: bool)->list:
      '''
      minimax algorithm
      Giải thuật duyệt các node la ik lên, có lưu các bước để có thể quay
      về trạng thái trước.
      '''
      node.generate(self.root)
      if len(node.child) == 0 or depth == 0:
         return self.value(), node.path
      Mx = 0
      if maximizingPlayer:
         Mx = -99
         bestNext = []
         for item in node.child:
            countPlayer1 = self.countPlayer1
            countPlayer2 = self.countPlayer2
            prePath = self.getNext(item[0], item[1], node.player)
            NewMx, next = self.minimax(Node(not(node.player),not(node.playerFirst), item),depth - 1, not(maximizingPlayer))
            self.getBack(prePath)
            self.countPlayer1 = countPlayer1
            self.countPlayer2 = countPlayer2
            
            if NewMx > Mx: 
               Mx = NewMx
               bestNext = item     
      else:
         Mx = 99
         bestNext = []
         for item in node.child:
            countPlayer1 = self.countPlayer1
            countPlayer2 = self.countPlayer2
            prePath = self.getNext(item[0], item[1], node.player)
            NewMx, next = self.minimax(Node(not(node.player),not(node.playerFirst), item), depth - 1, not(maximizingPlayer))
            self.countPlayer1 = countPlayer1
            self.countPlayer2 = countPlayer2           
            self.getBack(prePath)
            if NewMx < Mx:
               Mx = NewMx
               bestNext = item
      return Mx, bestNext
   def playerTurn(self, numPlayer, depth):
      '''
      Lượt của máy, gọi hàm này
      '''
      if self.countPlayer1 == 0 or self.countPlayer2 == 0:
         return
      
      if numPlayer == 1:
         temp = Node(True,not(self.humanFirst), [])
         Mx, bestNext = self.minimax(temp, depth, True)
         return self.getNext(bestNext[0], bestNext[1], True)
      temp = Node(False,self.humanFirst, [])
      Mx, bestNext = self.minimax(temp, depth, False)  
      return self.getNext(bestNext[0], bestNext[1], False)


   
   def getNext(self, currentPos, nextPos, player)->list:
      '''
      Ma trận đi đến vị trí kế tiếp, trả về danh sách các vị trí đã thay đổi
      '''
      prePath = []
      if self.root[nextPos[0]][nextPos[1]] == 0:
         # Nếu ô kế tiếp là ô trống
         prePath.append([currentPos, self.root[currentPos[0]][currentPos[1]]])
         prePath.append([nextPos, 0])
         self.root[nextPos[0]][nextPos[1]] = self.root[currentPos[0]][currentPos[1]]
         self.root[currentPos[0]][currentPos[1]] = 0
         if nextPos[0] == 7:
            if self.root[nextPos[0]][nextPos[1]] == 2:
               self.root[nextPos[0]][nextPos[1]] = 4
            elif self.root[nextPos[0]][nextPos[1]] == 1:
               self.root[nextPos[0]][nextPos[1]] = 3
            self.countPlayer1King += 1
         elif nextPos[0] == 0:
            if self.root[nextPos[0]][nextPos[1]] == 2:
               self.root[nextPos[0]][nextPos[1]] = 4
            elif self.root[nextPos[0]][nextPos[1]] == 1:
               self.root[nextPos[0]][nextPos[1]] = 3      
            self.countPlayer2King += 1      
      else:
         if player:
            # Đến lượt player1, ăn được quân
            flag = True
            while flag:
               self.countPlayer2 -= 1

               prePath.append([currentPos,self.root[currentPos[0]][currentPos[1]]])
               prePath.append([nextPos, self.root[nextPos[0]][nextPos[1]]])
               if nextPos[0] - currentPos[0] == 1:
                  if nextPos[1] - currentPos[1] == 1:
                     # Ô phía dưới bên phải ăn được
                     prePath.append([[nextPos[0] + 1, nextPos[1] + 1], 0])
                     self.root[nextPos[0] + 1][nextPos[1] + 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0

                     currentPos = [nextPos[0] + 1, nextPos[1] + 1]
                     nextPos = None
                  elif nextPos[1] + 1 == currentPos[1]:
                     # Ô phía dưới bên trái ăn được
                     prePath.append([[nextPos[0] + 1, nextPos[1] - 1], 0])
                     self.root[nextPos[0] + 1][nextPos[1] - 1] = self.root[currentPos[0]][currentPos[1]]
                     
                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0

                     currentPos = [nextPos[0] + 1, nextPos[1] - 1]
                     nextPos = None                        
               elif nextPos[0] + 1 == currentPos[0]:
                  if nextPos[1] - currentPos[1] == 1:
                     # Ô phía trên bên phải ăn được
                     prePath.append([[nextPos[0] - 1, nextPos[1] + 1], 0])
                     self.root[nextPos[0] - 1][nextPos[1] + 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] - 1, nextPos[1] + 1]
                     nextPos = None
                  elif nextPos[1] + 1 == currentPos[1]:
                     # Ô phía dưới bên phải ăn được
                     prePath.append([[nextPos[0] - 1, nextPos[1] - 1], 0])
                     self.root[nextPos[0] - 1][nextPos[1] - 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] - 1, nextPos[1] - 1]
                     nextPos = None
               # Phong hậu
               if currentPos[0] == 7:
                  if self.root[currentPos[0]][currentPos[1]] == 2:
                     self.root[currentPos[0]][currentPos[1]] = 4
                  elif self.root[currentPos[0]][currentPos[1]] == 1:
                     self.root[currentPos[0]][currentPos[1]] = 3
                  self.countPlayer1King += 1
               # kiểm tra xem có thể ăn tiếp được không
               temp = showsuggestPlayer1(currentPos, self.root, not(self.humanFirst))
               if len(temp) == 0:
                  flag = False
               else:
                  for item in temp:
                     if self.root[item[0]][item[1]] != 0:
                        nextPos = item
                        break
                  if nextPos == None:
                     flag = False
         else:
            # Nếu là lượt player2
            flag = True
            while flag:
               self.countPlayer1 -= 1

               prePath.append([currentPos,self.root[currentPos[0]][currentPos[1]]])
               prePath.append([nextPos, self.root[nextPos[0]][nextPos[1]]])
               if nextPos[0] - currentPos[0] == 1:
                  if nextPos[1] - currentPos[1] == 1:
                     # Ô phía dưới bên phải ăn được (áp dụng cho hậu)
                     prePath.append([[nextPos[0] + 1, nextPos[1] + 1], 0])
                     self.root[nextPos[0] + 1][nextPos[1] + 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] + 1, nextPos[1] + 1]
                     nextPos = None
                  elif nextPos[1] + 1 == currentPos[1]:
                     # Ô phía dưới bên trái ăn được (áp dụng cho hậu)
                     prePath.append([[nextPos[0] + 1, nextPos[1] - 1], 0])
                     self.root[nextPos[0] + 1][nextPos[1] - 1] = self.root[currentPos[0]][currentPos[1]]
                     
                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] + 1, nextPos[1] - 1]
                     nextPos = None                        
               elif nextPos[0] + 1 == currentPos[0]:
                  if nextPos[1] - currentPos[1] == 1:
                     ## Ô phía trên bên phải ăn được 
                     prePath.append([[nextPos[0] - 1, nextPos[1] + 1], 0])
                     self.root[nextPos[0] - 1][nextPos[1] + 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] - 1, nextPos[1] + 1]
                     nextPos = None
                  elif nextPos[1] + 1 == currentPos[1]:
                     ## Ô phía trên bên trái ăn được 
                     prePath.append([[nextPos[0] - 1, nextPos[1] - 1], 0])
                     self.root[nextPos[0] - 1][nextPos[1] - 1] = self.root[currentPos[0]][currentPos[1]]

                     self.root[currentPos[0]][currentPos[1]] = 0
                     self.root[nextPos[0]][nextPos[1]] = 0
                     currentPos = [nextPos[0] - 1, nextPos[1] - 1]
                     nextPos = None
               # Kiểm tra phong hậu
               if currentPos[0] == 0:
                  if self.root[currentPos[0]][currentPos[1]] == 2:
                     self.root[currentPos[0]][currentPos[1]] = 4
                  elif self.root[currentPos[0]][currentPos[1]] == 1:
                     self.root[currentPos[0]][currentPos[1]] = 3
                  self.countPlayer2King += 1
               # Kiểm tra ăn tiếp được không ?
               temp = showsuggestPlayer2(currentPos, self.root, self.humanFirst)
               if len(temp) == 0:
                  flag = False
               else:
                  for item in temp:
                     if self.root[item[0]][item[1]] != 0:
                        nextPos = item
                        break
                  if nextPos == None:
                     flag = False
      return prePath

   def getBack(self, prePath):
      '''
      ma trận về prePath[0] với prePath là chuỗi action 
      vd [[location1, type1], [location2, type2], location3, type3 ...], đi ngược lại là về vị trí ban đầu
      '''
      m = len(prePath) - 1
      while m >= 0:
         self.root[prePath[m][0][0]][prePath[m][0][1]] = prePath[m][1]
         m -= 1

   def value(self)->int:
      return self.countPlayer1 - self.countPlayer2
     #return self.countPlayer1 - self.countPlayer2 + self.countPlayer1King*0.5 - self.countPlayer2King*0.5


