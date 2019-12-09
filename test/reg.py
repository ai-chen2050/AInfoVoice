import re


str1 = '你好吗1、今天好哈哈哈  2、电话佛庵; 3、第三个'
# ChPattern = re.compile(r'[0-9]+、')  
# result = ChPattern.findall(str1)

res2 = re.split('[0-9]+、', str1)
strAll = res2[0] + '\n'

for num in range(0,len(res2)):
    strAll += str(num) + '、' + res2[num] + '\n'

print(strAll)