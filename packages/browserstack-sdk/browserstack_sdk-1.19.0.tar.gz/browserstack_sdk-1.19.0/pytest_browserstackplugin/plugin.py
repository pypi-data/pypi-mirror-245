# coding: UTF-8
import sys
bstack111l1_opy_ = sys.version_info [0] == 2
bstack1lllllll_opy_ = 2048
bstack1l11l1_opy_ = 7
def bstackl_opy_ (bstack1l1l11_opy_):
    global bstack11ll11_opy_
    bstack11lll1_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1l1ll1_opy_ = bstack1l1l11_opy_ [:-1]
    bstack1ll1l11_opy_ = bstack11lll1_opy_ % len (bstack1l1ll1_opy_)
    bstack11111ll_opy_ = bstack1l1ll1_opy_ [:bstack1ll1l11_opy_] + bstack1l1ll1_opy_ [bstack1ll1l11_opy_:]
    if bstack111l1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lllllll_opy_ - (bstack11lll_opy_ + bstack11lll1_opy_) % bstack1l11l1_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1lllllll_opy_ - (bstack11lll_opy_ + bstack11lll1_opy_) % bstack1l11l1_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1llll1l_opy_)
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11ll1l111_opy_, bstack1l1l1llll_opy_, update, bstack1ll11l1l1l_opy_,
                                       bstack1111l1l1_opy_, bstack1l1lll11ll_opy_, bstack11ll1ll11_opy_, bstack1ll11l11_opy_,
                                       bstack1l1ll11ll_opy_, bstack11111111_opy_, bstack1ll1l11111_opy_, bstack111l1ll1l_opy_,
                                       bstack111111l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1l1l11l1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll1l1llll_opy_, bstack1ll1ll11l_opy_, bstack1ll11lll_opy_, bstack1lll1111l1_opy_, \
    bstack1l1l1lll1_opy_
from bstack_utils.helper import bstack11l1l11ll_opy_, bstack1l1l1ll1l_opy_, bstack11lll111ll_opy_, bstack111l11lll_opy_, \
    bstack11ll1ll1l1_opy_, \
    bstack11ll1l1ll1_opy_, bstack11l1l1ll_opy_, bstack1ll11l1111_opy_, bstack11ll111lll_opy_, bstack1lllll111l_opy_, Notset, \
    bstack111ll11l_opy_, bstack11ll11l11l_opy_, bstack11l1ll1lll_opy_, Result, bstack11ll1111l1_opy_, bstack11ll11lll1_opy_, bstack1l1l11l11l_opy_, \
    bstack11l1l111l_opy_, bstack111l111ll_opy_, bstack11llll111_opy_
from bstack_utils.bstack11l1l11lll_opy_ import bstack11l1l1l11l_opy_
from bstack_utils.messages import bstack1llllll1ll_opy_, bstack11ll11ll_opy_, bstack11ll1l11_opy_, bstack1lll1lll1l_opy_, bstack1111l1ll1_opy_, \
    bstack1lll1l1l1l_opy_, bstack11lll1ll_opy_, bstack1ll1l111_opy_, bstack1l1lllll_opy_, bstack1ll1111l1l_opy_, \
    bstack1111111l1_opy_, bstack1l11ll11_opy_
from bstack_utils.proxy import bstack1l1ll1ll11_opy_, bstack1llll1111l_opy_
from bstack_utils.bstack11ll11l1_opy_ import bstack111ll11111_opy_, bstack111l1l1ll1_opy_, bstack111l1lllll_opy_, bstack111l1lll11_opy_, \
    bstack111l1ll1ll_opy_, bstack111ll1111l_opy_, bstack111l1lll1l_opy_, bstack1l111111_opy_, bstack111l1l1l1l_opy_
from bstack_utils.bstack1llll11ll1_opy_ import bstack11l111ll1_opy_
from bstack_utils.bstack1ll1l1l1_opy_ import bstack11l11lll_opy_, bstack111llll1l_opy_, bstack1111lll1_opy_, \
    bstack11l1ll111_opy_, bstack1l11l1ll1_opy_
from bstack_utils.bstack1l11l111l1_opy_ import bstack1l11l1lll1_opy_
from bstack_utils.bstack11ll11l11_opy_ import bstack1lll11l1ll_opy_
import bstack_utils.bstack1llllll1l1_opy_ as bstack1l1ll1l1ll_opy_
bstack1l1l11111_opy_ = None
bstack111lll1l1_opy_ = None
bstack11ll1ll1l_opy_ = None
bstack1llll11l1l_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1lll1111l_opy_ = None
bstack1l111ll11_opy_ = None
bstack1ll1l11l11_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack11l11ll11_opy_ = None
bstack1l1l11lll_opy_ = None
bstack1l1l111ll_opy_ = None
bstack1llll1ll_opy_ = None
bstack111lllll1_opy_ = bstackl_opy_ (u"ࠫࠬᓓ")
CONFIG = {}
bstack1l11ll111_opy_ = False
bstack1l1111111_opy_ = bstackl_opy_ (u"ࠬ࠭ᓔ")
bstack11lllllll_opy_ = bstackl_opy_ (u"࠭ࠧᓕ")
bstack1111lll1l_opy_ = False
bstack1ll1ll1lll_opy_ = []
bstack11ll1111l_opy_ = bstack1ll1ll11l_opy_
bstack11111ll111_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᓖ")
bstack1lllllllll1_opy_ = False
bstack11l1llll1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11ll1111l_opy_,
                    format=bstackl_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᓗ"),
                    datefmt=bstackl_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᓘ"),
                    stream=sys.stdout)
