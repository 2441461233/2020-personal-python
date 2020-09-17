import json
import os
import argparse

class Data:
    def __init__(self, dict_address: str = None, reload: int = 0):
        # 需要重新加载数据时
        if reload == 1:
            self.dataLoadIn(dict_address)
        # 数据地址为空且无加载数据时
        if dict_address is None and not os.path.exists('user.json') and not os.path.exists('repo.json') and not os.path.exists('user_repo.json'):
            raise RuntimeError('error: init failed')
        # 某用户的某事件数量
        x = open('user.json', 'r', encoding='utf-8').read()
        self.__4Events4PerP = json.loads(x)
        # 某项目的某事件数量
        x = open('repo.json', 'r', encoding='utf-8').read()
        self.__4Events4PerR = json.loads(x)
        # 某用户在某项目的某事件数量
        x = open('user_repo.json', 'r', encoding='utf-8').read()
        self.__4Events4PerPPerR = json.loads(x)

    def dataLoadIn(self, dict_address: str):
        json_list = []
        # 遍历文件夹
        for root, dic, files in os.walk(dict_address):
            for f in files:
                # 处理目标json文件
                if f[-5:] == '.json':
                    json_path = f
                    x = open(dict_address+'\\'+json_path,
                             'r', encoding='utf-8').read()
                    # json文件转换为数组, 元素为一行json格式的数据
                    str_list = [_x for _x in x.split('\n') if len(_x) > 0]
                    for _str in str_list:
                        try:
                            json_list.append(json.loads(_str))
                        except:
                            pass
        records = self.__listOfNestedDict2ListOfDict(json_list)
        self.__4Events4PerP = {}
        self.__4Events4PerR = {}
        self.__4Events4PerPPerR = {}
        for i in records:
            if not self.__4Events4PerP.get(i['actor__login'], 0):
                self.__4Events4PerP.update({i['actor__login']: {}})
                self.__4Events4PerPPerR.update({i['actor__login']: {}})
            self.__4Events4PerP[i['actor__login']][i['type']
                                         ] = self.__4Events4PerP[i['actor__login']].get(i['type'], 0)+1
            if not self.__4Events4PerR.get(i['repo__name'], 0):
                self.__4Events4PerR.update({i['repo__name']: {}})
            self.__4Events4PerR[i['repo__name']][i['type']
                                       ] = self.__4Events4PerR[i['repo__name']].get(i['type'], 0)+1
            if not self.__4Events4PerPPerR[i['actor__login']].get(i['repo__name'], 0):
                self.__4Events4PerPPerR[i['actor__login']].update({i['repo__name']: {}})
            self.__4Events4PerPPerR[i['actor__login']][i['repo__name']][i['type']
                                                          ] = self.__4Events4PerPPerR[i['actor__login']][i['repo__name']].get(i['type'], 0)+1
        with open('user.json', 'w', encoding='utf-8') as f:
            json.dump(self.__4Events4PerP,f)
        with open('repo.json', 'w', encoding='utf-8') as f:
            json.dump(self.__4Events4PerR,f)
        with open('user_repo.json', 'w', encoding='utf-8') as f:
            json.dump(self.__4Events4PerPPerR,f)
        return True

    def __parseDict(self, d: dict, prefix: str):
        _d = {}
        for k in d.keys():
            if str(type(d[k]))[-6:-2] == 'dict':
                _d.update(self.__parseDict(d[k], k))
            else:
                _k = f'{prefix}__{k}' if prefix != '' else k
                _d[_k] = d[k]
        return _d

    def __listOfNestedDict2ListOfDict(self, a: list):
        records = []
        for d in a:
            _d = self.__parseDict(d, '')
            records.append(_d)
        return records

    def getEventsUsers(self, username: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        else:
            return self.__4Events4PerP[username].get(event,0)

    def getEventsRepos(self, reponame: str, event: str) -> int:
        if not self.__4Events4PerR.get(reponame,0):
            return 0
        else:
            return self.__4Events4PerR[reponame].get(event,0)

    def getEventsUsersAndRepos(self, username: str, reponame: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        elif not self.__4Events4PerPPerR[username].get(reponame,0):
            return 0
        else:
            return self.__4Events4PerPPerR[username][reponame].get(event,0)


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data = None
        self.argInit()
        print(self.orderAnalyze())

    def argInit(self):
        # 初始化参数
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def orderAnalyze(self):
        # 初始化
        if self.parser.parse_args().init:
            self.data = Data(self.parser.parse_args().init, 1)
            return 0
        else:
            if self.data is None:
                self.data = Data()
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:
                    if self.parser.parse_args().repo:
                        res = self.data.getEventsUsersAndRepos(
                            self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
                    else:
                        res = self.data.getEventsUsers(
                            self.parser.parse_args().user, self.parser.parse_args().event)
                elif self.parser.parse_args().repo:
                    res = self.data.getEventsRepos(
                        self.parser.parse_args().reop, self.parser.parse_args().event)
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':
    a = Run()