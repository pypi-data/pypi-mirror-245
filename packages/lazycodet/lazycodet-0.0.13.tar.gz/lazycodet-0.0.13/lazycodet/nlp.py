
class NLP:
    def __init__(self):
        self.leftArray = {}
        self.rightArray = {}
        self.fullPuncArray = {}
        self.upperCaseArray = []
        self.keepAndOptimizePunctuation = False
        pass
    def getData(self):
        return self.leftArray, self.rightArray, self.fullPuncArray, self.upperCaseArray
    def isCleanChar(self, char):
        return char.isalnum() or char == ' '
    def save_position_uppercase(self, s):
        """
        :param s: chuỗi cần xử lí
        :return: mảng các vị trí đã lưu trong đó, mỗi vị trí là một mảng đại diện cho việc xuất hiện của từng chữ cái
        """
        vi_tri_chu = []

        for word in s.split():
            vi_tri_word = []
            for char in word:
                if char.isupper():
                    vi_tri_word.append(1)
                else:
                    vi_tri_word.append(0)
            vi_tri_chu.append(vi_tri_word)

        return vi_tri_chu
    def removePunctuation(self, text):
        # return ''.join(char for char in text if char not in string.punctuation)
        return ''.join(char for char in text if self.isCleanChar(char))
    def isWordIsFullPunctuation(self, word):
        """
            ### Hàm kiểm tra xem 1 từ có phải là toàn là punctuation không
            Ví dụ: abc => false
                    .,.,, => true
                    ...., => true
        """
        i = 0
        newText = ''
        isHavePunc = False
        if word == '':
            return False
        while i < len(word) and self.isCleanChar(word[i]):
            newText += word[i]
            isHavePunc = True
            i += 1
        if len(newText) == len(word) and isHavePunc == True:
            return True
        else:
            return False
    def restore_uppercase(self, s, upperCaseArray):
        """
        :param s: chuỗi cần khôi phục
        :param upperCaseArray: mảng các vị trí đã lưu, trong đó 1 là vị trí kí tự viết hoa
        :return: chuỗi đã được khôi phục chữ in hoa
        """

        
        newString = ''

        for idx, word in enumerate(s.split()):
            if len(word) != len(upperCaseArray[idx]):
                newString +=  word + ' '
                continue
            for idx_cs, charStatus in enumerate(upperCaseArray[idx]):
                if charStatus == 1:
                    newString +=  word[idx_cs].upper()
                else: 
                    newString +=  word[idx_cs]
            newString += ' '

        return newString.strip()
    def balance_length(self, arr, indexReference = None):
        """
        #### Hàm căn bằng arr cùng độ dài và thứ tự item khớp với fullPuncArray
        """
        # Trường hợp mà text ban đầu có các từ mà toàn là punc kiểu như ,,,... word word thì sẽ làm cho số lươngk
        # .. phần tử leftArray và rightArray nhiều hơn arr, nên ta sẽ làm căn bằng nó
        for idx in range(len(self.fullPuncArray)):
            if self.fullPuncArray[idx] == True:
                # Nếu như idx bị chèn vào nằm trước indexReference thì cũng sẽ tăng giá trị indexReference theo luôn
                if indexReference is not None and idx <= indexReference:
                    indexReference += 1
                # Dời các phần tử từ vị trí idx đến cuối mảng sang phải một vị trí
                arr.insert(idx, '')
        if indexReference is None:
            return arr
        else:
            return arr, indexReference
    def optimizePunctuation(self, arr):
        arr = self.balance_length(arr)
        textOptimize = ''
        for idx, word in enumerate(arr):
            if self.rightArray[idx] != '': # có puncuation
                textOptimize+= word + self.rightArray[idx][0] + ' '
            elif self.leftArray[idx] == '&':
                textOptimize+= '&' + ' '
            elif word != '':
                textOptimize+= word + ' '
        text = textOptimize.strip()
        return text
    def preprocessing(self, text, keepAndOptimizePunctuation = False):
        """
            #### return: `text` => text đã được xử lí
        """
        self.keepAndOptimizePunctuation = keepAndOptimizePunctuation
        
        # Loại bỏ punctuation và tạo leftArray và rightArray
    
        self.upperCaseArray = self.save_position_uppercase(text)
        # Đưa chuỗi về chữ thường và trim
        text = text.lower().strip()
        self.leftArray, self.rightArray, self.fullPuncArray = self.save_punctuation(text)
        # Loại bỏ punctuation khỏi chuỗi
        text = self.removePunctuation(text)
        text = text.replace('  ', ' ')
        text = text.strip()

        # Tôi ưu hoá - Gắn lại punctuation 1 cách hợp lí
        if keepAndOptimizePunctuation:
            arr = text.split()
            text = self.optimizePunctuation(arr)
        return text
    def save_punctuation(self, text):
        """
        #### return: `leftArray, rightArray, fullPuncArray`
        1. leftArray: các punctuation đã được lưu trữ phía bên trái của các từ
        2. rightArray: các punctuation đã được lưu trữ phía bên phải của các từ
        3. fullPuncArray: đánh dấu lại các vị trí của từ mà từ đó hoàn toàn là các punctuation, ví dụ như `Hello ,,..,, friends`
        """
        leftArray = {}
        rightArray = {}
        fullPuncArray = {}
        for idx, word in enumerate(text.split()):
            fullPuncArray[idx] = False
            # Lưu trữ kí tự cuối cùng của từ
            rightArray[idx] = ''
            i = len(word) - 1
            resultRightArray = ''
            # while i >= 0 and word[i] in string.punctuation:
            while i >= 0 and self.isCleanChar(word[i]) == False:
                resultRightArray += word[i]
                i -= 1
            # Do khi kiểm tra và lấy punctuation cho rightArray lấy từ bên phải qua trái, giả sử từ "w..," thì khi lấy punc sẽ có dạng ,..
            # .. lúc này ta phải đảo ngược lại resultRightArray
            rightArray[idx] += resultRightArray[::-1]

            if len(rightArray[idx]) == len(word):
                rightArray[idx] = ''
                fullPuncArray[idx] = True

            # Lưu trữ kí tự đầu tiên của từ
            leftArray[idx] = ''
            if len(rightArray[idx]) < len(word):
                i = 0
                # while i < len(word) and word[i] in string.punctuation:
                while i < len(word) and self.isCleanChar(word[i]) == False:
                    leftArray[idx] += word[i]
                    i += 1
            else:
                fullPuncArray[idx] = True
        return leftArray, rightArray, fullPuncArray
    def restore(self, text):
        if self.keepAndOptimizePunctuation:
            text = self.removePunctuation(text)
        #-----------------------
        index = 0
        arr = text.split()
        arr = self.balance_length(arr)


        newText = ''
        while index < len(self.leftArray): # index < len(leftArray) hoặc index < len(rightArray) đều được vì nó luôn bằng nhau
            if index > len(arr) - 1 and  self.rightArray[index] != '':
                newText += self.rightArray[index] + ' '
            elif index > len(arr) - 1 and  self.leftArray[index] != '':
                newText = newText + ' ' + self.leftArray[index] + ' '
            else:
                newText += self.leftArray[index] + arr[index] + self.rightArray[index] + ' '


            index += 1
        newText = self.restore_uppercase(newText, self.upperCaseArray)
        return newText.strip()