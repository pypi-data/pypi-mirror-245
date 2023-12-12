import json
import pkg_resources

# 载入配置
resource_path = pkg_resources.resource_filename(__name__, 'config.json')

with open(resource_path, 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

others = {
    "/login/cellphone": {
        "name": "手机登录",
        "explain": "说明 : 验证码,使用 /captcha/sent接口传入手机号获取验证码,调用此接口传入验证码,可使用验证码登录,传入后 password 参数将失效",
        "example": [
            {
                "query": {
                    "phone": "13xxx",
                    "captcha": "1234"
                },
                "result": {}
            }
        ]
    },
    "/user/replacephone": {
        "name": "用户绑定手机",
        "explain": "说明 : 登录后调用此接口 , 可以更换绑定手机",
        "example": [
            {
                "query": {
                    "phone": "xxx",
                    "captcha": "1234",
                    "oldcaptcha": "2345"
                },
                "result": {}
            }
        ]
    },
    "/audio/match": {
        "name": "听歌识曲",
        "explain": "说明: 使用此接口,上传音频文件或者麦克风采集声音可识别对应歌曲信息,具体调用例子参考 ",
        "example": []
    },
    "/rebind": {
        "name": "更换绑定手机",
        "explain": "说明 : 调用此接口 ,可更换绑定手机(流程:先发送验证码到原手机号码,再发送验证码到新手机号码然后再调用此接口)",
        "example": [
            {
                "query": {
                    "phone": "xxx",
                    "oldcaptcha": "1234",
                    "captcha": "5678"
                },
                "result": {}
            }
        ]
    },
    "/nickname/check": {
        "name": "重复昵称检测",
        "explain": "说明 : 调用此接口 ,可检测昵称是否重复,并提供备用昵称\n",
        "example": [
            {
                "query": {
                    "nickname": "binaryify"
                },
                "result": {}
            }
        ]
    },
    "/activate/init/profile": {
        "name": "初始化昵称",
        "explain": "说明 : 刚注册的账号(需登录),调用此接口 ,可初始化昵称",
        "example": [
            {
                "query": {
                    "nickname": "testUser2019"
                },
                "result": {}
            }
        ]
    },
    "/cellphone/existence/check": {
        "name": "检测手机号码是否已注册",
        "explain": "说明 : 调用此接口 ,可检测手机号码是否已注册",
        "example": [
            {
                "query": {
                    "phone": "13xxx"
                },
                "result": {}
            }
        ]
    },
    "/register/cellphone": {
        "name": "注册(修改密码)",
        "explain": "说明 : 调用此接口 ,传入手机号码和验证码,密码,昵称, 可注册网易云音乐账号(同时可修改密码)",
        "example": [
            {
                "query": {
                    "phone": "13xxx",
                    "password": "xxxxx",
                    "captcha": "1234",
                    "nickname": "binary1345"
                },
                "result": {}
            }
        ]
    },
    "/captcha/verify": {
        "name": "验证验证码",
        "explain": "说明 : 调用此接口 ,传入手机号码和验证码, 可校验验证码是否正确",
        "example": [
            {
                "query": {
                    "phone": "13xxx",
                    "captcha": "1597"
                },
                "result": {}
            }
        ]
    },
    "/captcha/sent": {
        "name": "发送验证码",
        "explain": "说明 : 调用此接口 ,传入手机号码, 可发送验证码",
        "example": [
            {
                "query": {
                    "phone": "13xxx"
                },
                "result": {}
            }
        ]
    },
    "/login/refresh": {
        "name": "刷新登录",
        "explain": "说明 : 调用此接口 , 可刷新登录状态,返回内容包含新的cookie(不支持刷新二维码登录的cookie)",
        "example": [
            {
                "query": {},
                "result": {}
            }
        ]
    },
    "/logout": {
        "name": "退出登录",
        "explain": "说明 : 调用此接口 , 可退出登录",
        "example": [
            {
                "query": {},
                "result": {}
            }
        ]
    },
    "/user/update": {
        "name": "更新用户信息",
        "explain": "说明 : 登录后调用此接口 , 传入相关信息,可以更新用户信息",
        "example": [
            {
                "query": {
                    "gender": "0",
                    "signature": "测试签名",
                    "city": "440300",
                    "nickname": "binary",
                    "birthday": "1525918298004",
                    "province": "440000"
                },
                "result": {}
            }
        ]
    },
    "/avatar/upload": {
        "name": "更新头像",
        "explain": "说明 : 登录后调用此接口,使用",
        "example": [
            {
                "query": {
                    "imgSize": "200"
                },
                "result": {}
            }
        ]
    },
    "/pl/count": {
        "name": "私信和通知接口",
        "explain": "说明 : 登录后调用此接口,可获取私信和通知数量信息",
        "example": [
            {
                "query": {},
                "result": {}
            }
        ]
    },
    "/playlist/update": {
        "name": "更新歌单",
        "explain": "说明 : 登录后调用此接口,可以更新用户歌单",
        "example": [
            {
                "query": {
                    "id": "24381616",
                    "name": "新歌单",
                    "desc": "描述",
                    "tags": "欧美"
                },
                "result": {}
            }
        ]
    },
    "/playlist/desc/update": {
        "name": "更新歌单描述",
        "explain": "说明 : 登录后调用此接口,可以单独更新用户歌单描述",
        "example": [
            {
                "query": {
                    "id": "24381616",
                    "desc": "描述"
                },
                "result": {}
            }
        ]
    },
    "/playlist/name/update": {
        "name": "更新歌单名",
        "explain": "说明 : 登录后调用此接口,可以单独更新用户歌单名",
        "example": [
            {
                "query": {
                    "id": "24381616",
                    "name": "歌单名"
                },
                "result": {}
            }
        ]
    },
    "/playlist/tags/update": {
        "name": "更新歌单标签",
        "explain": "说明 : 登录后调用此接口,可以单独更新用户歌单标签",
        "example": [
            {
                "query": {
                    "id": "24381616",
                    "tags": "学习"
                },
                "result": {}
            }
        ]
    },
    "/playlist/cover/update": {
        "name": "歌单封面上传",
        "explain": "说明 : 登录后调用此接口,使用",
        "example": [
            {
                "query": {
                    "id": "3143833470",
                    "imgSize": "200"
                },
                "result": {}
            }
        ]
    },
    "/event/forward": {
        "name": "转发用户动态",
        "explain": "说明 : 登录后调用此接口 ,可以转发用户动态",
        "example": [
            {
                "query": {
                    "evId": "6712917601",
                    "uid": "32953014",
                    "forwards": "测试内容"
                },
                "result": {}
            }
        ]
    },
    "/event/del": {
        "name": "删除用户动态",
        "explain": "说明 : 登录后调用此接口 ,可以删除用户动态",
        "example": [
            {
                "query": {
                    "evId": "6712917601"
                },
                "result": {}
            }
        ]
    },
    "/share/resource": {
        "name": "分享文本、歌曲、歌单、mv、电台、电台节目到动态",
        "explain": "说明 : 登录后调用此接口 ,可以分享文本、歌曲、歌单、mv、电台、电台节目,专辑到动态",
        "example": [
            {
                "query": {
                    "id": "1297494209",
                    "msg": "测试"
                },
                "result": {}
            },
            {
                "query": {
                    "type": "djradio",
                    "id": "336355127"
                },
                "result": {}
            },
            {
                "query": {
                    "type": "djprogram",
                    "id": "2061034798"
                },
                "result": {}
            },
            {
                "query": {
                    "type": "djprogram",
                    "id": "2061034798",
                    "msg": "测试@binaryify 测试"
                },
                "result": {}
            },
            {
                "query": {
                    "type": "noresource",
                    "msg": "测试"
                },
                "result": {}
            }
        ]
    },
    "/send/text": {
        "name": "发送私信",
        "explain": "说明 : 登录后调用此接口 , 传入用户 id 和要发送的信息, 可以发送私信,返回内容为历史私信,包含带歌单的私信信息(注:不能发送私信给自己)",
        "example": [
            {
                "query": {
                    "user_ids": "32953014",
                    "msg": "test"
                },
                "result": {}
            },
            {
                "query": {
                    "user_ids": "32953014,475625142",
                    "msg": "test"
                },
                "result": {}
            }
        ]
    },
    "/send/playlist": {
        "name": "发送私信(带歌单)",
        "explain": "说明 : 登录后调用此接口 , 传入用户 id 和要发送的信息和歌单 id, 可以发送带歌单的私信(注:不能发送重复的歌单)",
        "example": [
            {
                "query": {
                    "msg": "test",
                    "user_ids": "475625142",
                    "playlist": "705123491"
                },
                "result": {}
            },
            {
                "query": {
                    "msg": "test2",
                    "user_ids": "475625142,32953014",
                    "playlist": "705123493"
                },
                "result": {}
            }
        ]
    },
    "/playlist/create": {
        "name": "新建歌单",
        "explain": "说明 : 调用此接口 , 传入歌单名字可新建歌单",
        "example": [
            {
                "query": {
                    "name": "测试歌单"
                },
                "result": {}
            },
            {
                "query": {
                    "name": "test",
                    "type": "VIDEO"
                },
                "result": {}
            }
        ]
    },
    "/playlist/tracks": {
        "name": "对歌单添加或删除歌曲",
        "explain": "说明 : 调用此接口 , 可以添加歌曲到歌单或者从歌单删除某首歌曲 ( 需要登录 )",
        "example": [
            {
                "query": {
                    "op": "add",
                    "pid": "24381616",
                    "tracks": "347231"
                },
                "result": {}
            }
        ]
    },
    "/daily_signin": {
        "name": "签到",
        "explain": "说明 : 调用此接口 , 传入签到类型 ( 可不传 , 默认安卓端签到 ), 可签到 ( 需要登录\n), 其中安卓端签到可获得 3 点经验 , web/PC 端签到可获得 2 点经验",
        "example": [
            {
                "query": {},
                "result": {}
            }
        ]
    },
    "/fm_trash": {
        "name": "垃圾桶",
        "explain": "说明 : 调用此接口 , 传入音乐 id, 可把该音乐从私人 FM 中移除至垃圾桶",
        "example": [
            {
                "query": {
                    "id": "347230"
                },
                "result": {}
            }
        ]
    }
}

config.update(others)


def api_help(name: str = None) -> str:
    """
    获取接口帮助
    :param name: 接口名称
    :return:
    """
    if name is None:
        result_str = ("from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list\n\n"
                      "netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API\n"
                      "netease_cloud_music_api.cookie = YOUR_COOKIE  # 设置cookie\n"
                      "response = netease_cloud_music_api.request(apiName, queryDict)  # 调用接口\n\n"
                      "# Use ”help(apiName)“ to view detailed information about the interface\n"
                      "# Use ”api_list()“ to view the interface list")
    elif name in api_list():
        result_str = f'name: {name}\n    {config[name]["name"]}\n    {config[name]["explain"]}\n\n'

        result_str += "query example: \n"
        for example in config[name]["example"]:
            index = config[name]["example"].index(example)
            result_str += f'{json.dumps(config[name]["example"][index]["query"], indent=2, ensure_ascii=False)}\n\n'
    else:
        result_str = f'apiName: {name} not found，please use ”api_list()“ to view the interface list'

    return result_str


def api_list():
    """
    获取接口列表
    :return:
    """
    return list(config.keys())
