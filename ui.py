from ast import Num
from asyncio.windows_events import NULL
import data
import pygame
from ai import Minimax
from rule import showsuggestPlayer2, showsuggestPlayer1
import copy
from button import Button
'''

'''


khaki = (240,230,140)
slate_gray = (112,128,144)
white = (255,255,255)
brown = (165,42,42)
darkgreen = (0,100,0)
green = (152,251,152)
red = (255,0,0)
black = (0,0,0)
ly_cyan = (224,255,255)
sea_green = (46,139,87)
turquoise = (64,224,208)
sandy_brown = (244,164,96)
chocolate = (244,164,96)

# Kích thước của console
widthScreen = 900
heightScreen = 800

# màu của người chơi thứ nhất và người chơi thứ 2
firstEleColor = white # type = 1
secondEleColor = red # type = 2

# Màu khi chọn bước đi
chooseColor = turquoise

# Màu gợi í chọn gợi í ô đi 
suggestColor = sandy_brown

# màu của ô chẵn và màu của ô lẻ
oddEleColor = sea_green
evenEleColor = ly_cyan

# Khoảng cách giữa 2 ô trong bảng
length_between_2_button = 0

pygame.init()
fontTitle = pygame.font.Font(None,50)

opponent_font = pygame.font.Font(None, 30)
your_font = pygame.font.Font(None, 30)
your_turn_font = pygame.font.Font(None, 40)

hisLo = {
   1: [7,6], 2: [7,4], 3: [7,2], 4: [7,0],
   5: [6,7], 6: [6,5], 7: [6,3], 8:[6,1],
   9: [5,6],10:[5,4], 11: [5,2],12:[5,0],
  13: [4,7],14:[4,5], 15: [4,3],16:[4,1],
  17: [3,6],18:[3,4], 19: [3,2],20:[3,0],
  21: [2,7],22:[2,5], 23: [2,3],24:[2,1],
  25: [1,6],26:[1,4], 27: [1,2],28:[1,0],
  29: [0,7],30:[0,5], 31: [0,3],32:[0,1],
}
'''
firstPlayer2, 1 3 2 4 player2 - player1,   
'''
def get_key(val):
   for key, value in hisLo.items():
      if val == value:
            return key
 
   return "key doesn't exist"