store = {
    bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᓙ"): []
}
def bstack1ll11lll1_opy_():
    global CONFIG
    global bstack11ll1111l_opy_
    if bstackl_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᓚ") in CONFIG:
        bstack11ll1111l_opy_ = bstack1ll1l1llll_opy_[CONFIG[bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᓛ")]]
        logging.getLogger().setLevel(bstack11ll1111l_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l11ll1l1l_opy_ = {}
current_test_uuid = None
def bstack1l1ll111l_opy_(page, bstack1l1ll1lll_opy_):
    try:
        page.evaluate(bstackl_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᓜ"),
                      bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᓝ") + json.dumps(
                          bstack1l1ll1lll_opy_) + bstackl_opy_ (u"ࠣࡿࢀࠦᓞ"))
    except Exception as e:
        print(bstackl_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᓟ"), e)
def bstack1ll111l1l_opy_(page, message, level):
    try:
        page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᓠ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩᓡ") + json.dumps(
            message) + bstackl_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨᓢ") + json.dumps(level) + bstackl_opy_ (u"࠭ࡽࡾࠩᓣ"))
    except Exception as e:
        print(bstackl_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥᓤ"), e)
def pytest_configure(config):
    bstack1l1ll111l1_opy_ = Config.get_instance()
    config.args = bstack1lll11l1ll_opy_.bstack11111lll11_opy_(config.args)
    bstack1l1ll111l1_opy_.bstack1111111ll_opy_(bstack11llll111_opy_(config.getoption(bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᓥ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack111111ll11_opy_ = item.config.getoption(bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᓦ"))
    plugins = item.config.getoption(bstackl_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦᓧ"))
    report = outcome.get_result()
    bstack11111111l1_opy_(item, call, report)
    if bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤᓨ") not in plugins or bstack1lllll111l_opy_():
        return
    summary = []
    driver = getattr(item, bstackl_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨᓩ"), None)
    page = getattr(item, bstackl_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧᓪ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11111111ll_opy_(item, report, summary, bstack111111ll11_opy_)
    if (page is not None):
        bstack11111l1l1l_opy_(item, report, summary, bstack111111ll11_opy_)
def bstack11111111ll_opy_(item, report, summary, bstack111111ll11_opy_):
    if report.when == bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᓫ") and report.skipped:
        bstack111l1l1l1l_opy_(report)
    if report.when in [bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᓬ"), bstackl_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᓭ")]:
        return
    if not bstack11lll111ll_opy_():
        return
    try:
        if (str(bstack111111ll11_opy_).lower() != bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨᓮ")):
            item._driver.execute_script(
                bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᓯ") + json.dumps(
                    report.nodeid) + bstackl_opy_ (u"ࠬࢃࡽࠨᓰ"))
        os.environ[bstackl_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᓱ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstackl_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᓲ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstackl_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᓳ")))
    bstack1l1ll1llll_opy_ = bstackl_opy_ (u"ࠤࠥᓴ")
    bstack111l1l1l1l_opy_(report)
    if not passed:
        try:
            bstack1l1ll1llll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstackl_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᓵ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1llll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstackl_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᓶ")))
        bstack1l1ll1llll_opy_ = bstackl_opy_ (u"ࠧࠨᓷ")
        if not passed:
            try:
                bstack1l1ll1llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstackl_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᓸ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1llll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᓹ")
                    + json.dumps(bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᓺ"))
                    + bstackl_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᓻ")
                )
            else:
                item._driver.execute_script(
                    bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᓼ")
                    + json.dumps(str(bstack1l1ll1llll_opy_))
                    + bstackl_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᓽ")
                )
        except Exception as e:
            summary.append(bstackl_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᓾ").format(e))
def bstack1llllllll11_opy_(test_name, error_message):
    try:
        bstack11111l1l11_opy_ = []
        bstack11l1l1l11_opy_ = os.environ.get(bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᓿ"), bstackl_opy_ (u"ࠧ࠱ࠩᔀ"))
        bstack1ll1lll111_opy_ = {bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᔁ"): test_name, bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᔂ"): error_message, bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᔃ"): bstack11l1l1l11_opy_}
        bstack11111l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᔄ"))
        if os.path.exists(bstack11111l11ll_opy_):
            with open(bstack11111l11ll_opy_) as f:
                bstack11111l1l11_opy_ = json.load(f)
        bstack11111l1l11_opy_.append(bstack1ll1lll111_opy_)
        with open(bstack11111l11ll_opy_, bstackl_opy_ (u"ࠬࡽࠧᔅ")) as f:
            json.dump(bstack11111l1l11_opy_, f)
    except Exception as e:
        logger.debug(bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᔆ") + str(e))
def bstack11111l1l1l_opy_(item, report, summary, bstack111111ll11_opy_):
    if report.when in [bstackl_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᔇ"), bstackl_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᔈ")]:
        return
    if (str(bstack111111ll11_opy_).lower() != bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᔉ")):
        bstack1l1ll111l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstackl_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᔊ")))
    bstack1l1ll1llll_opy_ = bstackl_opy_ (u"ࠦࠧᔋ")
    bstack111l1l1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1ll1llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstackl_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᔌ").format(e)
                )
        try:
            if passed:
                bstack1l11l1ll1_opy_(getattr(item, bstackl_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᔍ"), None), bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᔎ"))
            else:
                error_message = bstackl_opy_ (u"ࠨࠩᔏ")
                if bstack1l1ll1llll_opy_:
                    bstack1ll111l1l_opy_(item._page, str(bstack1l1ll1llll_opy_), bstackl_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᔐ"))
                    bstack1l11l1ll1_opy_(getattr(item, bstackl_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᔑ"), None), bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᔒ"), str(bstack1l1ll1llll_opy_))
                    error_message = str(bstack1l1ll1llll_opy_)
                else:
                    bstack1l11l1ll1_opy_(getattr(item, bstackl_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᔓ"), None), bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᔔ"))
                bstack1llllllll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstackl_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᔕ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstackl_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᔖ"), default=bstackl_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᔗ"), help=bstackl_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᔘ"))
    parser.addoption(bstackl_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᔙ"), default=bstackl_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᔚ"), help=bstackl_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᔛ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstackl_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᔜ"), action=bstackl_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᔝ"), default=bstackl_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᔞ"),
                         help=bstackl_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᔟ"))
def bstack1l11ll1111_opy_(log):
    if not (log[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔠ")] and log[bstackl_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔡ")].strip()):
        return
    active = bstack1l1l1l1ll1_opy_()
    log = {
        bstackl_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᔢ"): log[bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᔣ")],
        bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᔤ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫᔥ"),
        bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔦ"): log[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔧ")],
    }
    if active:
        if active[bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪᔨ")] == bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᔩ"):
            log[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔪ")] = active[bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔫ")]
        elif active[bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᔬ")] == bstackl_opy_ (u"ࠪࡸࡪࡹࡴࠨᔭ"):
            log[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔮ")] = active[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔯ")]
    bstack1lll11l1ll_opy_.bstack1l11l11111_opy_([log])
def bstack1l1l1l1ll1_opy_():
    if len(store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᔰ")]) > 0 and store[bstackl_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᔱ")][-1]:
        return {
            bstackl_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᔲ"): bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᔳ"),
            bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔴ"): store[bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔵ")][-1]
        }
    if store.get(bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᔶ"), None):
        return {
            bstackl_opy_ (u"࠭ࡴࡺࡲࡨࠫᔷ"): bstackl_opy_ (u"ࠧࡵࡧࡶࡸࠬᔸ"),
            bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔹ"): store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᔺ")]
        }
    return None
