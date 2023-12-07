import os
import shutil
import subprocess
import time
import wda

from kytest.utils.log import logger
from kytest.utils.common import retry
from kytest.utils.exceptions import KError
from kytest.utils.common import screenshot_util


def connected():
    """已连接设备列表"""
    return TideviceUtil.get_connected()


class TideviceUtil:
    """
    tidevice常用功能的封装
    """

    @staticmethod
    def get_connected():
        """获取当前连接的设备列表"""
        cmd = 'tidevice list'
        output = os.popen(cmd).read()
        device_list = [item.split(' ')[0] for item in output.split('\n') if item]
        if len(device_list) > 0:
            logger.info(f"已连接设备列表: {device_list}")
            return device_list
        else:
            raise KError(msg=f"无已连接设备")

    @staticmethod
    def uninstall_app(device_id=None, pkg_name=None):
        """卸载应用"""
        cmd = f"tidevice -u {device_id} uninstall {pkg_name}"
        logger.info(f"卸载应用: {pkg_name}")
        output = subprocess.getoutput(cmd)
        if "Complete" in output.split()[-1]:
            logger.info(f"{device_id} 卸载应用{pkg_name} 成功")
            return
        else:
            logger.info(f"{device_id} 卸载应用{pkg_name}失败，因为{output}")

    @staticmethod
    def install_app(device_id=None, ipa_url=None):
        """安装应用
        """
        cmd = f"tidevice -u {device_id} install {ipa_url}"
        logger.info(f"安装应用: {ipa_url}")
        output = subprocess.getoutput(cmd)
        if "Complete" in output.split()[-1]:
            logger.info(f"{device_id} 安装应用{ipa_url} 成功")
            return
        else:
            logger.info(f"{device_id} 安装应用{ipa_url}失败，因为{output}")

    @staticmethod
    def start_wda(udid: str, port, wda_bundle_id=None):
        xctool_path = shutil.which("tidevice")
        args = []
        if udid:
            args.extend(["-u", udid])
        args.append("wdaproxy")
        args.extend(["--port", str(port)])
        if wda_bundle_id is not None:
            args.extend(["-B", wda_bundle_id])
        p = subprocess.Popen([xctool_path] + args)
        time.sleep(3)
        if p.poll() is not None:
            raise KError("wda启动失败，可能是手机未连接")


class IosDriver(object):

    def __init__(self, device_id: str = None, pkg_name: str = None):
        """device_id可以是udid，也可以是wda服务url"""
        logger.info("初始化ios驱动")

        self.pkg_name = pkg_name
        if not self.pkg_name:
            raise KError('应用包名不能为空')

        self.device_id = device_id
        if not self.device_id:
            raise KError("设备id不能为空")

        if 'http' in self.device_id:
            self.wda_url = self.device_id
        else:
            self.port = self.device_id.split("-")[0][-4:]
            self.wda_url = f"http://localhost:{self.port}"

        self.d = wda.Client(self.wda_url)

        # check if wda is ready
        if self.d.is_ready():
            logger.info('wda已就绪')
        else:
            if 'http' in self.device_id:
                raise KError("wda异常，请确认服务已正常启动！！！")
            else:
                logger.info('wda未就绪, 现在启动')
                for i in range(5):
                    try:
                        TideviceUtil.start_wda(self.device_id, port=self.port)
                        break
                    except Exception as e:
                        logger.info("启动wda异常，重试!!!")
                        logger.info(str(e))
                        continue
                if self.d.is_ready():
                    logger.info('wda启动成功')
                else:
                    raise KError('wda启动失败，可能是WebDriverAgent APP端证书失效!')

    def device_info(self):
        logger.info("获取设备信息")
        info = self.d.device_info()
        logger.info(info)
        return info

    def current_app(self):
        logger.info("获取当前应用")
        info = self.d.app_current()
        logger.info(info)
        return info

    def page_content(self):
        logger.info('获取页面xml内容')
        page_source = self.d.source(accessible=False)
        logger.info(page_source)
        return page_source

    def install_app(self, ipa_url, new=True):
        """安装应用
        @param ipa_url: ipa链接
        @param new: 是否先卸载
        @return:
        """
        logger.info(f"安装应用: {ipa_url}")
        if new is True:
            self.uninstall_app()

        TideviceUtil.install_app(self.device_id, ipa_url)

    def uninstall_app(self):
        logger.info(f"卸载应用: {self.pkg_name}")
        TideviceUtil.uninstall_app(self.device_id, self.pkg_name)

    def start_app(self, stop=True):
        """启动应用
        @param stop: 是否先停止应用
        """
        logger.info(f"启动应用: {self.pkg_name}")
        if stop is True:
            self.d.app_terminate(self.pkg_name)
        self.d.app_start(self.pkg_name)

    def stop_app(self):
        logger.info(f"停止应用: {self.pkg_name}")
        self.d.app_terminate(self.pkg_name)

    def back(self):
        """返回上一页"""
        logger.info("返回上一页")
        time.sleep(1)
        self.d.swipe(0, 100, 100, 100)

    def enter(self):
        logger.info("点击回车")
        self.d.send_keys("\n")

    @retry
    def input(self, text: str, clear=False, enter=False):
        logger.info(f"输入文本: {text}")
        if clear is True:
            self.d.send_keys("")
        self.d.send_keys(text)
        if enter is True:
            self.enter()

    @retry
    def click(self, x, y):
        logger.info(f"点击坐标: {x}, {y}")
        self.d.click(x, y)

    def screenshot(self, file_name=None, position=None):
        return screenshot_util(self.d,
                               file_name=file_name,
                               position=position)

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        logger.info(f"点击弹窗: {alert_list}")
        try:
            self.d.alert.click(alert_list)
        except:
            pass

    def swipe_up(self):
        self.d.swipe_up()

    def swipe_down(self):
        self.d.swipe_down()

    def swipe_left(self):
        self.d.swipe_left()

    def swipe_right(self):
        self.d.swipe_right()


if __name__ == '__main__':
    pass










