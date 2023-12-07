"""
@Author: kang.yang
@Date: 2023/11/16 17:47
"""
import kytest
from kytest import *
from pages.ios_page import DemoPage


@story('测试demo')
class TestIosDemo(TestCase):

    def start(self):
        self.page = DemoPage(self.driver)

    @title('进入设置页')
    def test_go_setting(self):
        self.page.adBtn.click_exists()
        self.page.myTab.click()
        self.page.setBtn.click()
        self.page.about.assert_exists()


if __name__ == '__main__':
    device_id = connected()[0]
    kytest.main(
        platform='ios',
        device_id=device_id,
        pkg_name='com.qizhidao.company'
    )
