from django.db import models
from datetime import datetime
from django.conf import settings
# Create your models here.


class UploadImage(models.Model):
    #description = models.CharField(default='这是一个空的描述', max_length=100)
    #image = models.ImageField(default='default.png', upload_to='images/')

    id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=252, default="")
    file_md5 = models.CharField(max_length=128)
    file_type = models.CharField(max_length=32)
    file_size = models.IntegerField()
    url = models.CharField(max_length=100,default='13912B24602642CE96E9A5BDFD7605AC_zuHkkXY.png')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    # 我们还定义了通过文件md5值获取模型对象的类方法
    @classmethod
    def getImageByMd5(cls, md5):
        try:
            return UploadImage.objects.filter(file_md5=md5).first()
        except Exception as e:
            return None

    # 获取本图片的url，我们可以通过这个url在浏览器访问到这个图片
    # 其中settings.WEB_HOST_NAME 是常量配置，指你的服务器的域名
    # settings.WEB_IMAGE_SERVER_PATH 也是常量配置，指你的静态图片资源访问路径
    # 这些配置项我在Django项目的settings.py文件中进行配置
    def getImageUrl(self):
        filename = self.file_md5 + "." + self.file_type
        url = settings.WEB_HOST_NAME + settings.WEB_IMAGE_SERVER_PATH + filename
        return url

    # 获取本图片在本地的位置，即你的文件系统的路径，图片会保存在这个路径下
    def getImagePath(self):
        filename = self.file_md5 + "." + self.file_type
        path = settings.IMAGE_SAVING_PATH + filename
        print(path)
        return path

    def __str__(self):
        s = "filename:" + str(self.filename) + " - " + "filetype:" + str(self.file_type) \
            + " - " + "filesize:" + str(self.file_size) + " - " + "filemd5:" + str(self.file_md5)
        return s
