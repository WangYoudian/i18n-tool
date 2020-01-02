"""
存放parse的规则，录入一些预先发现的模式，依照策略模式构建规则类
"""
import time
from abc import abstractmethod, ABCMeta
import re

from config import *
from loglib.logger import Logger

log = Logger().get_logger()
output_file = 'demo.txt'


class BaseRule(metaclass=ABCMeta):
    @abstractmethod
    def rule_configuration(cls, stream_in, separation_strategy):
        pass

    @abstractmethod
    def regexp(cls, stream_in):
        pass


class PrimaryRule(BaseRule):
    """
    rule_configuration不可用，支持用户自定制类，继承BaseRule
    """
    def rule_configuration(self, stream_in, separation_strategy):
        """
        在实际项目中，配置信息一般都会放在一个统一的config文件中，且用 key = value形式赋值
        至少，在Django和Spring Boot中都是这样
        :return:
        # TODO: 接口参数stream_in修改为file_in
        """
        # 提取项目配置文件中的实际message信息
        pattern = re.compile(r'"[0-9]+"%s.*?"(.*?)"' % separation_strategy)
        matches = re.findall(pattern, stream_in)
        # print(stream_in)
        if matches is None:
            log.info("No pattern found in configuration file, check if you have the wrong separating strategies!")
        with open(output_file, 'a') as f:
            for match in matches:
                if match:
                    f.write(match + '\n')
                else:
                    continue

        log.info("Configuration File Extraction Finished, Rules Are Placed in %s!" % output_file)

    def regexp(self, stream_in):
        """
        模块定制部分
        :return:
        """
        pass


class PythonRule(PrimaryRule):
    """
    定义在Python脚本中的规则
    """
    def regexp(self, stream_in):
        pattern = re.compile(r'raise Exception\("(.*?)"')
        matches = re.findall(pattern, stream_in)
        if matches is None:
            log.info("No pattern found in current script!")
        with open(output_file, 'a') as f:
            for match in matches:
                match = match.replace(' ', '')
                # print(match)
                f.write(match + '\n')


if __name__ == '__main__':
    stream_in = """
        "0":"Success",
        "200":"Success",
        "201": "Exceute Success",
        # Auth failed
        "101":"身份验证失败",
        "102":"权限不足",
        "103":"已有权限,无需再申请",
        "104":"重复申请",
    """

    separation_strategy = ':'
    # print(stream_in)
    python = PythonRule()
    python.rule_configuration(stream_in, separation_strategy)
    stream_in = """
                        raise Exception("请提供必须的tree_id和tree_type和node_list参数")
                                    # 检查下给定的父节点是否存在
            if not self.check_tree_or_node_exists(tree_id=tree_id, tree_type=tree_type, node_id=new_father_id):
                raise Exception("输入的新的父节点[%s]不存在" % new_father_id)

            # 如果它自己的id和要绑定的id是相同的，则不用变更。
            if node_id == new_father_id:
                raise Exception("要绑定的新的父节点和该节点一样，无需变更")

            # 如果是把该节点绑定到它现在的父节点，则不做变更
            ret=self.get_node_info(tree_id=tree_id,tree_type=tree_type,node_id=node_id)
            if ret["father_id"] == new_father_id:
                raise Exception("要绑定的新的父节点是该节点现在的父节点，无需变更")

            # 不能把这个节点绑定到它的子节点上
            length_node = len(node_id.split("-"))
            length_new_father_id = len(new_father_id.split("-"))
            if (length_node < length_new_father_id) and (new_father_id.find(node_id)==0):
                raise Exception("不支持把父节点绑定到它的子节点上面")
    """
    python.regexp(stream_in)
