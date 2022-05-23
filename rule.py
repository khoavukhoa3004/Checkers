
def getNearLocation(position: list) -> list:
   ''''
   Lấy tất cả vị trí trên đg chéo liền kề ô hiện tại
   '''
   ans = []
   if position[0] > 0:
      if position[1] > 0: 
         ans.append([position[0] - 1, position[1] - 1])
      if position[1] < 7:
         ans.append([position[0] - 1, position[1] + 1])
   if position[0] < 7:
      if position[1] > 0:
         ans.append([position[0] + 1, position[1] - 1])
      if position[1] < 7: 
         ans.append([position[0] + 1, position[1] + 1])
   return ans

def showsuggestPlayer2(position: list, matrix: list, playerFirst: bool)->list:
   '''
   Liệt kê tất cả vị trí mà player2 có thể đi được từ một điểm đã chọn
   '''
   m = 0
   n = 0
   check_eat = False
   check_user = False
   temp = []
   while m <= 7:
      while n <= 7:
         t1 = suggestPlayer2([m,n], matrix, playerFirst)
         if len(t1) == 1:
            t2 = t1.pop()
            if matrix[t2[0]][t2[1]] != 0:
               check_eat = True
               if m == position[0] and n == position[1]:
                  check_user = True
                  break
         n += 1
      if check_user:
         break
      m += 1
      n = 0
   if check_eat:
      if check_user:
         temp = suggestPlayer2([position[0],position[1]], matrix, playerFirst)
      else:
         temp = []
   else:
      temp = suggestPlayer2([position[0],position[1]], matrix, playerFirst)
   return temp
def showsuggestPlayer1(position: list, matrix: list, playerFirst: bool)->list:
   '''
   Liệt kê tất cả vị trí mà player1 có thể đi được từ vị trí đã chọn.
   '''
   m = 0
   n = 0
   check_eat = False
   check_user = False
   temp = []
   while m <= 7:
      while n <= 7:
         t1 = suggestPlayer1([m,n], matrix, playerFirst)
         if len(t1) == 1:
            t2 = t1.pop()
            if matrix[t2[0]][t2[1]] != 0:
               check_eat = True
               if m == position[0] and n == position[1]:
                  check_user = True
                  break
         n += 1
      if check_user:
         break
      m += 1
      n = 0
   if check_eat:
      if check_user:
         temp = suggestPlayer1([position[0],position[1]], matrix, playerFirst)
      else:
         temp = []
   else:
      temp = suggestPlayer1([position[0],position[1]], matrix, playerFirst)
   return temp

def suggestPlayer2(position: list, matrix: list, playerFirst: bool) -> list:
   ''''
   Gợi ý ô đi tiếp theo cho human hoặc player 2(nằm ở nửa dưới bàn cờ di chuyển) tại position. Với playerFirst = True tức 
   nghĩa là nửa dưới cầm quân trắng và ngược lại
   '''
   i = position[0]
   j = position[1]
   ans = []
   if playerFirst:
      # người chơi cầm quân trắng
      if matrix[i][j] not in [1,3]:
         return ans
      else:
         # nếu phần tử hiện chọn chỉ là quân thường
         if matrix[i][j] == 1:
            temp = getNearLocation(position)
            for item in temp:
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans           
         else:  
            # nếu phần tử hiện tại là quân hậu 
            temp = getNearLocation(position)
            for item in temp:
               # Xét 2 ô đường chéo phía trên
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:
                     ans.append(item)
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                      
   else:
      # Người chơi cầm quân đỏ
      if matrix[i][j] not in [2,4]:
         return ans
      else:
         if matrix[i][j] == 2:
            temp = getNearLocation(position)
            for item in temp:
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans           
         else:  
            temp = getNearLocation(position)
            for item in temp:
               # Xét 2 ô đường chéo phía trên
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:
                     ans.append(item)
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
   return ans

def suggestPlayer1(position: list, matrix: list, playerFirst: bool) -> list:
   ''''
   Gợi ý ô đi tiếp theo cho player1 (phần nửa trên của bàn cờ) tại position. Nếu playerFirst = 1 tức nghĩa là player1 cầm quân trắng.
   và ngược lại
   '''
   i = position[0]
   j = position[1]
   ans = []
   if playerFirst:
      # người chơi cầm quân trắng
      if matrix[i][j] not in [1,3]:
         return ans
      else:
         # nếu phần tử hiện chọn chỉ là quân thường
         if matrix[i][j] == 1:
            temp = getNearLocation(position)
            for item in temp:
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía dưới đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans           
         else:  
            # nếu phần tử hiện tại là quân hậu 
            temp = getNearLocation(position)
            for item in temp:
               # Xét 2 ô đường chéo phía trên
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía dưới đang trống
                     ans.append(item)
                  elif matrix[item[0]][item[1]] in [2,4]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                      
   else:
      # Người chơi cầm quân đỏ
      if matrix[i][j] not in [2,4]:
         return ans
      else:
         if matrix[i][j] == 2:
            temp = getNearLocation(position)
            for item in temp:
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía dưới đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans           
         else:  
            # nếu phần tử hiện tại là quân hậu 
            temp = getNearLocation(position)
            for item in temp:
               # Xét 2 ô đường chéo phía trên
               if item[0] + 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía trên đang trống
                     ans.append(item)                                   
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] - 1 >= 0:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] - 1][item[1] + 1] == 0:    # ô đường chéo phía trên bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] - 1][item[1] - 1] == 0:    # ô đường chéo phía trên bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
               if item[0] - 1 == i:
                  if matrix[item[0]][item[1]] == 0:                     # ô đường chéo phía dưới đang trống
                     ans.append(item)
                  elif matrix[item[0]][item[1]] in [1,3]:
                     if item[0] + 1 <= 7:
                        if item[1] - 1 == j and item[1] + 1 <= 7:
                           if matrix[item[0] + 1][item[1] + 1] == 0:    # ô đường chéo phía dưới bên phải có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
                        elif item[1] + 1 == j and item[1] - 1 >= 0:
                           if matrix[item[0] + 1][item[1] - 1] == 0:    # ô đường chéo phía dưới bên trái có thể ăn
                              ans.clear()
                              ans.append(item)
                              return ans
   return ans   

