import json
import os.path
import socket
from pprint import pprint
import requests
from py_mini_racer import py_mini_racer
import pkg_resources

class NeteaseCloudMusicApi:
    def __init__(self):

        resource_path = '/'.join(('NeteaseCloudMusicApi.js',))
        # js_code = pkg_resources.resource_string(__name__, resource_path).decode('utf-8')

        with open(resource_path, 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.ctx = py_mini_racer.MiniRacer()
        self.ctx.eval(js_code)

        self.DEBUG = False

        self.__cookie = None
        self.__ip = None

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            print("get local ip error")
            IP = "116.25.146.177"
        finally:
            s.close()
        return IP

    @property
    def cookie(self):
        if self.__cookie is None:
            if os.path.isfile("cookie_storage"):
                with open("cookie_storage", "r", encoding='utf-8') as f:
                    self.__cookie = f.read()
            else:
                raise Exception("cookie not found")
        else:
            return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        if cookie is None:
            cookie = ""
        self.__cookie = cookie
        with open("cookie_storage", "w+", encoding='utf-8') as f:
            f.write(cookie)

    @property
    def ip(self):
        if self.__ip is None:
            self.__ip = self.get_local_ip()
        return self.__ip

    def request(self, name, query):
        request_param = self.ctx.call('NeteaseCloudMusicApi.beforeRequest', name, query)  # 拿到请求头和请求参数

        param_data = {}
        for item in request_param["data"].split("&"):
            param_data[item.split("=")[0]] = item.split("=")[1]

        response = requests.post(request_param["url"], data=param_data, headers=request_param["headers"])

        response_result = {
            "headers": dict(response.headers),
            "data": json.loads(response.text),
            "status": response.status_code,
        }

        result = self.ctx.call('NeteaseCloudMusicApi.afterRequest',
                               json.dumps(response_result),
                               request_param['crypto'],
                               request_param['apiName'])  # 拿到请求头和请求参数

        return result

    def login_cellphone(self, phone, captcha):
        response = self.api("/login/cellphone", {"phone": phone, "captcha": captcha})

        if response.status_code == 200:
            body = response.json()
            result = {key.replace("avatarImgId_str", "avatarImgIdStr"): value for key, value in body.items()}

            cookies = response.cookies.items()
            result["cookie"] = '; '.join([f'{name}={value}' for name, value in cookies])

            self.cookie = result["cookie"]

            return result

        return response

    def api(self, name, query=None):
        """

        :param name:
        :param query:
        :return: requests.Response
        """
        if query is None:
            query = {}
        if query.get("cookie") is None:
            query["cookie"] = self.cookie

        if query.get("realIP") is None:
            query["realIP"] = self.ip
        else:
            query["realIP"] = query.get("realIP")

        result = self.request(name, query)

        return result


if __name__ == '__main__':
    import json
    import os
    from pprint import pprint
    import dotenv

    from main import NeteaseCloudMusicApi

    dotenv.load_dotenv("../../.env")  # 从.env文件中加载环境变量

    netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
    netease_cloud_music_api.cookie = os.getenv("COOKIE")  # 设置cookie
    netease_cloud_music_api.DEBUG = True  # 开启调试模式


    def songv1_test():
        # 获取歌曲详情
        response = netease_cloud_music_api.api("song_url_v1", {"id": 33894312, "level": "exhigh"})
        pprint(response)


    songv1_test()