bstack1l1l111111_opy_ = bstack1l1l1l11l1_opy_(bstack1l11ll1111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lllllllll1_opy_
        if bstack1lllllllll1_opy_:
            driver = getattr(item, bstackl_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᔻ"), None)
            bstack1l11l1l1l_opy_ = bstack1l1ll1l1ll_opy_.bstack111lll1l_opy_(CONFIG, bstack11ll1l1ll1_opy_(item.own_markers))
            item._a11y_started = bstack1l1ll1l1ll_opy_.bstack11ll1l1l_opy_(driver, bstack1l11l1l1l_opy_)
        if not bstack1lll11l1ll_opy_.on() or bstack11111ll111_opy_ != bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᔼ"):
            return
        global current_test_uuid, bstack1l1l111111_opy_
        bstack1l1l111111_opy_.start()
        bstack1l11l11l11_opy_ = {
            bstackl_opy_ (u"ࠬࡻࡵࡪࡦࠪᔽ"): uuid4().__str__(),
            bstackl_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᔾ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"࡛ࠧࠩᔿ")
        }
        current_test_uuid = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᕀ")]
        store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᕁ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᕂ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l11ll1l1l_opy_[item.nodeid] = {**_1l11ll1l1l_opy_[item.nodeid], **bstack1l11l11l11_opy_}
        bstack11111l1lll_opy_(item, _1l11ll1l1l_opy_[item.nodeid], bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕃ"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᕄ"), str(err))
