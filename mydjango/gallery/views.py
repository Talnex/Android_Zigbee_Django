from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import filetype, hashlib
from gallery.models import UploadImage
from django.conf import settings


# Create your views here.
# 上传文件的视图
@require_http_methods(["POST"])
@csrf_exempt
def uploadImage(request):
    # 从请求表单中获取文件对象
    file = request.FILES.get("img", None)
    if not file:  # 文件对象不存在， 返回400请求错误
        return returnBadRequest("need file.")

    # 图片大小限制
    if not pIsAllowedFileSize(file.size):
        return returnForbidden("文件太大")

    # 计算文件md5
    md5 = pCalculateMd5(file)
    uploadImg = UploadImage.getImageByMd5(md5)
    if uploadImg:  # 图片文件已存在， 直接返回
        return returnOk({'url': uploadImg.getImageUrl()})

    # 获取扩展类型 并 判断
    ext = pGetFileExtension(file)
    if not pIsAllowedImageType(ext):
        return returnForbidden("文件类型错误")

    # 检测通过 创建新的image对象
    # 文件对象即上一小节的UploadImage模型
    uploadImg = UploadImage()
    uploadImg.filename = file.name
    uploadImg.file_size = file.size
    uploadImg.file_md5 = md5
    uploadImg.file_type = ext
    uploadImg.url = getImageUrl(uploadImg)

    # 保存 文件到磁盘
    with open(uploadImg.getImagePath(), "wb+") as f:
        # 分块写入
        for chunk in file.chunks():
            f.write(chunk)

    uploadImg.save()  # 插入数据库

    # 返回图片的url以供访问
    return returnOk({"url": uploadImg.getImageUrl()})

def getImageUrl(img):
    filename = img.file_md5 + "." + img.file_type
    url = settings.WEB_IMAGE_SERVER_PATH + filename
    return url

# 检测文件类型
# 我们使用第三方的库filetype进行检测，而不是通过文件名进行判断
# pip install filetype 即可安装该库
def pGetFileExtension(file):
    rawData = bytearray()
    for c in file.chunks():
        rawData += c
    try:
        ext = filetype.guess_extension(rawData)
        return ext
    except Exception as e:
        # todo log
        return None


# 计算文件的md5
def pCalculateMd5(file):
    md5Obj = hashlib.md5()
    for chunk in file.chunks():
        md5Obj.update(chunk)
    return md5Obj.hexdigest()


# 文件类型过滤 我们只允许上传常用的图片文件
def pIsAllowedImageType(ext):
    if ext in ["png", "jpeg", "jpg"]:
        return True
    return False


# 文件大小限制
# settings.IMAGE_SIZE_LIMIT是常量配置，我设置为10M
def pIsAllowedFileSize(size):
    limit = settings.IMAGE_SIZE_LIMIT
    if size < limit:
        return True
    return False


from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


# Create your views here.

def returnBase(message="", code=1, status=400):
    data = {
        "err_code": code,
        "message": message
    }
    return JsonResponse(data, status=status)


def returnNotFound(message, code=1):
    return returnBase(message, code)


def returnOk(data=None):
    if not data:
        data = {}
    return JsonResponse(data=data, status=200)


def returnBadRequest(message, code=1):
    return returnBase(message, code)


def returnForbidden(message, code=1):
    return returnBase(message, code, status=403)


def returnRedirect(location):
    return HttpResponseRedirect(location)


# 检查参数
def checkPara(dataMap, keyList):
    if not isinstance(dataMap, dict) or not isinstance(keyList, list):
        return False

    result = [True]
    for k in keyList:
        if k not in dataMap:
            if result[0] == True:
                result[0] = "Need para: " + k
            value = None
        else:
            value = dataMap[k]
        result.append(value)

    return tuple(result)