class ElementInterface:
   def __init__(self, display_surface,real_location: list, back_ground_color, length, type) -> None:
      self.display_surface = display_surface

      self.location = real_location
      self.background = back_ground_color

      self.width = length
      self.height = length
      
      self.press = False
      self.button = pygame.Rect(self.location, (self.width, self.height))
      
      self.clicked = False
      self.choose = False
      self.suggest = False
      
      self.action = False
      self.type = type

   def draw(self):
      self.action = False
      pos = pygame.mouse.get_pos()
      if self.button.collidepoint(pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.action = True
      if pygame.mouse.get_pressed()[0] == 0:
         self.clicked = False
      return self.action

   def display(self):
      if self.choose:
         self.displayEle()
      elif self.suggest:
         self.displaySuggestEle()
      else:
         self.displayNULL()
      if self.type == 1:
         pygame.draw.circle(self.display_surface, firstEleColor, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/6)
         pass
      elif self.type == 2: 
         pygame.draw.circle(self.display_surface, secondEleColor, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/6)
         pass
      elif self.type == 3: 
         pygame.draw.circle(self.display_surface, firstEleColor, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/6)
         pygame.draw.circle(self.display_surface, black, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/3)
         pass
      elif self.type == 4:
         pygame.draw.circle(self.display_surface, secondEleColor, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/6)
         pygame.draw.circle(self.display_surface, black, [self.location[0] + self.width/2, self.location[1] + self.height/2], self.height/2 - self.height/3)

   def displayEle(self):
      '''
      Vẽ ô cờ được chọn (tô màu background khác với các ô khác)
      '''
      pygame.draw.rect(self.display_surface, chooseColor, self.button)
   def displaySuggestEle(self):
      '''
      Vẽ ô cờ được suggest (tô màu background khác với các ô khác và khác với ô chọn)
      '''
      pygame.draw.rect(self.display_surface, suggestColor, self.button)
   def displayNULL(self):
      '''
      Hiện thị chế độ thường
      '''
      pygame.draw.rect(self.display_surface, self.background ,self.button)


class GameControl:
   def __init__(self, initLocation, length, firstPlayer2) -> None:
      # Các biến xử lý console
      self.initLocation = initLocation
      self.length = length
      self.display_surface = pygame.display.set_mode((widthScreen, heightScreen))

                                                       
      self.matrix = NULL                                 # data là biến ma trận
      
      self.firstPlayer2 = firstPlayer2                       # firstPlayer2 là cờ chỉ player 2 đi trước hay sau
      self.interfaceMatrix = NULL
      self.actionQueue = []                                    # Hàng đợi chứa các action mà người lựa chọn (tối đa 2 ElementInterface)
   
      
      #turn                 
      self.turnPlayer2 = False                              # cờ thể hiện lượt của người hiện tại
      self.setDefaultGame()                              # mặc định game
      self.setInterfaceMatrix()                          
      # Ello
      self.yourEllo = 0
      self.aiEllo = 0
      #self.ggButton = ElementInterface(self.display_surface,(500, 700), )
      self.ggButton = Button((700,650),120, 50, "Dau hang!")
      self.gg = False

      self.history = ""
      self.his2 = ""
      self.resetHis()
   
   # Nếu bạn đi trước, first = false (có nghĩa là máy đi sau) và bạn cầm quân trắng (type = 1)
   def setDefaultGame(self):
      
      # máy cầm quân đỏ
      if self.firstPlayer2:
         self.matrix = copy.deepcopy(data.data["first"])
         self.turnPlayer2 = True
      # nếu máy cầm quân trắng
      else:
         self.matrix = copy.deepcopy(data.data["second"])
         self.turnPlayer2 = False

   def setInterfaceMatrix(self) -> None:
      '''
      Khởi tạo ma trận interfaceMatrix
      '''
      self.interfaceMatrix = []
      for i in range(8):
         for j in range(8):
            if j == 0:
               if (i + j) % 2 ==0:                                                          
                  self.interfaceMatrix.append([ElementInterface(self.display_surface, (self.initLocation[0] + j *(self.length + length_between_2_button), self.initLocation[1] + i *(self.length + length_between_2_button)), evenEleColor,self.length,self.matrix[i][j])])
               else:
                  self.interfaceMatrix.append([ElementInterface(self.display_surface, (self.initLocation[0] + j *(self.length + length_between_2_button), self.initLocation[1] + i *(self.length + length_between_2_button)), oddEleColor,self.length, self.matrix[i][j])])
            else:
               if (i + j) % 2 == 0:
                  self.interfaceMatrix[i].append(ElementInterface(self.display_surface, (self.initLocation[0] + j *(self.length + length_between_2_button), self.initLocation[1] + i *(self.length + length_between_2_button)), evenEleColor,self.length,self.matrix[i][j]))
               else:
                  self.interfaceMatrix[i].append(ElementInterface(self.display_surface, (self.initLocation[0] + j *(self.length + length_between_2_button), self.initLocation[1] + i *(self.length + length_between_2_button)), oddEleColor,self.length, self.matrix[i][j]))       

   def display(self) -> None:
      #chocolate
      self.display_surface.fill(chocolate)
      pygame.display.set_caption("Checkers Game")
      title = fontTitle.render("Checkers Game", True, red)
      self.display_surface.blit(title, (300, 75))
      if self.firstPlayer2:
         opponent_ello = opponent_font.render("Opponent level: "+ str(self.aiEllo), True, red)
         your_ello = your_font.render("Your level: " + str(self.yourEllo), True, white)
      
      else:
         opponent_ello = opponent_font.render("Opponent ello: "+ str(self.aiEllo), True, white)
         your_ello = your_font.render("Your ello: " + str(self.yourEllo), True, red)
      if self.turnPlayer2:
         if self.firstPlayer2:
            your_turn = your_turn_font.render("Robot: Your turn now!!!", True, red)
         else:
            your_turn = your_turn_font.render("Robot: Your turn now!!!", True, white)
      else:
         if self.firstPlayer2:
            your_turn = your_turn_font.render("Robot: It's my turn!! :))", True, white)
         else:
            your_turn = your_turn_font.render("Robot: It's my turn!! :))", True, red)
      self.display_surface.blit(opponent_ello, (600, 200))
      self.display_surface.blit(your_ello, (600, 450))
      self.display_surface.blit(your_turn, (500, 600))


      for i in range(8):
         for j in range(8):
            if isinstance(self.interfaceMatrix[i][j], ElementInterface):
               # Nếu là lượt của player2, xét actionQueue, nếu actionQueue = 1 thì gợi ý các nước đi 
               # tiếp theo có thể có = cách kích interfaceMatrix.suggest = True
               # Nếu actionQueue = 2. Xét vị trí cần di chuyển. Nếu nó có suggest = True thì di chuyển
               # nếu ko thì reset actionQueue. Trả suggest = False
               if self.turnPlayer2:
                  if self.interfaceMatrix[i][j].draw():
                     self.interfaceMatrix[i][j].choose = not(self.interfaceMatrix[i][j].choose)
                     # Xét vị trí vừa chọn, đưa vào actionQueue để xử lý
                     if [i,j] in self.actionQueue:
                        self.actionQueue.clear()
                     else:
                        self.actionQueue.append([i,j])
                     #print(len(self.actionQueue))
                     
                     # Nếu actionQueue = 1, gợi í phương án đi cho player2, đồng thời đánh dấu những điểm suggest để player2 chọn
                     if len(self.actionQueue) == 1:
                        self.showsuggestPlayer2(self.actionQueue[0])
                        
                     
                     # quan trọng, bước này để run player2 chọn, nếu đi thành công thì set turnPlayer2 = false
                     if len(self.actionQueue) == 2:
                        if self.moveInterfacePlayer2():
                           if not(self.firstPlayer2) :
                              self.saveTempHis()
                              pass
                           self.turnPlayer2 = False
                        self.actionQueue.clear()                       
                     # Nếu hàng đợi == 2: bắt đầu kiểm tra 2 điểm chọn có đúng với suggest ko, nếu đúng thì move, nếu không thì xóa data cho lại từ đầu
                     if len(self.actionQueue) > 2: 
                        for item in self.actionQueue:
                           self.interfaceMatrix[item[0]][item[1]].choose = False
                        self.actionQueue.clear()   
               else:
                  if self.interfaceMatrix[i][j].draw():
                     self.interfaceMatrix[i][j].choose = not(self.interfaceMatrix[i][j].choose)
                  # Xét vị trí vừa chọn, đưa vào actionQueue để xử lý
                     if [i,j] in self.actionQueue:
                        self.actionQueue.clear()
                     else:
                        self.actionQueue.append([i,j])
                     #print(len(self.actionQueue))
                  
                     # Nếu actionQueue = 1, gợi í phương án đi cho player1, đồng thời đánh dấu những điểm suggest để player1 chọn
                     if len(self.actionQueue) == 1:
                        self.showsuggestPlayer1(self.actionQueue[0])
                     
                  
                     # quan trọng, bước này để run player1 chọn, nếu đi thành công thì set turnPlayer2 = True
                     if len(self.actionQueue) == 2:
                        if self.moveInterfacePlayer1():
                           if self.firstPlayer2:
                              self.saveTempHis()
                              pass
                           self.turnPlayer2 = True
                        self.actionQueue.clear()                       
                     # Nếu hàng đợi == 2: bắt đầu kiểm tra 2 điểm chọn có đúng với suggest ko, nếu đúng thì move, nếu không thì xóa data cho lại từ đầu
                     if len(self.actionQueue) > 2: 
                        for item in self.actionQueue:
                           self.interfaceMatrix[item[0]][item[1]].choose = False
                        self.actionQueue.clear()  

      if len(self.actionQueue) == 0:
         for i in range(8):
            for j in range(8):
               self.interfaceMatrix[i][j].type = self.matrix[i][j]
               self.interfaceMatrix[i][j].choose = False
               self.interfaceMatrix[i][j].suggest = False     
      for i in range(8):
         for j in range(8):
            self.interfaceMatrix[i][j].display()
      if self.ggButton.draw(self.display_surface):
         self.gg = True
   def showsuggestPlayer2(self, position):
      '''
      gợi ý các vị trí tiếp theo tại vị trí hiện tại (interface)
      '''
      temp = showsuggestPlayer2(position, self.matrix, self.firstPlayer2)
      for item in temp:
         self.interfaceMatrix[item[0]][item[1]].suggest = True
      return temp     
   def showsuggestPlayer1(self, position):
      '''
      Giống v nhưng là player1
      '''
      temp = showsuggestPlayer1(position, self.matrix, not(self.firstPlayer2))
      for item in temp:
         self.interfaceMatrix[item[0]][item[1]].suggest = True
      return temp
   def moveInterfacePlayer2(self) -> bool:
      '''
      di chuyển player2, nhận dữ liệu từ user (actionQueue và interfaceMatrix.suggest)
      '''
      if len(self.actionQueue) != 2:
         return False
      start = self.actionQueue[0]         # Vị trí muốn di chuyển
      end = self.actionQueue[1]           # Vị trí cần duy chuyển tới
      self.actionQueue.clear()
      move = False
      if self.interfaceMatrix[end[0]][end[1]].suggest:   # Nếu vị trí end được chấp nhận (suggest tại đó = True)
         move = True
         self.his2 += " "+str(get_key(start)) + " " + str(get_key(end))

         if self.matrix[end[0]][end[1]] == 0:            # Nếu vị trí end rỗng
            self.matrix[end[0]][end[1]] = self.matrix[start[0]][start[1]]
            self.matrix[start[0]][start[1]] = 0

            self.interfaceMatrix[end[0]][end[1]].type = self.interfaceMatrix[start[0]][start[1]].type
            self.interfaceMatrix[start[0]][start[1]].type = 0 
            if end[0] == 0:                             # Nếu vị trí end có thể phong hậu
               if self.firstPlayer2:
                  self.matrix[end[0]][end[1]] = 3
                  self.interfaceMatrix[end[0]][end[1]].type = 3
               else:
                  self.matrix[end[0]][end[1]] = 4
                  self.interfaceMatrix[end[0]][end[1]].type = 4
         else:       
            '''
            Nếu end là một quân cờ đối thủ, tiến hành di chuyển đến vị trí trống (sau khi ăn)
            xóa đối thủ. Thiết lập start = vị trí hiện tại, nếu vị trí đó có thể ăn thì set end = vị trí 
            di chuyển tiếp theo và flag = True, nếu ko còn ăn được thì end = None, flag = False.
            Loop
            '''

            flag = True
            while flag:
               if end[0] - 1 == start[0] and end[1] - 1 == start[1]:
                  self.matrix[end[0] + 1][end[1] + 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] + 1][end[1] + 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] + 1, end[1] + 1]
               elif end[0] - 1 == start[0] and end[1] + 1 == start[1]:
                  self.matrix[end[0] + 1][end[1] - 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] + 1][end[1] - 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] + 1, end[1] - 1]
               elif end[0] + 1 == start[0] and end[1] - 1 == start[1]:
                  self.matrix[end[0] - 1][end[1] + 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] - 1][end[1] + 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] - 1, end[1] + 1]
               elif end[0] + 1 == start[0] and end[1] + 1 == start[1]:
                  self.matrix[end[0] - 1][end[1] - 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] - 1][end[1] - 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] - 1, end[1] - 1]
               if start[0] == 0:
                  if self.firstPlayer2:
                     self.matrix[start[0]][start[1]] = 3
                     self.interfaceMatrix[start[0]][start[1]].type = 3
                  else:
                     self.matrix[start[0]][start[1]] = 4
                     self.interfaceMatrix[start[0]][start[1]].type = 4
               temp = self.showsuggestPlayer2(start)
               if len(temp) == 0:
                  flag = False
               else:
                  for item in temp:
                     if self.interfaceMatrix[item[0]][item[1]].type != 0:
                        end = item
                        break
                     else:
                        flag = False
      return move
   
   def moveInterfacePlayer1(self)->bool:
      '''
      di chuyển player1
      '''
      if len(self.actionQueue) != 2:
         return False
      start = self.actionQueue[0]
      end = self.actionQueue[1]
      self.actionQueue.clear()
      move = False
      if self.interfaceMatrix[end[0]][end[1]].suggest:
         move = True

         self.his2 += " "+str(get_key(start)) + " " + str(get_key(end))

         if self.matrix[end[0]][end[1]] == 0:
            self.matrix[end[0]][end[1]] = self.matrix[start[0]][start[1]]
            self.matrix[start[0]][start[1]] = 0

            self.interfaceMatrix[end[0]][end[1]].type = self.interfaceMatrix[start[0]][start[1]].type
            self.interfaceMatrix[start[0]][start[1]].type = 0 
            if end[0] == 7:
               if self.firstPlayer2:
                  self.matrix[end[0]][end[1]] = 4
                  self.interfaceMatrix[end[0]][end[1]].type = 4
               else:
                  self.matrix[end[0]][end[1]] = 3
                  self.interfaceMatrix[end[0]][end[1]].type = 3
         else:
            flag = True
            while flag:
               if end[0] - 1 == start[0] and end[1] - 1 == start[1]:
                  self.matrix[end[0] + 1][end[1] + 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] + 1][end[1] + 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] + 1, end[1] + 1]
               elif end[0] - 1 == start[0] and end[1] + 1 == start[1]:
                  self.matrix[end[0] + 1][end[1] - 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] + 1][end[1] - 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] + 1, end[1] - 1]
               elif end[0] + 1 == start[0] and end[1] - 1 == start[1]:
                  self.matrix[end[0] - 1][end[1] + 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] - 1][end[1] + 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] - 1, end[1] + 1]
               elif end[0] + 1 == start[0] and end[1] + 1 == start[1]:
                  self.matrix[end[0] - 1][end[1] - 1] = self.matrix[start[0]][start[1]]
                  self.matrix[end[0]][end[1]] = 0
                  self.matrix[start[0]][start[1]] = 0

                  self.interfaceMatrix[end[0] - 1][end[1] - 1].type = self.interfaceMatrix[start[0]][start[1]].type
                  self.interfaceMatrix[end[0]][end[1]].type = 0
                  self.interfaceMatrix[end[0]][end[1]].suggest = False
                  self.interfaceMatrix[start[0]][start[1]].type = 0
                  start = [end[0] - 1, end[1] - 1]
               if start[0] == 7:
                  if self.firstPlayer2:
                     self.matrix[start[0]][start[1]] = 4
                     self.interfaceMatrix[start[0]][start[1]].type = 4
                  else:
                     self.matrix[start[0]][start[1]] = 3
                     self.interfaceMatrix[start[0]][start[1]].type = 3
               temp = self.showsuggestPlayer1(start)
               if len(temp) == 0:
                  flag = False
               else:
                  for item in temp:
                     if self.interfaceMatrix[item[0]][item[1]].type != 0:
                        end = item
                        break
                     else:
                        flag = False
      return move
   
   def movePlayer1(self, current: list, next: list)-> bool:
      if current == next:
         return False
      self.actionQueue.clear()
      self.actionQueue.append(current)
      temp = self.showsuggestPlayer1(current)
      self.actionQueue.append(next)
      ans = self.moveInterfacePlayer1()
      for item in temp:
         self.interfaceMatrix[item[0]][item[1]].suggest = False
      return ans

   def movePlayer2(self, current, next)-> bool:
      if current == next:
         return False
      self.actionQueue.clear()
      self.actionQueue.append(current)
      temp = self.showsuggestPlayer2(current)
      self.actionQueue.append(next)
      ans = self.moveInterfacePlayer2()
      for item in temp:
         self.interfaceMatrix[item[0]][item[1]].suggest = False
      return ans
   
   def getData(self) -> list:
      return self.matrix

   # Phương thức dùng để load dữ liệu bước đi tiếp theo vào giao diện
   def setData(self, data):
      self.matrix = data
      self.setInterfaceMatrix()
      self.display()
   def countPlayer(self):
      '''
      Trả về số lượng quân cờ và số quân hậu của player 1 và player2.
      '''
      count1 = 0
      count1King = 0
      count2 = 0
      count2King = 0
      for i in range(8):
         for j in range(8):
            if self.firstPlayer2:
               if self.matrix[i][j] in [1,3]:
                  count2 += 1
                  if self.matrix[i][j] == 3:
                     count2King += 1
               elif self.matrix[i][j] in [2,4]:
                  count1 += 1
                  if self.matrix[i][j] == 4:
                     count1King += 1
            else:
               if self.matrix[i][j] in [1,3]:
                  count1 += 1
                  if self.matrix[i][j] == 3:
                     count1King += 1
               elif self.matrix[i][j] in [2,4]:
                  count2 += 1
                  if self.matrix[i][j] == 4:
                     count2King += 1
      return count1, count1King, count2, count2King

   def saveTempHis(self):
      #count1, count1King, count2, count2King = self.countPlayer()

      #self.history +=" " + self.his2 + " " + str(count2 - count1)
      self.history +=" " + self.his2
      self.his2 = ","
   def resetHis(self):
      self.history = str(int(self.firstPlayer2))
      self.his2 = ","




