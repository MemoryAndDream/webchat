# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: img_operate.py
@time: 2017/12/19 17:05 
"""
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL   import  ImageDraw, ImageFont

import os

class Img_opt:  #参考https://www.cnblogs.com/apexchu/p/4231041.html
    def __init__(self):
        pass

    def add_suiying(self):
        pass

    #转换图片格式为jpg
    @classmethod
    def convert_to_jpg(self,infile):
        f, e = os.path.splitext(infile)
        outfile = f + ".jpg"
        if infile != outfile:
            try:
                Image.open(infile).save(outfile)
            except IOError:
                print("cannot convert", infile)
        return outfile

    #生成缩略图
    @classmethod
    def get_thumbnail(self,infile,size = (128, 128)):
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                im = Image.open(infile)
                im.thumbnail(size)
                im.save(outfile, "JPEG")
            except IOError:
                print("cannot create thumbnail for", infile)
        return outfile

    # 获取图片属性
    @classmethod
    def get_img_property(self,infile):
        try:
            with Image.open(infile) as im:
                print(infile, im.format, "%dx%d" % im.size, im.mode)
        except IOError:
            pass
        return im.format, "%dx%d" % im.size, im.mode

    #显示图片 用于调试
    @classmethod
    def show(self,infile):
        im = Image.open(infile)
        im.show()

    #抠图 (left, upper, right, lower) 都是基于左上为原点  left-right upper-lower
    @classmethod
    def corp(self,infile):
        im = Image.open(infile)
        box = im.copy()  # 直接复制图像
        box = (100, 100, 400, 400)
        region = im.crop(box)
        return region

    #子图拼回原图 这里演示了左右互换 子图的region必须和给定box的region吻合
    @classmethod
    def roll(self,infile, delta):
        "Roll an image sideways"
        im = Image.open(infile)
        image = im.copy()  # 复制图像
        xsize, ysize = image.size

        delta = delta % xsize
        if delta == 0: return image
        part1 = image.crop((0, 0, delta, ysize))#左边一块
        part2 = image.crop((delta, 0, xsize, ysize))#右侧剩余部分
        image.paste(part2, (0, 0, xsize - delta, ysize))#左右互换
        image.paste(part1, (xsize - delta, 0, xsize, ysize))

        return image

    #几何变换 Image类有resize()、rotate()和transpose()、transform()方法进行几何变换。
    @classmethod
    def transform(self,infile):
        im = Image.open(infile)
        #简单几何变换
        out = im.resize((128, 128))
        out = im.rotate(45)  # 顺时针角度表示
        #置换图像
        out = im.transpose(Image.FLIP_LEFT_RIGHT)
        out = im.transpose(Image.FLIP_TOP_BOTTOM)
        out = im.transpose(Image.ROTATE_90)
        out = im.transpose(Image.ROTATE_180)
        out = im.transpose(Image.ROTATE_270)

    # 模式转换 “L”, “RGB” and “CMYK.” 黑白 RGB CMYK
    @classmethod
    def transform(self, infile):
        im = Image.open(infile).convert('L')


    #Filter 图像增强 比如边缘模糊 平滑之类 http://pillow.readthedocs.io/en/latest/reference/ImageFilter.html#module-PIL.ImageFilter
    @classmethod
    def transform(self,infile):
        im = Image.open(infile)
        out = im.filter(ImageFilter.DETAIL)



    #像素点变换

    #处理单独通道

    #高级图片增强http://pillow.readthedocs.io/en/latest/reference/ImageEnhance.html#module-PIL.ImageEnhance

    #动态图 当读取动态图时，PIL自动读取动态图的第一帧，可以使用seek和tell方法读取不同帧。

    #Pillow允许通过Postscript Printer在图片上添加images、text、graphics。

    #draft()方法允许在不读取文件内容的情况下尽可能（可能不会完全等于给定的参数）地将图片转成给定模式和大小

    #增加图片水印
    @classmethod
    def add_watermark_to_image(self,image, watermark):
        rgba_image = image.convert('RGBA')
        rgba_watermark = watermark.convert('RGBA')

        image_x, image_y = rgba_image.size
        watermark_x, watermark_y = rgba_watermark.size

        # 缩放图片
        scale = 10
        watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
        new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
        # 透明度
        rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
        rgba_watermark.putalpha(rgba_watermark_mask)

        watermark_x, watermark_y = rgba_watermark.size
        # 水印位置
        rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask)

        return rgba_image
    '''
    im_before = Image.open("lena.jpg")
    im_before.show()

    im_watermark = Image.open("watermark.jpg")
    im_after = add_watermark_to_image(im_before, im_watermark)
    im_after.show()
    '''

    #增加文字水印
    @classmethod
    # image: 图片  text：要添加的文本 font：字体
    def add_text_to_image(self,image, text):
        # 指定要使用的字体和大小；/Library/Fonts/是macOS字体目录；Linux的字体目录是/usr/share/fonts/
        font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 24)
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)

        text_size_x, text_size_y = image_draw.textsize(text, font=font)
        # 设置文本文字位置
        print(rgba_image)
        text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
        # 设置文本颜色和透明度
        image_draw.text(text_xy, text, font=font, fill='black')

        image_with_text = Image.alpha_composite(rgba_image, text_overlay)

        return image_with_text

    ''' im_before = Image.open("lena.jpg")
    im_before.show()
    im_after = add_text_to_image(im_before, 'WTF')
    im_after.show()
    # im.save('im_after.jpg')
    '''

infile=r'D:\pic\test1.jpg'

#Img_opt.get_img_property(infile)
#outfile = Img_opt.get_thumbnail(infile)
#Img_opt.show(infile)
#Img_opt.roll(infile,30).show()
#Img_opt.corp(infile).show()
im_before = Image.open(infile)
#im_before.show()
im_after = Img_opt.add_text_to_image(im_before, 'mengzaizai')
im_after.show()
# im.save('im_after.jpg')