def pytest_runtest_setup(item):
    if bstack11ll111lll_opy_():
        atexit.register(bstack1l111ll1_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111ll11111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᕅ")
    try:
        if not bstack1lll11l1ll_opy_.on():
            return
        bstack1l1l111111_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l11l11_opy_ = {
            bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕆ"): uuid,
            bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᕇ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫᕈ"),
            bstackl_opy_ (u"ࠪࡸࡾࡶࡥࠨᕉ"): bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᕊ"),
            bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᕋ"): bstackl_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᕌ"),
            bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᕍ"): bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᕎ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᕏ")] = item
        store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᕐ")] = [uuid]
        if not _1l11ll1l1l_opy_.get(item.nodeid, None):
            _1l11ll1l1l_opy_[item.nodeid] = {bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᕑ"): [], bstackl_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᕒ"): []}
        _1l11ll1l1l_opy_[item.nodeid][bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᕓ")].append(bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕔ")])
        _1l11ll1l1l_opy_[item.nodeid + bstackl_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᕕ")] = bstack1l11l11l11_opy_
        bstack1111111ll1_opy_(item, bstack1l11l11l11_opy_, bstackl_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᕖ"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᕗ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11l1llll1_opy_
        if getattr(item, bstackl_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᕘ"), False):
            logger.info(bstackl_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧᕙ"))
            driver = getattr(item, bstackl_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᕚ"), None)
            bstack11llll1l11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1ll1l1ll_opy_.bstack11111ll11_opy_(driver, bstack11llll1l11_opy_, item.name, item.module.__name__, item.path, bstack11l1llll1_opy_)
        if not bstack1lll11l1ll_opy_.on():
            return
        bstack1l11l11l11_opy_ = {
            bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕛ"): uuid4().__str__(),
            bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᕜ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫᕝ"),
            bstackl_opy_ (u"ࠪࡸࡾࡶࡥࠨᕞ"): bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᕟ"),
            bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᕠ"): bstackl_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᕡ"),
            bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᕢ"): bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᕣ")
        }
        _1l11ll1l1l_opy_[item.nodeid + bstackl_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᕤ")] = bstack1l11l11l11_opy_
        bstack1111111ll1_opy_(item, bstack1l11l11l11_opy_, bstackl_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᕥ"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᕦ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll11l1ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack111l1lll11_opy_(fixturedef.argname):
        store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᕧ")] = request.node
    elif bstack111l1ll1ll_opy_(fixturedef.argname):
        store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᕨ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᕩ"): fixturedef.argname,
            bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᕪ"): bstack11ll1ll1l1_opy_(outcome),
            bstackl_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᕫ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1111111111_opy_ = store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᕬ")]
        if not _1l11ll1l1l_opy_.get(bstack1111111111_opy_.nodeid, None):
            _1l11ll1l1l_opy_[bstack1111111111_opy_.nodeid] = {bstackl_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᕭ"): []}
        _1l11ll1l1l_opy_[bstack1111111111_opy_.nodeid][bstackl_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᕮ")].append(fixture)
    except Exception as err:
        logger.debug(bstackl_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᕯ"), str(err))
if bstack1lllll111l_opy_() and bstack1lll11l1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l11ll1l1l_opy_[request.node.nodeid][bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᕰ")].bstack1111ll1ll1_opy_(id(step))
        except Exception as err:
            print(bstackl_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᕱ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l11ll1l1l_opy_[request.node.nodeid][bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᕲ")].bstack1l11lll111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᕳ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11l111l1_opy_: bstack1l11l1lll1_opy_ = _1l11ll1l1l_opy_[request.node.nodeid][bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᕴ")]
            bstack1l11l111l1_opy_.bstack1l11lll111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᕵ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111ll111_opy_
        try:
            if not bstack1lll11l1ll_opy_.on() or bstack11111ll111_opy_ != bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᕶ"):
                return
            global bstack1l1l111111_opy_
            bstack1l1l111111_opy_.start()
            if not _1l11ll1l1l_opy_.get(request.node.nodeid, None):
                _1l11ll1l1l_opy_[request.node.nodeid] = {}
            bstack1l11l111l1_opy_ = bstack1l11l1lll1_opy_.bstack1111l1lll1_opy_(
                scenario, feature, request.node,
                name=bstack111ll1111l_opy_(request.node, scenario),
                bstack1l11llllll_opy_=bstack111l11lll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstackl_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᕷ"),
                tags=bstack111l1lll1l_opy_(feature, scenario)
            )
            _1l11ll1l1l_opy_[request.node.nodeid][bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᕸ")] = bstack1l11l111l1_opy_
            bstack111111l1ll_opy_(bstack1l11l111l1_opy_.uuid)
            bstack1lll11l1ll_opy_.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᕹ"), bstack1l11l111l1_opy_)
        except Exception as err:
            print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᕺ"), str(err))
def bstack1111111lll_opy_(bstack111111lll1_opy_):
    if bstack111111lll1_opy_ in store[bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᕻ")]:
        store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᕼ")].remove(bstack111111lll1_opy_)
def bstack111111l1ll_opy_(bstack111111l11l_opy_):
    store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᕽ")] = bstack111111l11l_opy_
    threading.current_thread().current_test_uuid = bstack111111l11l_opy_
@bstack1lll11l1ll_opy_.bstack1111l11111_opy_
def bstack11111111l1_opy_(item, call, report):
    global bstack11111ll111_opy_
    try:
        if report.when == bstackl_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᕾ"):
            bstack1l1l111111_opy_.reset()
        if report.when == bstackl_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᕿ"):
            if bstack11111ll111_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᖀ"):
                _1l11ll1l1l_opy_[item.nodeid][bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᖁ")] = bstack11ll1111l1_opy_(report.stop)
                bstack11111l1lll_opy_(item, _1l11ll1l1l_opy_[item.nodeid], bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖂ"), report, call)
                store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖃ")] = None
            elif bstack11111ll111_opy_ == bstackl_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᖄ"):
                bstack1l11l111l1_opy_ = _1l11ll1l1l_opy_[item.nodeid][bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᖅ")]
                bstack1l11l111l1_opy_.set(hooks=_1l11ll1l1l_opy_[item.nodeid].get(bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖆ"), []))
                exception, bstack1l1l1l1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l1l1111_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l11l111l1_opy_.stop(time=bstack11ll1111l1_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1l1l1111_opy_=bstack1l1l1l1111_opy_))
                bstack1lll11l1ll_opy_.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᖇ"), _1l11ll1l1l_opy_[item.nodeid][bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᖈ")])
        elif report.when in [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᖉ"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᖊ")]:
            bstack1l1l11llll_opy_ = item.nodeid + bstackl_opy_ (u"࠭࠭ࠨᖋ") + report.when
            if report.skipped:
                hook_type = bstackl_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖌ") if report.when == bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᖍ") else bstackl_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᖎ")
                _1l11ll1l1l_opy_[bstack1l1l11llll_opy_] = {
                    bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖏ"): uuid4().__str__(),
                    bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᖐ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstackl_opy_ (u"ࠬࡠࠧᖑ"),
                    bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᖒ"): hook_type
                }
            _1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖓ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstackl_opy_ (u"ࠨ࡜ࠪᖔ")
            bstack1111111lll_opy_(_1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖕ")])
            bstack1111111ll1_opy_(item, _1l11ll1l1l_opy_[bstack1l1l11llll_opy_], bstackl_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᖖ"), report, call)
            if report.when == bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᖗ"):
                if report.outcome == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᖘ"):
                    bstack1l11l11l11_opy_ = {
                        bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖙ"): uuid4().__str__(),
                        bstackl_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᖚ"): bstack111l11lll_opy_(),
                        bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᖛ"): bstack111l11lll_opy_()
                    }
                    _1l11ll1l1l_opy_[item.nodeid] = {**_1l11ll1l1l_opy_[item.nodeid], **bstack1l11l11l11_opy_}
                    bstack11111l1lll_opy_(item, _1l11ll1l1l_opy_[item.nodeid], bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᖜ"))
                    bstack11111l1lll_opy_(item, _1l11ll1l1l_opy_[item.nodeid], bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᖝ"), report, call)
    except Exception as err:
        print(bstackl_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩᖞ"), str(err))
def bstack111111llll_opy_(test, bstack1l11l11l11_opy_, result=None, call=None, bstack111l111l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l111l1_opy_ = {
        bstackl_opy_ (u"ࠬࡻࡵࡪࡦࠪᖟ"): bstack1l11l11l11_opy_[bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖠ")],
        bstackl_opy_ (u"ࠧࡵࡻࡳࡩࠬᖡ"): bstackl_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᖢ"),
        bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᖣ"): test.name,
        bstackl_opy_ (u"ࠪࡦࡴࡪࡹࠨᖤ"): {
            bstackl_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᖥ"): bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᖦ"),
            bstackl_opy_ (u"࠭ࡣࡰࡦࡨࠫᖧ"): inspect.getsource(test.obj)
        },
        bstackl_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᖨ"): test.name,
        bstackl_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᖩ"): test.name,
        bstackl_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᖪ"): bstack1lll11l1ll_opy_.bstack1l1l1ll11l_opy_(test),
        bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᖫ"): file_path,
        bstackl_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᖬ"): file_path,
        bstackl_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᖭ"): bstackl_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᖮ"),
        bstackl_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᖯ"): file_path,
        bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖰ"): bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖱ")],
        bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᖲ"): bstackl_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᖳ"),
        bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᖴ"): {
            bstackl_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᖵ"): test.nodeid
        },
        bstackl_opy_ (u"ࠧࡵࡣࡪࡷࠬᖶ"): bstack11ll1l1ll1_opy_(test.own_markers)
    }
    if bstack111l111l1_opy_ in [bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᖷ"), bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᖸ")]:
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠪࡱࡪࡺࡡࠨᖹ")] = {
            bstackl_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᖺ"): bstack1l11l11l11_opy_.get(bstackl_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᖻ"), [])
        }
    if bstack111l111l1_opy_ == bstackl_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᖼ"):
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᖽ")] = bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᖾ")
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖿ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᗀ")]
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗁ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗂ")]
    if result:
        bstack1l11l111l1_opy_[bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗃ")] = result.outcome
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᗄ")] = result.duration * 1000
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗅ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗆ")]
        if result.failed:
            bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᗇ")] = bstack1lll11l1ll_opy_.bstack1l1111l1l1_opy_(call.excinfo.typename)
            bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᗈ")] = bstack1lll11l1ll_opy_.bstack1111l1l111_opy_(call.excinfo, result)
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᗉ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᗊ")]
    if outcome:
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᗋ")] = bstack11ll1ll1l1_opy_(outcome)
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᗌ")] = 0
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗍ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗎ")]
        if bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᗏ")] == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗐ"):
            bstack1l11l111l1_opy_[bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᗑ")] = bstackl_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᗒ")  # bstack11111l111l_opy_
            bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᗓ")] = [{bstackl_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗔ"): [bstackl_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᗕ")]}]
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᗖ")] = bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᗗ")]
    return bstack1l11l111l1_opy_
def bstack11111l1111_opy_(test, bstack1l11lll11l_opy_, bstack111l111l1_opy_, result, call, outcome, bstack111111ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11lll11l_opy_[bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᗘ")]
    hook_name = bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᗙ")]
    hook_data = {
        bstackl_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᗚ"): bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗛ")],
        bstackl_opy_ (u"ࠪࡸࡾࡶࡥࠨᗜ"): bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᗝ"),
        bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᗞ"): bstackl_opy_ (u"࠭ࡻࡾࠩᗟ").format(bstack111l1l1ll1_opy_(hook_name)),
        bstackl_opy_ (u"ࠧࡣࡱࡧࡽࠬᗠ"): {
            bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᗡ"): bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᗢ"),
            bstackl_opy_ (u"ࠪࡧࡴࡪࡥࠨᗣ"): None
        },
        bstackl_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᗤ"): test.name,
        bstackl_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᗥ"): bstack1lll11l1ll_opy_.bstack1l1l1ll11l_opy_(test, hook_name),
        bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᗦ"): file_path,
        bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᗧ"): file_path,
        bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᗨ"): bstackl_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᗩ"),
        bstackl_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᗪ"): file_path,
        bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᗫ"): bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗬ")],
        bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᗭ"): bstackl_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᗮ") if bstack11111ll111_opy_ == bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᗯ") else bstackl_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᗰ"),
        bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᗱ"): hook_type
    }
    bstack1lllllll1ll_opy_ = bstack1l11ll11ll_opy_(_1l11ll1l1l_opy_.get(test.nodeid, None))
    if bstack1lllllll1ll_opy_:
        hook_data[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᗲ")] = bstack1lllllll1ll_opy_
    if result:
        hook_data[bstackl_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᗳ")] = result.outcome
        hook_data[bstackl_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᗴ")] = result.duration * 1000
        hook_data[bstackl_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᗵ")] = bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗶ")]
        if result.failed:
            hook_data[bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᗷ")] = bstack1lll11l1ll_opy_.bstack1l1111l1l1_opy_(call.excinfo.typename)
            hook_data[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᗸ")] = bstack1lll11l1ll_opy_.bstack1111l1l111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstackl_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᗹ")] = bstack11ll1ll1l1_opy_(outcome)
        hook_data[bstackl_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᗺ")] = 100
        hook_data[bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᗻ")] = bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᗼ")]
        if hook_data[bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᗽ")] == bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗾ"):
            hook_data[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᗿ")] = bstackl_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᘀ")  # bstack11111l111l_opy_
            hook_data[bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᘁ")] = [{bstackl_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᘂ"): [bstackl_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᘃ")]}]
    if bstack111111ll1l_opy_:
        hook_data[bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘄ")] = bstack111111ll1l_opy_.result
        hook_data[bstackl_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᘅ")] = bstack11ll11l11l_opy_(bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘆ")], bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘇ")])
        hook_data[bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘈ")] = bstack1l11lll11l_opy_[bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘉ")]
        if hook_data[bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘊ")] == bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᘋ"):
            hook_data[bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᘌ")] = bstack1lll11l1ll_opy_.bstack1l1111l1l1_opy_(bstack111111ll1l_opy_.exception_type)
            hook_data[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᘍ")] = [{bstackl_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᘎ"): bstack11l1ll1lll_opy_(bstack111111ll1l_opy_.exception)}]
    return hook_data
def bstack11111l1lll_opy_(test, bstack1l11l11l11_opy_, bstack111l111l1_opy_, result=None, call=None, outcome=None):
    bstack1l11l111l1_opy_ = bstack111111llll_opy_(test, bstack1l11l11l11_opy_, result, call, bstack111l111l1_opy_, outcome)
    driver = getattr(test, bstackl_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᘏ"), None)
    if bstack111l111l1_opy_ == bstackl_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᘐ") and driver:
        bstack1l11l111l1_opy_[bstackl_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᘑ")] = bstack1lll11l1ll_opy_.bstack1l1l11l1ll_opy_(driver)
    if bstack111l111l1_opy_ == bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᘒ"):
        bstack111l111l1_opy_ = bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᘓ")
    bstack1l1l111l11_opy_ = {
        bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᘔ"): bstack111l111l1_opy_,
        bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᘕ"): bstack1l11l111l1_opy_
    }
    bstack1lll11l1ll_opy_.bstack1l1l11ll1l_opy_(bstack1l1l111l11_opy_)
def bstack1111111ll1_opy_(test, bstack1l11l11l11_opy_, bstack111l111l1_opy_, result=None, call=None, outcome=None, bstack111111ll1l_opy_=None):
    hook_data = bstack11111l1111_opy_(test, bstack1l11l11l11_opy_, bstack111l111l1_opy_, result, call, outcome, bstack111111ll1l_opy_)
    bstack1l1l111l11_opy_ = {
        bstackl_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᘖ"): bstack111l111l1_opy_,
        bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᘗ"): hook_data
    }
    bstack1lll11l1ll_opy_.bstack1l1l11ll1l_opy_(bstack1l1l111l11_opy_)
def bstack1l11ll11ll_opy_(bstack1l11l11l11_opy_):
    if not bstack1l11l11l11_opy_:
        return None
    if bstack1l11l11l11_opy_.get(bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᘘ"), None):
        return getattr(bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᘙ")], bstackl_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘚ"), None)
    return bstack1l11l11l11_opy_.get(bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘛ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lll11l1ll_opy_.on():
            return
        places = [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᘜ"), bstackl_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᘝ"), bstackl_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᘞ")]
        bstack1l1l1l111l_opy_ = []
        for bstack111111l111_opy_ in places:
            records = caplog.get_records(bstack111111l111_opy_)
            bstack111111l1l1_opy_ = bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘟ") if bstack111111l111_opy_ == bstackl_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᘠ") else bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘡ")
            bstack1111111l11_opy_ = request.node.nodeid + (bstackl_opy_ (u"ࠪࠫᘢ") if bstack111111l111_opy_ == bstackl_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᘣ") else bstackl_opy_ (u"ࠬ࠳ࠧᘤ") + bstack111111l111_opy_)
            bstack111111l11l_opy_ = bstack1l11ll11ll_opy_(_1l11ll1l1l_opy_.get(bstack1111111l11_opy_, None))
            if not bstack111111l11l_opy_:
                continue
            for record in records:
                if bstack11ll11lll1_opy_(record.message):
                    continue
                bstack1l1l1l111l_opy_.append({
                    bstackl_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᘥ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstackl_opy_ (u"࡛ࠧࠩᘦ"),
                    bstackl_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᘧ"): record.levelname,
                    bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘨ"): record.message,
                    bstack111111l1l1_opy_: bstack111111l11l_opy_
                })
        if len(bstack1l1l1l111l_opy_) > 0:
            bstack1lll11l1ll_opy_.bstack1l11l11111_opy_(bstack1l1l1l111l_opy_)
    except Exception as err:
        print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᘩ"), str(err))
def bstack11lll1111_opy_(driver_command, response):
    if driver_command == bstackl_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᘪ"):
        bstack1lll11l1ll_opy_.bstack1ll1lll1l1_opy_({
            bstackl_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᘫ"): response[bstackl_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᘬ")],
            bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘭ"): store[bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᘮ")]
        })
