#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    从企业微信中获取用户 ID，更新到 zabbix 用户的企业微信告警媒介的 sendto。
"""
import argparse
import sys
import os
from functools import reduce
import logging
import copy
from lib.utils.format import pretty_tbl
from lib.utils.wxapis import WxWorkApi

# 以下分别代表了在设置告警通知级别时，各个级别所对应的数值
# 以各项相加之值代表所要设置的告警通知级别
NOT_CLASSIFIED = 1
INFORMATION = 2
WARNING = 4
AVERAGE = 8
HIGH = 16
DISASTER = 32
# 指定要通过其进行用户匹配的告警媒介
# Zabbix 的用户信息和企业微信的用户信息没有必然的联系，但是通过手机号码、邮箱
# 这些独一无二的信息可以用来在企业微信中进行匹配和搜索
MEDIA_ATTR_LIST = [
    {"kind": "email", "media_type_name": "Email", "attr": "email"},
    {"kind": "sms", "media_type_name": "FortuneSMS", "attr": "mobile"},
    {"kind": "wework", "media_type_name": "wework-sendmsg", "attr": "wework_id"},
    {"kind": "wework", "media_type_name": "Wxwork webhook", "attr": "wework_id"}
]
# 定义一个全局变量，用来存储特定媒介（如 FortuneSMS、Email 等）的 id 与媒介名称的对应关系
# 之所以指定特定的媒介，如 FortuneSMS、Email 等，是为后续匹配邮件、匹配手机号码做准备
# 生成的数据格式如下：
# {"1": "email", "5": "mobile", "12": "wework_id", "16": "wework_id"}
USER_MEDIA_ATTRS = {}
# 定义一个全局变量，用来保存从命令行输入的媒介名称得到的媒介 id
WEWORK_MEDIA_TYPE_ID = None
# 定义一个全局变量，用来保存从 Zabbix 中获取到的用户信息
ZABBIX_USERS = []


def show(zbx_users: list):
    field_names = ["Zabbix Userid", "Zabbix User Fullname", "Zabbix User Sendto"]
    tbl = pretty_tbl(
        title="Zabbix用户企业微信账号对照",
        field_names=field_names,
        rows=[
            [
                zbx_user.get("username"),
                zbx_user.get("fullname") if zbx_user.get("fullname") else "",
                zbx_user.get("output_sendto") if zbx_user.get("output_sendto") else ""
            ]
            for zbx_user in zbx_users
            if zbx_users
        ]
    )
    for field in field_names:
        tbl.align[field] = "l"
    print(tbl)


class SyncWeworkMedia:
    def __init__(self, zapi, corpid, agentid, secret, depart_name,
                 zbx_usrgrps, zbx_username, extra_media_type):
        self._zapi = zapi
        self._corpid = corpid
        self._agentid = agentid
        self._secret = secret
        self._zbx_usrgrps = zbx_usrgrps
        self._depart_name = depart_name
        self._zbx_username = zbx_username
        self._extra_media_type = extra_media_type

    def get_media_attrs(self):
        """
            依据 "MediaAttrList" 列表获取用户必要的媒介信息：
                1. "MediaAttrList" 列表指定了用户特定的媒介类型，如 FortuneSMS、Email 等；
                2. 获取这些特定类型媒介的信息是为了之后通过邮件、手机号码等匹配用户做准备。
        :return:
        """
        for item in MEDIA_ATTR_LIST:
            media_type = self._zapi.mediatype.get(
                {
                    "output": ["name"],
                    "filter": {"name": item.get("media_type_name")}
                }
            )
            media_attr = {media_type[0].get("mediatypeid"): item.get("attr")} if media_type else {}
            global USER_MEDIA_ATTRS
            USER_MEDIA_ATTRS.update(media_attr)
            if item["kind"] == "wework" and item.get("media_type_name") == self._extra_media_type:
                global WEWORK_MEDIA_TYPE_ID
                WEWORK_MEDIA_TYPE_ID = media_type[0].get("mediatypeid") if media_type else None

    def get_zbx_users(self):
        """
            获取指定的用户信息：
                1. 依据命令行传入的参数获取指定用户信息，包括 "medias"；
                2. 获取到的用户信息需要针对中文名称进行处理；
                3. 最后还要根据 "MediaAttrList" 列表中指定的用户特定媒介进行更新以为后续的匹配做准备。
        :return:
        """
        user_groups = self._zapi.usergroup.get(
            {
                "filter": {"name": self._zbx_usrgrps},
                "output": ["name"]
            }
        )
        global ZABBIX_USERS
        zbx_users = self._zapi.user.get(
            {
                "output": ["alias", "name", "surname"],
                "usrgrpids": [grp.get("usrgrpid") for grp in user_groups if user_groups],
                "filter": {"username": self._zbx_username},
                "selectMedias": ["mediatypeid", "sendto", "active", "severity", "period"]
            }
        )
        ZABBIX_USERS = zbx_users
        for zbx_user in ZABBIX_USERS:
            if zbx_user.get("surname") and zbx_user.get("name"):
                # 添加 fullname，即 "姓+名"
                zbx_user["fullname"] = zbx_user.get("surname") + zbx_user.get("name")

            medias = zbx_user.get("medias")
            for media in medias:
                mediatypeid = media.get("mediatypeid")
                # USER_MEDIA_ATTRS:
                # {"1": "email", "5": "mobile", "12": "wework_id", "16": "wework_id"}
                if mediatypeid in USER_MEDIA_ATTRS:
                    attr = USER_MEDIA_ATTRS.get(mediatypeid)
                    sendto = media.get("sendto") if isinstance(media.get("sendto"), list) \
                        else [media.get("sendto")]
                    if zbx_user.get(attr):
                        zbx_user[attr] += sendto
                    else:
                        zbx_user[attr] = sendto

    def match_wework_userid(self, zbx_user: dict):
        """
            匹配用户信息以获取到准确的用户：
               1. 从 Zabbix 用户告警媒介中，通过报警媒介类型, 提取到用户的手机号码、邮箱、姓名等信息；
               2. 通过多种途径匹配到该用户在企业微信的 userid；
               3. 优先通过手机号码匹配, 如用户无手机号码或手机号码匹配不到，再依次通过其他途径匹配；
               4. 最终匹配到企业微信的 userid 的用户, 新建或更新报警媒介。
        :param zbx_user:
        :return:
        """
        match_funcs = [
            # 通过手机号码匹配（手机号码是唯一的）
            lambda z_user, w_user: w_user.get("mobile") in z_user.get("mobile", []),
            # 通过邮箱匹配（邮箱名也是唯一的）
            lambda z_user, w_user: w_user.get("email") in z_user.get("email", []),
            # 通过 surname + name 匹配（姓名有可能重复的）
            lambda z_user, w_user: z_user.get("fullname") == w_user.get("name")
        ]
        wework_users = WxWorkApi(
            corpid=self._corpid,
            agentid=self._agentid,
            secret=self._secret
        ).get_dep_users(self._depart_name)
        for match_func in match_funcs:
            result = [
                user
                for user in wework_users
                if wework_users and match_func(zbx_user, user)
            ]
            if result:
                return result[0].get("userid")

    def add_user_wework_media(self, zbx_user: dict, update=False, prefix=False):
        """
            为 zabbix 用户添加企业微信告警媒介：
                1. 如用户已经存在企业微信告警媒介, 且原 userid 与获取到的 userid 不一致, update 值为 False 则不做处理，
                   update 值为 True 则更新为获取到的 userid。
        """
        wework_userid = self.match_wework_userid(zbx_user)
        if not wework_userid:
            logging.info(
                "\033[33m同步失败: Zabbix user '%s' 未找到对应的企业微信账号\033[0m",
                zbx_user.get("username")
            )
            return
        zbx_user_medias = zbx_user.get("medias")
        zbx_user_medias_copy = copy.deepcopy(zbx_user.get("medias"))
        sendto = f"{self._corpid}_{wework_userid}" if prefix else wework_userid
        add_media = {
            "mediatypeid": "",
            "sendto": sendto,
            # 0 表示开启，1 表示禁用
            "active": 0,
            "severity": str(sum([WARNING, AVERAGE, HIGH, DISASTER])),
            "period": "1-7,00:00-24:00"
        }
        typeid = WEWORK_MEDIA_TYPE_ID
        wework_media = [media for media in zbx_user_medias if media.get("mediatypeid") == typeid]
        # wework_media:
        # [{"mediatypeid": "", "sendto": "", "active": "", "severity": "", "period": ""}]
        if wework_media and not [media for media in wework_media if media.get("sendto") == sendto]:
            for media in wework_media:
                sendto = media.get("sendto")
                add_media.update({"mediatypeid": typeid})
                zbx_user_medias.append(add_media)
                # 企业微信 id 和企业微信用户 id 使用 "_" 进行分割，但是考虑到用户 id 中带有 "_" 的情况，
                # 因而指定分割次数，即 "maxsplit=1"
                wework_split = sendto.split("_", maxsplit=1)
                # 当 zabbix user 已经有了相应的 wework 告警媒介，但是此用户属于另一个企业时，需要再次添加
                # 考虑到企业微信用户名称中可能带有 "_" 的情况，"maxsplit=1" 指定根据匹配到的第一个 "_" 进行分割
                if sendto and len(wework_split) == 2 and wework_split[0] != self._corpid and prefix:
                    add_media.update({"mediatypeid": typeid})
                    zbx_user_medias.append(add_media)
                if update and sendto:
                    media.update(
                        {
                            "sendto": f"{wework_split[0]}_{wework_userid}" if
                            sendto and len(wework_split) == 2 else wework_userid
                        }
                    )
                    logging.info(
                        "\033[32m成功更新企业微信userid：Zabbix userid => '%s', "
                        "WeWork userid => '%s'\033[0m",
                        zbx_user.get("username"),
                        wework_userid
                    )
        if not wework_media:
            add_media.update({"mediatypeid": typeid})
            zbx_user_medias.append(add_media)
        # 对要更新的用户 medias 列表进行去重，防止重复添加
        distinct_zbx_user_medias = []
        if zbx_user_medias:
            for media in zbx_user_medias:
                if media not in distinct_zbx_user_medias:
                    distinct_zbx_user_medias.append(media)
        if distinct_zbx_user_medias != zbx_user_medias_copy:
            self._zapi.user.update(
                {
                    "userid": zbx_user.get("userid"),
                    "medias": distinct_zbx_user_medias
                }
            )
            logging.info(
                "\033[32m同步成功: Zabbix user: '%s', WeWork userid: '%s'\033[0m",
                zbx_user.get("username"),
                wework_userid
            )
        return add_media.get("sendto")


def main(args):
    corpid = args.corpid
    secret = args.secret
    agentid = args.agentid
    if args.env:
        corpid = corpid if corpid else os.environ.get("WEWORK_CORPID")
        secret = secret if secret else os.environ.get("WEWORK_SECRET")
        agentid = agentid if agentid else os.environ.get("WEWORK_AGENTID")
    if corpid and secret and agentid:
        worker = SyncWeworkMedia(
            zapi=args.zapi,
            corpid=corpid,
            agentid=agentid,
            secret=secret,
            depart_name=args.depart_name,
            zbx_usrgrps=reduce(lambda x, y: x + y, args.usergroups) if args.usergroups else [],
            zbx_username=args.username,
            extra_media_type=args.media_type
        )
        worker.get_media_attrs()
        worker.get_zbx_users()
        for user in ZABBIX_USERS:
            sendto = worker.add_user_wework_media(
                zbx_user=user,
                update=args.allow_update,
                prefix=args.allow_prefix
            )
            user["output_sendto"] = sendto
        show(ZABBIX_USERS)
    else:
        parser.print_help()
        logging.error("\033[31m缺乏必要参数：'corpid' or 'secret' or 'agentid'\033[0m")
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--corpid", required=True, help="企业微信的企业ID")
parser.add_argument("-t", "--secret", required=True, help="企业微信内应用的Secret")
parser.add_argument("-a", "--agentid", required=True, help="企业微信内应用的ID")
parser.add_argument("-d", "--depart_name", required=True, help="指定企业微信中部门名称")
parser.add_argument("-e", "--env", action="store_true", help="从环境变量中读取参数")
parser.add_argument("-g", "--usergroups", nargs="+", action="append", help="指定更新的zabbix用户组")
parser.add_argument("-u", "--username", help="指定更新的zabbix用户")
parser.add_argument("-m", "--media_type", required=True, help="指定zabbix中企业微信的告警媒介")
parser.add_argument("--allow-update", action="store_true", help="当zabbix user已存在企业微信告警媒介, \
但sendto字段与获取的企业微信userid不一致, 是否允许更新")
parser.add_argument("--allow-prefix", action="store_true", help="是否加上企业微信的企业id作为前缀，\
如'ww438e13e211d83d51_ChenHuiPing'")
parser.set_defaults(handler=main)
