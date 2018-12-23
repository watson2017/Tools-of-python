- [词云的gitlab地址](https://github.com/amueller/word_cloud)
- [参考文章](http://blog.csdn.net/fontthrone/article/details/72775865)

基于上方的文档，做出词云的一个测试
```
# -*- coding: utf-8 -*-
'''
    基于词云将文本中的文字按照特定的格式生成一个图片
'''
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


filename = "C:\\Users\\scott.wang\\Desktop\\test.txt"
picture = "C:\\Users\\scott.wang\\Desktop\\test.png"
shape = "F:\\girl.png"
font_path = "F:\\simfang.ttf"
girl_color = np.array(Image.open(shape))
image_colors = ImageColorGenerator(girl_color)

# 用 stopwords.add()设置屏蔽显示的词语,可以添加多个
stopwords = set(STOPWORDS)
stopwords.add("aaaa")
stopwords.add("bb")

text = open(filename).read()

wd = WordCloud(
        width=1024,
        height=768,                  # width,height设置生成的词云图片的大小
        font_path=font_path,         # 设置字体为本地的字体，有中文必须要加
        background_color="white",    # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
        max_words=2000,              # 设置最大的字数
        mask=girl_color,             # 通过mask 参数 来设置背景图片，即词云的形状
        max_font_size=40,            # 设置字体的最大值
        stopwords=stopwords,         # 设置停用词
        random_state=42              # 设置有多少种随机生成状态，即有多少种配色方案
    )
# generate 可以对全部文本进行自动分词,但是他对中文支持不好，在WordCloud中设置字符的路径
wd.generate(text)

plt.imshow(wd, interpolation="bilinear")
plt.axis("off")  # 关闭显示x轴、y轴下标

plt.figure()  # 生成一个新的图像
# 用词云形状的图片颜色来渲染词云的颜色，用color_func来指定
plt.imshow(wd.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.figure()
plt.imshow(girl_color, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")

plt.show()  # 展示所有的图片
wd.to_file(picture)  # 保存图片
```
#####提示：
*在选用词云图片的时候背景颜色要与background_color的颜色保持一致*

**词云所用到的图片，及生成的两种图片的对比:**

![词云用到的原图片](http://upload-images.jianshu.io/upload_images/6868814-e073a23e3e0b212b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![根据词云原图片颜色渲染的图片](http://upload-images.jianshu.io/upload_images/6868814-17ac658882a7ebd9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![根据系统默认设置字体颜色的图片](http://upload-images.jianshu.io/upload_images/6868814-e9f97e5380e25a01.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
