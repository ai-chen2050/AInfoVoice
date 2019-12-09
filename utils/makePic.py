import os
import re
from PIL import Image, ImageDraw, ImageFont


class ImgFactory():  
    # msyhbd.ttc  / STKAITI.TTF / STXINGKA.TTF / STXINWEI.TTF
    font = ImageFont.truetype('STXINGKA.TTF', 45)
    fontEng = ImageFont.truetype('STLITI.TTF', 50)
    ChPattern = re.compile(u'[\u4e00-\u9fa5]+')   

    def __init__(self, imgPath, dailyStr):
        # 图片预设宽度
        self.width = 1030
        # 文本
        self.text = dailyStr
        # 图片路径
        self.imgPath = imgPath
        # 段落，行数， 行高
        self.paragraph, self.line_num, self.line_height = self.split_text()

    def get_paragraph(self, text):
        match = ImgFactory.ChPattern.search(text)
        txt = Image.new('RGBA', (1030, 1920), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            if match:              
                width, height = draw.textsize(char, ImgFactory.font)
            else:
                width, height = draw.textsize(char, ImgFactory.fontEng)
            sum_width += width
            if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count

    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_paragraph(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        note_img = Image.open(self.imgPath)
        draw = ImageDraw.Draw(note_img)
        # 左上角开始
        x, y = 10, 220
        for duanluo, line_count in self.paragraph:
            # choose different font by the english or chinese
            match = ImgFactory.ChPattern.search(duanluo)
            if match:
                draw.text((x, y), duanluo, fill=(255,255,255), font=ImgFactory.font)
            else: 
                draw.text((x, y), duanluo, fill=(255, 255, 0), font=ImgFactory.fontEng)  
            y += self.line_height * line_count
        # note_img.show()
        imgTmp = self.imgPath[:-4] + "_tmp.jpg"
        # 如果图片存在，则删除缓存
        if os.path.exists(imgTmp):
            os.remove(imgTmp)
        # 保存    
        note_img.save(imgTmp)