def bstack1l111ll1_opy_():
    global bstack1ll1ll1lll_opy_
    bstack1lll11l1ll_opy_.bstack1l1l11111l_opy_()
    for driver in bstack1ll1ll1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11lllll_opy_(self, *args, **kwargs):
    bstack1l11lllll_opy_ = bstack1l1l11111_opy_(self, *args, **kwargs)
    bstack1lll11l1ll_opy_.bstack1ll111l111_opy_(self)
    return bstack1l11lllll_opy_
def bstack1lll1ll1l1_opy_(framework_name):
    global bstack111lllll1_opy_
    global bstack1lll11l111_opy_
    bstack111lllll1_opy_ = framework_name
    logger.info(bstack1l11ll11_opy_.format(bstack111lllll1_opy_.split(bstackl_opy_ (u"ࠩ࠰ࠫᘯ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11lll111ll_opy_():
            Service.start = bstack11ll1ll11_opy_
            Service.stop = bstack1ll11l11_opy_
            webdriver.Remote.__init__ = bstack1lll1lll11_opy_
            webdriver.Remote.get = bstack111l11ll_opy_
            if not isinstance(os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᘰ")), str):
                return
            WebDriver.close = bstack1l1ll11ll_opy_
            WebDriver.quit = bstack1ll1lllll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1ll1l1ll_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1111llll_opy_ = getAccessibilityResultsSummary
        if not bstack11lll111ll_opy_() and bstack1lll11l1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1ll11lllll_opy_
        bstack1lll11l111_opy_ = True
    except Exception as e:
        pass
    bstack1ll11ll11_opy_()
    if os.environ.get(bstackl_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᘱ")):
        bstack1lll11l111_opy_ = eval(os.environ.get(bstackl_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᘲ")))
    if not bstack1lll11l111_opy_:
        bstack1ll1l11111_opy_(bstackl_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᘳ"), bstack1111111l1_opy_)
    if bstack1ll11l1ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l111l111_opy_
        except Exception as e:
            logger.error(bstack1lll1l1l1l_opy_.format(str(e)))
    if bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᘴ") in str(framework_name).lower():
        if not bstack11lll111ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1111l1l1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lll11ll_opy_
            Config.getoption = bstack1lll111l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1llll1ll1_opy_
        except Exception as e:
            pass
def bstack1ll1lllll_opy_(self):
    global bstack111lllll1_opy_
    global bstack11ll111l1_opy_
    global bstack111lll1l1_opy_
    try:
        if bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᘵ") in bstack111lllll1_opy_ and self.session_id != None and bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᘶ"), bstackl_opy_ (u"ࠪࠫᘷ")) != bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᘸ"):
            bstack111l1l1l_opy_ = bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᘹ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᘺ")
            bstack111l111ll_opy_(logger, True)
            if self != None:
                bstack11l1ll111_opy_(self, bstack111l1l1l_opy_, bstackl_opy_ (u"ࠧ࠭ࠢࠪᘻ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstackl_opy_ (u"ࠨࠩᘼ")
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥᘽ") + str(e))
    bstack111lll1l1_opy_(self)
    self.session_id = None
def bstack1lll1lll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll111l1_opy_
    global bstack111111l1l_opy_
    global bstack1111lll1l_opy_
    global bstack111lllll1_opy_
    global bstack1l1l11111_opy_
    global bstack1ll1ll1lll_opy_
    global bstack1l1111111_opy_
    global bstack11lllllll_opy_
    global bstack1lllllllll1_opy_
    global bstack11l1llll1_opy_
    CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᘾ")] = str(bstack111lllll1_opy_) + str(__version__)
    command_executor = bstack1ll11l1111_opy_(bstack1l1111111_opy_)
    logger.debug(bstack1lll1lll1l_opy_.format(command_executor))
    proxy = bstack111111l1_opy_(CONFIG, proxy)
    bstack11l1l1l11_opy_ = 0
    try:
        if bstack1111lll1l_opy_ is True:
            bstack11l1l1l11_opy_ = int(os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᘿ")))
    except:
        bstack11l1l1l11_opy_ = 0
    bstack1l11ll1ll_opy_ = bstack11ll1l111_opy_(CONFIG, bstack11l1l1l11_opy_)
    logger.debug(bstack1ll1l111_opy_.format(str(bstack1l11ll1ll_opy_)))
    bstack11l1llll1_opy_ = CONFIG.get(bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᙀ"))[bstack11l1l1l11_opy_]
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᙁ") in CONFIG and CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᙂ")]:
        bstack1111lll1_opy_(bstack1l11ll1ll_opy_, bstack11lllllll_opy_)
    if desired_capabilities:
        bstack111l111l_opy_ = bstack1l1l1llll_opy_(desired_capabilities)
        bstack111l111l_opy_[bstackl_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᙃ")] = bstack111ll11l_opy_(CONFIG)
        bstack1l11l1l11_opy_ = bstack11ll1l111_opy_(bstack111l111l_opy_)
        if bstack1l11l1l11_opy_:
            bstack1l11ll1ll_opy_ = update(bstack1l11l1l11_opy_, bstack1l11ll1ll_opy_)
        desired_capabilities = None
    if options:
        bstack11111111_opy_(options, bstack1l11ll1ll_opy_)
    if not options:
        options = bstack1ll11l1l1l_opy_(bstack1l11ll1ll_opy_)
    if bstack1l1ll1l1ll_opy_.bstack1ll111lll_opy_(CONFIG, bstack11l1l1l11_opy_) and bstack1l1ll1l1ll_opy_.bstack11l1l111_opy_(bstack1l11ll1ll_opy_, options):
        bstack1lllllllll1_opy_ = True
        bstack1l1ll1l1ll_opy_.set_capabilities(bstack1l11ll1ll_opy_, CONFIG)
    if proxy and bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᙄ")):
        options.proxy(proxy)
    if options and bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᙅ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1l1ll_opy_() < version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᙆ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11ll1ll_opy_)
    logger.info(bstack11ll1l11_opy_)
    if bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᙇ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᙈ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᙉ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll1llll1_opy_ = bstackl_opy_ (u"ࠨࠩᙊ")
        if bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪᙋ")):
            bstack1ll1llll1_opy_ = self.caps.get(bstackl_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥᙌ"))
        else:
            bstack1ll1llll1_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᙍ"))
        if bstack1ll1llll1_opy_:
            bstack11l1l111l_opy_(bstack1ll1llll1_opy_)
            if bstack11l1l1ll_opy_() <= version.parse(bstackl_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᙎ")):
                self.command_executor._url = bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᙏ") + bstack1l1111111_opy_ + bstackl_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᙐ")
            else:
                self.command_executor._url = bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᙑ") + bstack1ll1llll1_opy_ + bstackl_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᙒ")
            logger.debug(bstack11ll11ll_opy_.format(bstack1ll1llll1_opy_))
        else:
            logger.debug(bstack1llllll1ll_opy_.format(bstackl_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᙓ")))
    except Exception as e:
        logger.debug(bstack1llllll1ll_opy_.format(e))
    bstack11ll111l1_opy_ = self.session_id
    if bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᙔ") in bstack111lllll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1lll11l1ll_opy_.bstack1ll111l111_opy_(self)
    bstack1ll1ll1lll_opy_.append(self)
    if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᙕ") in CONFIG and bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙖ") in CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙗ")][bstack11l1l1l11_opy_]:
        bstack111111l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᙘ")][bstack11l1l1l11_opy_][bstackl_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᙙ")]
    logger.debug(bstack1ll1111l1l_opy_.format(bstack11ll111l1_opy_))
def bstack111l11ll_opy_(self, url):
    global bstack1l1l1l1l1_opy_
    global CONFIG
    try:
        bstack111llll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1lllll_opy_.format(str(err)))
    try:
        bstack1l1l1l1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack11111ll1l_opy_ = str(e)
            if any(err_msg in bstack11111ll1l_opy_ for err_msg in bstack1lll1111l1_opy_):
                bstack111llll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1lllll_opy_.format(str(err)))
        raise e
def bstack1ll1l1ll1_opy_(item, when):
    global bstack1l1l111ll_opy_
    try:
        bstack1l1l111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll1ll1_opy_(item, call, rep):
    global bstack1llll1ll_opy_
    global bstack1ll1ll1lll_opy_
    name = bstackl_opy_ (u"ࠪࠫᙚ")
    try:
        if rep.when == bstackl_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᙛ"):
            bstack11ll111l1_opy_ = threading.current_thread().bstackSessionId
            bstack111111ll11_opy_ = item.config.getoption(bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᙜ"))
            try:
                if (str(bstack111111ll11_opy_).lower() != bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫᙝ")):
                    name = str(rep.nodeid)
                    bstack1ll11l111_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᙞ"), name, bstackl_opy_ (u"ࠨࠩᙟ"), bstackl_opy_ (u"ࠩࠪᙠ"), bstackl_opy_ (u"ࠪࠫᙡ"), bstackl_opy_ (u"ࠫࠬᙢ"))
                    os.environ[bstackl_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᙣ")] = name
                    for driver in bstack1ll1ll1lll_opy_:
                        if bstack11ll111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11l111_opy_)
            except Exception as e:
                logger.debug(bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᙤ").format(str(e)))
            try:
                bstack1l111111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᙥ"):
                    status = bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᙦ") if rep.outcome.lower() == bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙧ") else bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙨ")
                    reason = bstackl_opy_ (u"ࠫࠬᙩ")
                    if status == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᙪ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstackl_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᙫ") if status == bstackl_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᙬ") else bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᙭")
                    data = name + bstackl_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ᙮") if status == bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙯ") else name + bstackl_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧᙰ") + reason
                    bstack1lllll1ll_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᙱ"), bstackl_opy_ (u"࠭ࠧᙲ"), bstackl_opy_ (u"ࠧࠨᙳ"), bstackl_opy_ (u"ࠨࠩᙴ"), level, data)
                    for driver in bstack1ll1ll1lll_opy_:
                        if bstack11ll111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lllll1ll_opy_)
            except Exception as e:
                logger.debug(bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᙵ").format(str(e)))
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧᙶ").format(str(e)))
    bstack1llll1ll_opy_(item, call, rep)
notset = Notset()
def bstack1lll111l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l11lll_opy_
    if str(name).lower() == bstackl_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᙷ"):
        return bstackl_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᙸ")
    else:
        return bstack1l1l11lll_opy_(self, name, default, skip)
def bstack1l111l111_opy_(self):
    global CONFIG
    global bstack1l111ll11_opy_
    try:
        proxy = bstack1l1ll1ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstackl_opy_ (u"࠭࠮ࡱࡣࡦࠫᙹ")):
                proxies = bstack1llll1111l_opy_(proxy, bstack1ll11l1111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1ll1l1l_opy_ = proxies.popitem()
                    if bstackl_opy_ (u"ࠢ࠻࠱࠲ࠦᙺ") in bstack1l1ll1l1l_opy_:
                        return bstack1l1ll1l1l_opy_
                    else:
                        return bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᙻ") + bstack1l1ll1l1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨᙼ").format(str(e)))
    return bstack1l111ll11_opy_(self)
def bstack1ll11l1ll1_opy_():
    return (bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᙽ") in CONFIG or bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᙾ") in CONFIG) and bstack1l1l1ll1l_opy_() and bstack11l1l1ll_opy_() >= version.parse(
        bstack1ll11lll_opy_)
def bstack1ll1lllll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack111111l1l_opy_
    global bstack1111lll1l_opy_
    global bstack111lllll1_opy_
    CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᙿ")] = str(bstack111lllll1_opy_) + str(__version__)
    bstack11l1l1l11_opy_ = 0
    try:
        if bstack1111lll1l_opy_ is True:
            bstack11l1l1l11_opy_ = int(os.environ.get(bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ ")))
    except:
        bstack11l1l1l11_opy_ = 0
    CONFIG[bstackl_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᚁ")] = True
    bstack1l11ll1ll_opy_ = bstack11ll1l111_opy_(CONFIG, bstack11l1l1l11_opy_)
    logger.debug(bstack1ll1l111_opy_.format(str(bstack1l11ll1ll_opy_)))
    if CONFIG.get(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚂ")):
        bstack1111lll1_opy_(bstack1l11ll1ll_opy_, bstack11lllllll_opy_)
    if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚃ") in CONFIG and bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᚄ") in CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᚅ")][bstack11l1l1l11_opy_]:
        bstack111111l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᚆ")][bstack11l1l1l11_opy_][bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᚇ")]
    import urllib
    import json
    bstack1lll1l1l_opy_ = bstackl_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩᚈ") + urllib.parse.quote(json.dumps(bstack1l11ll1ll_opy_))
    browser = self.connect(bstack1lll1l1l_opy_)
    return browser
def bstack1ll11ll11_opy_():
    global bstack1lll11l111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1lllll1_opy_
        bstack1lll11l111_opy_ = True
    except Exception as e:
        pass
def bstack11111l11l1_opy_():
    global CONFIG
    global bstack1l11ll111_opy_
    global bstack1l1111111_opy_
    global bstack11lllllll_opy_
    global bstack1111lll1l_opy_
    CONFIG = json.loads(os.environ.get(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧᚉ")))
    bstack1l11ll111_opy_ = eval(os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᚊ")))
    bstack1l1111111_opy_ = os.environ.get(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪᚋ"))
    bstack111l1ll1l_opy_(CONFIG, bstack1l11ll111_opy_)
    bstack1ll11lll1_opy_()
    global bstack1l1l11111_opy_
    global bstack111lll1l1_opy_
    global bstack11ll1ll1l_opy_
    global bstack1llll11l1l_opy_
    global bstack1lll1111ll_opy_
    global bstack1lll1111l_opy_
    global bstack1ll1l11l11_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1l111ll11_opy_
    global bstack1l1l11lll_opy_
    global bstack1l1l111ll_opy_
    global bstack1llll1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l11111_opy_ = webdriver.Remote.__init__
        bstack111lll1l1_opy_ = WebDriver.quit
        bstack1ll1l11l11_opy_ = WebDriver.close
        bstack1l1l1l1l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᚌ") in CONFIG or bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᚍ") in CONFIG) and bstack1l1l1ll1l_opy_():
        if bstack11l1l1ll_opy_() < version.parse(bstack1ll11lll_opy_):
            logger.error(bstack11lll1ll_opy_.format(bstack11l1l1ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111ll11_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1lll1l1l1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1l11lll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1111l1ll1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧᚎ"))
    bstack11lllllll_opy_ = CONFIG.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᚏ"), {}).get(bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚐ"))
    bstack1111lll1l_opy_ = True
    bstack1lll1ll1l1_opy_(bstack1l1l1lll1_opy_)
if (bstack11ll111lll_opy_()):
    bstack11111l11l1_opy_()
@bstack1l1l11l11l_opy_(class_method=False)
def bstack11111l1ll1_opy_(hook_name, event, bstack1llllllllll_opy_=None):
    if hook_name not in [bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᚑ"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᚒ"), bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᚓ"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᚔ"), bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᚕ"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᚖ"), bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᚗ"), bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᚘ")]:
        return
    node = store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᚙ")]
    if hook_name in [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᚚ"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ᚛")]:
        node = store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ᚜")]
    elif hook_name in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ᚝"), bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ᚞")]:
        node = store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ᚟")]
    if event == bstackl_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᚠ"):
        hook_type = bstack111l1lllll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11lll11l_opy_ = {
            bstackl_opy_ (u"ࠫࡺࡻࡩࡥࠩᚡ"): uuid,
            bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᚢ"): bstack111l11lll_opy_(),
            bstackl_opy_ (u"࠭ࡴࡺࡲࡨࠫᚣ"): bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᚤ"),
            bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᚥ"): hook_type,
            bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᚦ"): hook_name
        }
        store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᚧ")].append(uuid)
        bstack111111111l_opy_ = node.nodeid
        if hook_type == bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᚨ"):
            if not _1l11ll1l1l_opy_.get(bstack111111111l_opy_, None):
                _1l11ll1l1l_opy_[bstack111111111l_opy_] = {bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᚩ"): []}
            _1l11ll1l1l_opy_[bstack111111111l_opy_][bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᚪ")].append(bstack1l11lll11l_opy_[bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚫ")])
        _1l11ll1l1l_opy_[bstack111111111l_opy_ + bstackl_opy_ (u"ࠨ࠯ࠪᚬ") + hook_name] = bstack1l11lll11l_opy_
        bstack1111111ll1_opy_(node, bstack1l11lll11l_opy_, bstackl_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᚭ"))
    elif event == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᚮ"):
        bstack1l1l11llll_opy_ = node.nodeid + bstackl_opy_ (u"ࠫ࠲࠭ᚯ") + hook_name
        _1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚰ")] = bstack111l11lll_opy_()
        bstack1111111lll_opy_(_1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚱ")])
        bstack1111111ll1_opy_(node, _1l11ll1l1l_opy_[bstack1l1l11llll_opy_], bstackl_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᚲ"), bstack111111ll1l_opy_=bstack1llllllllll_opy_)
def bstack1llllllll1l_opy_():
    global bstack11111ll111_opy_
    if bstack1lllll111l_opy_():
        bstack11111ll111_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᚳ")
    else:
        bstack11111ll111_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᚴ")
@bstack1lll11l1ll_opy_.bstack1111l11111_opy_
def bstack1111111l1l_opy_():
    bstack1llllllll1l_opy_()
    if bstack1l1l1ll1l_opy_():
        bstack11l111ll1_opy_(bstack11lll1111_opy_)
    bstack11l1l11lll_opy_ = bstack11l1l1l11l_opy_(bstack11111l1ll1_opy_)
bstack1111111l1l_opy_()