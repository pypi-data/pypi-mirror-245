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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack1lll1ll1ll_opy_():
  global CONFIG
  headers = {
        bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll1l1l1l_opy_(CONFIG, bstack1llllll111_opy_)
  try:
    response = requests.get(bstack1llllll111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l1l1l_opy_ = response.json()[bstackl_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1111l1l_opy_.format(response.json()))
      return bstack1l1l1l1l_opy_
    else:
      logger.debug(bstack111l1ll11_opy_.format(bstackl_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l1ll11_opy_.format(e))
def bstack1lll1111_opy_(hub_url):
  global CONFIG
  url = bstackl_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstackl_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1llll1l1l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll111l11_opy_.format(hub_url, e))
def bstack1111l1l1l_opy_():
  try:
    global bstack1l1111111_opy_
    bstack1l1l1l1l_opy_ = bstack1lll1ll1ll_opy_()
    bstack111l1llll_opy_ = []
    results = []
    for bstack1l1ll1l1l1_opy_ in bstack1l1l1l1l_opy_:
      bstack111l1llll_opy_.append(bstack1l1lll11l1_opy_(target=bstack1lll1111_opy_,args=(bstack1l1ll1l1l1_opy_,)))
    for t in bstack111l1llll_opy_:
      t.start()
    for t in bstack111l1llll_opy_:
      results.append(t.join())
    bstack111111l11_opy_ = {}
    for item in results:
      hub_url = item[bstackl_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstackl_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack111111l11_opy_[hub_url] = latency
    bstack1ll1111l11_opy_ = min(bstack111111l11_opy_, key= lambda x: bstack111111l11_opy_[x])
    bstack1l1111111_opy_ = bstack1ll1111l11_opy_
    logger.debug(bstack1ll1l1ll11_opy_.format(bstack1ll1111l11_opy_))
  except Exception as e:
    logger.debug(bstack1l1lllll1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l111l1l_opy_, bstack1ll11l1l1_opy_, bstack11l1l11ll_opy_, bstack1ll1ll1111_opy_, Notset, bstack111ll11l_opy_, \
  bstack1l1l1l1ll_opy_, bstack1lll11lll_opy_, bstack11l11l1l_opy_, bstack11ll1lll_opy_, bstack1lllll111l_opy_, bstack1l1l1ll1l_opy_, bstack1l1lll1l1_opy_, \
  bstack1111l11ll_opy_, bstack11lll11l_opy_, bstack11l1l111l_opy_, bstack1l11l1ll_opy_, bstack111l111ll_opy_, bstack1l11111l_opy_, \
  bstack1111l11l1_opy_, bstack11llll111_opy_
from bstack_utils.bstack1llll11ll1_opy_ import bstack11l111ll1_opy_
from bstack_utils.bstack1ll1l1l1_opy_ import bstack11l1ll111_opy_, bstack1l11l1ll1_opy_
from bstack_utils.bstack11ll11l11_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.proxy import bstack1llll1111l_opy_, bstack1ll1l1l1l_opy_, bstack1l1ll1ll11_opy_, bstack1lllll11l1_opy_
import bstack_utils.bstack1llllll1l1_opy_ as bstack1l1ll1l1ll_opy_
from browserstack_sdk.bstack1l1l11ll_opy_ import *
from browserstack_sdk.bstack1ll111l1l1_opy_ import *
from bstack_utils.bstack11ll11l1_opy_ import bstack1l111111_opy_
bstack11l1lll11_opy_ = bstackl_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11llll11_opy_ = bstackl_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack11lllll1l_opy_ = None
CONFIG = {}
bstack1llll1ll11_opy_ = {}
bstack11lll111l_opy_ = {}
bstack11ll111l1_opy_ = None
bstack11l1lll1_opy_ = None
bstack111111l1l_opy_ = None
bstack1ll1l111l_opy_ = -1
bstack1l1l1l11_opy_ = 0
bstack11ll1111l_opy_ = bstack1ll1ll11l_opy_
bstack11l11l11_opy_ = 1
bstack1111lll1l_opy_ = False
bstack1l1ll1l111_opy_ = False
bstack111lllll1_opy_ = bstackl_opy_ (u"ࠨࠩࢂ")
bstack11lllllll_opy_ = bstackl_opy_ (u"ࠩࠪࢃ")
bstack1l11ll111_opy_ = False
bstack1l11ll1l1_opy_ = True
bstack1l111lll_opy_ = bstackl_opy_ (u"ࠪࠫࢄ")
bstack1ll1ll1lll_opy_ = []
bstack1l1111111_opy_ = bstackl_opy_ (u"ࠫࠬࢅ")
bstack1lll11l111_opy_ = False
bstack1llll111ll_opy_ = None
bstack11ll11111_opy_ = None
bstack1lllll11l_opy_ = -1
bstack11l1l1lll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧࢆ")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstackl_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll111111l_opy_ = 0
bstack1llllll11_opy_ = []
bstack11l11ll1_opy_ = []
bstack1ll1l1l1l1_opy_ = []
bstack1l11lll1_opy_ = []
bstack1lll111ll1_opy_ = bstackl_opy_ (u"ࠨࠩࢉ")
bstack11ll111l_opy_ = bstackl_opy_ (u"ࠩࠪࢊ")
bstack1llll1l11l_opy_ = False
bstack1ll1l1l111_opy_ = False
bstack11l1llll1_opy_ = {}
bstack1l1l11111_opy_ = None
bstack111lll1l1_opy_ = None
bstack1ll1111l1_opy_ = None
bstack1l1lll111l_opy_ = None
bstack1l1l111l_opy_ = None
bstack11ll1ll1l_opy_ = None
bstack1llll11l1l_opy_ = None
bstack111l11111_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1lll1111l_opy_ = None
bstack1l111ll11_opy_ = None
bstack1ll1l11l11_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack11l11ll11_opy_ = None
bstack1l1l11lll_opy_ = None
bstack1l1l111ll_opy_ = None
bstack1l1111lll_opy_ = None
bstack1llll1ll_opy_ = None
bstack11111lll_opy_ = None
bstack11l11111_opy_ = bstackl_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11ll1111l_opy_,
                    format=bstackl_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstackl_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1l1ll111l1_opy_ = Config.get_instance()
percy = bstack1ll1l1111l_opy_()
def bstack1ll11lll1_opy_():
  global CONFIG
  global bstack11ll1111l_opy_
  if bstackl_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack11ll1111l_opy_ = bstack1ll1l1llll_opy_[CONFIG[bstackl_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack11ll1111l_opy_)
def bstack1ll1lll11l_opy_():
  global CONFIG
  global bstack1llll1l11l_opy_
  global bstack1l1ll111l1_opy_
  bstack1111ll111_opy_ = bstack11l1ll1ll_opy_(CONFIG)
  if (bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1111ll111_opy_ and str(bstack1111ll111_opy_[bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1llll1l11l_opy_ = True
  bstack1l1ll111l1_opy_.bstack1111111ll_opy_(bstack1111ll111_opy_.get(bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1lllll11ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111ll1l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstackl_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l111lll_opy_
      bstack1l111lll_opy_ += bstackl_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack111l1lll_opy_ = re.compile(bstackl_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1ll1ll1ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111l1lll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstackl_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstackl_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1ll111llll_opy_():
  bstack1ll1l11ll1_opy_ = bstack111ll1l1_opy_()
  if bstack1ll1l11ll1_opy_ and os.path.exists(os.path.abspath(bstack1ll1l11ll1_opy_)):
    fileName = bstack1ll1l11ll1_opy_
  if bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack11l11_opy_ = os.path.abspath(fileName)
  else:
    bstack11l11_opy_ = bstackl_opy_ (u"ࠩࠪ࢟")
  bstack11l1l11l_opy_ = os.getcwd()
  bstack111ll1ll1_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack111ll1lll_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack11l11_opy_)) and bstack11l1l11l_opy_ != bstackl_opy_ (u"ࠧࠨࢢ"):
    bstack11l11_opy_ = os.path.join(bstack11l1l11l_opy_, bstack111ll1ll1_opy_)
    if not os.path.exists(bstack11l11_opy_):
      bstack11l11_opy_ = os.path.join(bstack11l1l11l_opy_, bstack111ll1lll_opy_)
    if bstack11l1l11l_opy_ != os.path.dirname(bstack11l1l11l_opy_):
      bstack11l1l11l_opy_ = os.path.dirname(bstack11l1l11l_opy_)
    else:
      bstack11l1l11l_opy_ = bstackl_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack11l11_opy_):
    bstack11111l11_opy_(
      bstack111l11l11_opy_.format(os.getcwd()))
  try:
    with open(bstack11l11_opy_, bstackl_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstackl_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack111l1lll_opy_)
      yaml.add_constructor(bstackl_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1ll1ll1ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l11_opy_, bstackl_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11111l11_opy_(bstack11111l1ll_opy_.format(str(exc)))
def bstack1lllllll11_opy_(config):
  bstack1ll11111l_opy_ = bstack1l1lll1l_opy_(config)
  for option in list(bstack1ll11111l_opy_):
    if option.lower() in bstack1l11l111l_opy_ and option != bstack1l11l111l_opy_[option.lower()]:
      bstack1ll11111l_opy_[bstack1l11l111l_opy_[option.lower()]] = bstack1ll11111l_opy_[option]
      del bstack1ll11111l_opy_[option]
  return config
def bstack111l11l1l_opy_():
  global bstack11lll111l_opy_
  for key, bstack1111111l_opy_ in bstack1llllllll_opy_.items():
    if isinstance(bstack1111111l_opy_, list):
      for var in bstack1111111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11lll111l_opy_[key] = os.environ[var]
          break
    elif bstack1111111l_opy_ in os.environ and os.environ[bstack1111111l_opy_] and str(os.environ[bstack1111111l_opy_]).strip():
      bstack11lll111l_opy_[key] = os.environ[bstack1111111l_opy_]
  if bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack11lll111l_opy_[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack11lll111l_opy_[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack11l1l1l1_opy_():
  global bstack1llll1ll11_opy_
  global bstack1l111lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstackl_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack1llll1ll11_opy_[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack1llll1ll11_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l11l11l_opy_ in bstack1lll1llll_opy_.items():
    if isinstance(bstack11l11l11l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l11l11l_opy_:
          if idx < len(sys.argv) and bstackl_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack1llll1ll11_opy_:
            bstack1llll1ll11_opy_[key] = sys.argv[idx + 1]
            bstack1l111lll_opy_ += bstackl_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstackl_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstackl_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11l11l11l_opy_.lower() == val.lower() and not key in bstack1llll1ll11_opy_:
          bstack1llll1ll11_opy_[key] = sys.argv[idx + 1]
          bstack1l111lll_opy_ += bstackl_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11l11l11l_opy_ + bstackl_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1l1llll_opy_(config):
  bstack1111ll1l1_opy_ = config.keys()
  for bstack1l11l11l1_opy_, bstack1l11ll11l_opy_ in bstack1l111llll_opy_.items():
    if bstack1l11ll11l_opy_ in bstack1111ll1l1_opy_:
      config[bstack1l11l11l1_opy_] = config[bstack1l11ll11l_opy_]
      del config[bstack1l11ll11l_opy_]
  for bstack1l11l11l1_opy_, bstack1l11ll11l_opy_ in bstack11lll1l1l_opy_.items():
    if isinstance(bstack1l11ll11l_opy_, list):
      for bstack11111111l_opy_ in bstack1l11ll11l_opy_:
        if bstack11111111l_opy_ in bstack1111ll1l1_opy_:
          config[bstack1l11l11l1_opy_] = config[bstack11111111l_opy_]
          del config[bstack11111111l_opy_]
          break
    elif bstack1l11ll11l_opy_ in bstack1111ll1l1_opy_:
      config[bstack1l11l11l1_opy_] = config[bstack1l11ll11l_opy_]
      del config[bstack1l11ll11l_opy_]
  for bstack11111111l_opy_ in list(config):
    for bstack1ll11111_opy_ in bstack111llll1_opy_:
      if bstack11111111l_opy_.lower() == bstack1ll11111_opy_.lower() and bstack11111111l_opy_ != bstack1ll11111_opy_:
        config[bstack1ll11111_opy_] = config[bstack11111111l_opy_]
        del config[bstack11111111l_opy_]
  bstack1lll111l1_opy_ = []
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1lll111l1_opy_ = config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1lll111l1_opy_:
    for bstack11111111l_opy_ in list(platform):
      for bstack1ll11111_opy_ in bstack111llll1_opy_:
        if bstack11111111l_opy_.lower() == bstack1ll11111_opy_.lower() and bstack11111111l_opy_ != bstack1ll11111_opy_:
          platform[bstack1ll11111_opy_] = platform[bstack11111111l_opy_]
          del platform[bstack11111111l_opy_]
  for bstack1l11l11l1_opy_, bstack1l11ll11l_opy_ in bstack11lll1l1l_opy_.items():
    for platform in bstack1lll111l1_opy_:
      if isinstance(bstack1l11ll11l_opy_, list):
        for bstack11111111l_opy_ in bstack1l11ll11l_opy_:
          if bstack11111111l_opy_ in platform:
            platform[bstack1l11l11l1_opy_] = platform[bstack11111111l_opy_]
            del platform[bstack11111111l_opy_]
            break
      elif bstack1l11ll11l_opy_ in platform:
        platform[bstack1l11l11l1_opy_] = platform[bstack1l11ll11l_opy_]
        del platform[bstack1l11ll11l_opy_]
  for bstack1ll1111lll_opy_ in bstack1llll1lll_opy_:
    if bstack1ll1111lll_opy_ in config:
      if not bstack1llll1lll_opy_[bstack1ll1111lll_opy_] in config:
        config[bstack1llll1lll_opy_[bstack1ll1111lll_opy_]] = {}
      config[bstack1llll1lll_opy_[bstack1ll1111lll_opy_]].update(config[bstack1ll1111lll_opy_])
      del config[bstack1ll1111lll_opy_]
  for platform in bstack1lll111l1_opy_:
    for bstack1ll1111lll_opy_ in bstack1llll1lll_opy_:
      if bstack1ll1111lll_opy_ in list(platform):
        if not bstack1llll1lll_opy_[bstack1ll1111lll_opy_] in platform:
          platform[bstack1llll1lll_opy_[bstack1ll1111lll_opy_]] = {}
        platform[bstack1llll1lll_opy_[bstack1ll1111lll_opy_]].update(platform[bstack1ll1111lll_opy_])
        del platform[bstack1ll1111lll_opy_]
  config = bstack1lllllll11_opy_(config)
  return config
def bstack1lll1l1ll_opy_(config):
  global bstack11lllllll_opy_
  if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstackl_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack111l11lll_opy_ = datetime.datetime.now()
      bstack1l11llll1_opy_ = bstack111l11lll_opy_.strftime(bstackl_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack11l1lll1l_opy_ = bstackl_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack1l11llll1_opy_, hostname, bstack11l1lll1l_opy_)
      config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack11lllllll_opy_ = config[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack11111lll1_opy_():
  bstack11ll1lll1_opy_ =  bstack11ll1lll_opy_()[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack11ll1lll1_opy_ if bstack11ll1lll1_opy_ else -1
def bstack1lll1l1lll_opy_(bstack11ll1lll1_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstackl_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack11ll1lll1_opy_)
  )
def bstack111111ll1_opy_():
  global CONFIG
  if not bstackl_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack111l11lll_opy_ = datetime.datetime.now()
  bstack1l11llll1_opy_ = bstack111l11lll_opy_.strftime(bstackl_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack1l11llll1_opy_
  )
def bstack11ll1llll_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstackl_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack111111ll1_opy_()
    os.environ[bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack11ll1lll1_opy_ = bstackl_opy_ (u"ࠪࠫࣟ")
  bstack1l1lll1ll_opy_ = bstack11111lll1_opy_()
  if bstack1l1lll1ll_opy_ != -1:
    bstack11ll1lll1_opy_ = bstackl_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack1l1lll1ll_opy_)
  if bstack11ll1lll1_opy_ == bstackl_opy_ (u"ࠬ࠭࣡"):
    bstack111l11ll1_opy_ = bstack1lll1lllll_opy_(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack111l11ll1_opy_ != -1:
      bstack11ll1lll1_opy_ = str(bstack111l11ll1_opy_)
  if bstack11ll1lll1_opy_:
    bstack1lll1l1lll_opy_(bstack11ll1lll1_opy_)
    os.environ[bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1ll11l1ll_opy_(bstack1lll1ll11l_opy_, bstack1l1l111l1_opy_, path):
  bstack11ll111ll_opy_ = {
    bstackl_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack1l1l111l1_opy_
  }
  if os.path.exists(path):
    bstack1l1lll1l11_opy_ = json.load(open(path, bstackl_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1l1lll1l11_opy_ = {}
  bstack1l1lll1l11_opy_[bstack1lll1ll11l_opy_] = bstack11ll111ll_opy_
  with open(path, bstackl_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1l1lll1l11_opy_, outfile)
def bstack1lll1lllll_opy_(bstack1lll1ll11l_opy_):
  bstack1lll1ll11l_opy_ = str(bstack1lll1ll11l_opy_)
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧࣨ")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack111l1111l_opy_):
      os.makedirs(bstack111l1111l_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩ࣪")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstackl_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1lll1llll1_opy_:
      bstack111l1l1l1_opy_ = json.load(bstack1lll1llll1_opy_)
    if bstack1lll1ll11l_opy_ in bstack111l1l1l1_opy_:
      bstack1ll1lll1_opy_ = bstack111l1l1l1_opy_[bstack1lll1ll11l_opy_][bstackl_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack1l1lll1111_opy_ = int(bstack1ll1lll1_opy_) + 1
      bstack1ll11l1ll_opy_(bstack1lll1ll11l_opy_, bstack1l1lll1111_opy_, file_path)
      return bstack1l1lll1111_opy_
    else:
      bstack1ll11l1ll_opy_(bstack1lll1ll11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111lllll_opy_.format(str(e)))
    return -1
def bstack1ll111ll_opy_(config):
  if not config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack111l1l11l_opy_(config, index=0):
  global bstack1l11ll111_opy_
  bstack1lllll1lll_opy_ = {}
  caps = bstack1lll111l11_opy_ + bstack1l1111l1_opy_
  if bstack1l11ll111_opy_:
    caps += bstack1lllll1111_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1lllll1lll_opy_[key] = config[key]
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1111lll11_opy_ in config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1111lll11_opy_ in caps + [bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1lllll1lll_opy_[bstack1111lll11_opy_] = config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1111lll11_opy_]
  bstack1lllll1lll_opy_[bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstackl_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1lllll1lll_opy_:
    del (bstack1lllll1lll_opy_[bstackl_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1lllll1lll_opy_
def bstack11ll11l1l_opy_(config):
  global bstack1l11ll111_opy_
  bstack1lll111ll_opy_ = {}
  caps = bstack1l1111l1_opy_
  if bstack1l11ll111_opy_:
    caps += bstack1lllll1111_opy_
  for key in caps:
    if key in config:
      bstack1lll111ll_opy_[key] = config[key]
  return bstack1lll111ll_opy_
def bstack11l11l111_opy_(bstack1lllll1lll_opy_, bstack1lll111ll_opy_):
  bstack11l1lllll_opy_ = {}
  for key in bstack1lllll1lll_opy_.keys():
    if key in bstack1l111llll_opy_:
      bstack11l1lllll_opy_[bstack1l111llll_opy_[key]] = bstack1lllll1lll_opy_[key]
    else:
      bstack11l1lllll_opy_[key] = bstack1lllll1lll_opy_[key]
  for key in bstack1lll111ll_opy_:
    if key in bstack1l111llll_opy_:
      bstack11l1lllll_opy_[bstack1l111llll_opy_[key]] = bstack1lll111ll_opy_[key]
    else:
      bstack11l1lllll_opy_[key] = bstack1lll111ll_opy_[key]
  return bstack11l1lllll_opy_
def bstack11ll1l111_opy_(config, index=0):
  global bstack1l11ll111_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lll111ll_opy_ = bstack11ll11l1l_opy_(config)
  bstack1lll11ll11_opy_ = bstack1l1111l1_opy_
  bstack1lll11ll11_opy_ += bstack1lll11l1l_opy_
  if bstack1l11ll111_opy_:
    bstack1lll11ll11_opy_ += bstack1lllll1111_opy_
  if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack1111ll11l_opy_ = {}
    for bstack1l1ll11l_opy_ in bstack1lll11ll11_opy_:
      if bstack1l1ll11l_opy_ in config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l1ll11l_opy_ == bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack1111ll11l_opy_[bstack1l1ll11l_opy_] = str(config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1ll11l_opy_] * 1.0)
          except:
            bstack1111ll11l_opy_[bstack1l1ll11l_opy_] = str(config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l1ll11l_opy_])
        else:
          bstack1111ll11l_opy_[bstack1l1ll11l_opy_] = config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l1ll11l_opy_]
        del (config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l1ll11l_opy_])
    bstack1lll111ll_opy_ = update(bstack1lll111ll_opy_, bstack1111ll11l_opy_)
  bstack1lllll1lll_opy_ = bstack111l1l11l_opy_(config, index)
  for bstack11111111l_opy_ in bstack1l1111l1_opy_ + [bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack11111111l_opy_ in bstack1lllll1lll_opy_:
      bstack1lll111ll_opy_[bstack11111111l_opy_] = bstack1lllll1lll_opy_[bstack11111111l_opy_]
      del (bstack1lllll1lll_opy_[bstack11111111l_opy_])
  if bstack111ll11l_opy_(config):
    bstack1lllll1lll_opy_[bstackl_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1lll111ll_opy_)
    caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1lllll1lll_opy_
  else:
    bstack1lllll1lll_opy_[bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack11l11l111_opy_(bstack1lllll1lll_opy_, bstack1lll111ll_opy_))
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1ll11l1111_opy_():
  global bstack1l1111111_opy_
  if bstack11l1l1ll_opy_() <= version.parse(bstackl_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack1l1111111_opy_ != bstackl_opy_ (u"ࠧࠨछ"):
      return bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack1l1111111_opy_ + bstackl_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack11lll11ll_opy_
  if bstack1l1111111_opy_ != bstackl_opy_ (u"ࠪࠫञ"):
    return bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack1l1111111_opy_ + bstackl_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1lllll1l11_opy_
def bstack1l1l1ll11_opy_(options):
  return hasattr(options, bstackl_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111l1ll_opy_(options, bstack1l1lll1l1l_opy_):
  for bstack111ll11l1_opy_ in bstack1l1lll1l1l_opy_:
    if bstack111ll11l1_opy_ in [bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack111ll11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack111ll11l1_opy_] = update(options._experimental_options[bstack111ll11l1_opy_],
                                                         bstack1l1lll1l1l_opy_[bstack111ll11l1_opy_])
    else:
      options.add_experimental_option(bstack111ll11l1_opy_, bstack1l1lll1l1l_opy_[bstack111ll11l1_opy_])
  if bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack1l1lll1l1l_opy_:
    for arg in bstack1l1lll1l1l_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack1l1lll1l1l_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstackl_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack1l1lll1l1l_opy_:
    for ext in bstack1l1lll1l1l_opy_[bstackl_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack1l1lll1l1l_opy_[bstackl_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1lllll1l1l_opy_(options, bstack11l11llll_opy_):
  if bstackl_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack11l11llll_opy_:
    for bstack11ll1ll1_opy_ in bstack11l11llll_opy_[bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack11ll1ll1_opy_ in options._preferences:
        options._preferences[bstack11ll1ll1_opy_] = update(options._preferences[bstack11ll1ll1_opy_], bstack11l11llll_opy_[bstackl_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack11ll1ll1_opy_])
      else:
        options.set_preference(bstack11ll1ll1_opy_, bstack11l11llll_opy_[bstackl_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack11ll1ll1_opy_])
  if bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack11l11llll_opy_:
    for arg in bstack11l11llll_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack11l111111_opy_(options, bstack1l1lllllll_opy_):
  if bstackl_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1l1lllllll_opy_:
    options.use_webview(bool(bstack1l1lllllll_opy_[bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1l111l1ll_opy_(options, bstack1l1lllllll_opy_)
def bstack1l111l11l_opy_(options, bstack1l11ll1l_opy_):
  for bstack1llll11l11_opy_ in bstack1l11ll1l_opy_:
    if bstack1llll11l11_opy_ in [bstackl_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1llll11l11_opy_, bstack1l11ll1l_opy_[bstack1llll11l11_opy_])
  if bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1l11ll1l_opy_:
    for arg in bstack1l11ll1l_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1l11ll1l_opy_:
    options.bstack1lll1ll111_opy_(bool(bstack1l11ll1l_opy_[bstackl_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1l1llll1l_opy_(options, bstack1llllllll1_opy_):
  for bstack1l1l11l1l_opy_ in bstack1llllllll1_opy_:
    if bstack1l1l11l1l_opy_ in [bstackl_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1l1l11l1l_opy_] = bstack1llllllll1_opy_[bstack1l1l11l1l_opy_]
  if bstackl_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1llllllll1_opy_:
    for bstack1ll11l111l_opy_ in bstack1llllllll1_opy_[bstackl_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack111ll1111_opy_(
        bstack1ll11l111l_opy_, bstack1llllllll1_opy_[bstackl_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack1ll11l111l_opy_])
  if bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1llllllll1_opy_:
    for arg in bstack1llllllll1_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack1lll11l1l1_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstackl_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1l111l1ll_opy_(options, caps[bstackl_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstackl_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1lllll1l1l_opy_(options, caps[bstackl_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1l111l11l_opy_(options, caps[bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstackl_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack11l111111_opy_(options, caps[bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1l1llll1l_opy_(options, caps[bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1ll11l1l1l_opy_(caps):
  global bstack1l11ll111_opy_
  if isinstance(os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack1l11ll111_opy_ = eval(os.getenv(bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack1l11ll111_opy_:
    if bstack1lllll11ll_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstackl_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstackl_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstackl_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstackl_opy_ (u"࠭ࡩࡦࠩख़"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstackl_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstackl_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1ll11_opy_(options):
        return None
      for bstack11111111l_opy_ in caps.keys():
        options.set_capability(bstack11111111l_opy_, caps[bstack11111111l_opy_])
      bstack1lll11l1l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11111111_opy_(options, bstack1l11ll1ll_opy_):
  if not bstack1l1l1ll11_opy_(options):
    return
  for bstack11111111l_opy_ in bstack1l11ll1ll_opy_.keys():
    if bstack11111111l_opy_ in bstack1lll11l1l_opy_:
      continue
    if bstack11111111l_opy_ in options._caps and type(options._caps[bstack11111111l_opy_]) in [dict, list]:
      options._caps[bstack11111111l_opy_] = update(options._caps[bstack11111111l_opy_], bstack1l11ll1ll_opy_[bstack11111111l_opy_])
    else:
      options.set_capability(bstack11111111l_opy_, bstack1l11ll1ll_opy_[bstack11111111l_opy_])
  bstack1lll11l1l1_opy_(options, bstack1l11ll1ll_opy_)
  if bstackl_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack11111l11l_opy_(proxy_config):
  if bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstackl_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstackl_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstackl_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack111111l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack11111l11l_opy_(config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1l111l111_opy_(self):
  global CONFIG
  global bstack1l111ll11_opy_
  try:
    proxy = bstack1l1ll1ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstackl_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack1llll1111l_opy_(proxy, bstack1ll11l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll1l1l_opy_ = proxies.popitem()
          if bstackl_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1l1ll1l1l_opy_:
            return bstack1l1ll1l1l_opy_
          else:
            return bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1l1ll1l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1l111ll11_opy_(self)
def bstack1ll11l1ll1_opy_():
  global CONFIG
  return bstack1lllll11l1_opy_(CONFIG) and bstack1l1l1ll1l_opy_() and bstack11l1l1ll_opy_() >= version.parse(bstack1ll11lll_opy_)
def bstack1ll11llll_opy_():
  global CONFIG
  return (bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1l1lll1l1_opy_()
def bstack1l1lll1l_opy_(config):
  bstack1ll11111l_opy_ = {}
  if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1ll11111l_opy_ = config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1ll11111l_opy_ = config[bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1l1ll1ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstackl_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1ll11111l_opy_[bstackl_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstackl_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1ll1l1l1l_opy_(config, bstack1ll11l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll1l1l_opy_ = proxies.popitem()
          if bstackl_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1l1ll1l1l_opy_:
            parsed_url = urlparse(bstack1l1ll1l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstackl_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1l1ll1l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll11111l_opy_[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll11111l_opy_[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll11111l_opy_[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll11111l_opy_[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1ll11111l_opy_
def bstack11l1ll1ll_opy_(config):
  if bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack1111lll1_opy_(caps):
  global bstack11lllllll_opy_
  if bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack11lllllll_opy_:
      caps[bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack11lllllll_opy_
  else:
    caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack11lllllll_opy_:
      caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack11lllllll_opy_
def bstack1lll1l1l11_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack11llll111_opy_(CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1ll11111l_opy_ = bstack1l1lll1l_opy_(CONFIG)
    bstack111l1ll1_opy_(CONFIG[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll11111l_opy_)
def bstack111l1ll1_opy_(key, bstack1ll11111l_opy_):
  global bstack11lllll1l_opy_
  logger.info(bstack11l111lll_opy_)
  try:
    bstack11lllll1l_opy_ = Local()
    bstack111lll11l_opy_ = {bstackl_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack111lll11l_opy_.update(bstack1ll11111l_opy_)
    logger.debug(bstack1ll111ll11_opy_.format(str(bstack111lll11l_opy_)))
    bstack11lllll1l_opy_.start(**bstack111lll11l_opy_)
    if bstack11lllll1l_opy_.isRunning():
      logger.info(bstack1l11l1l1_opy_)
  except Exception as e:
    bstack11111l11_opy_(bstack1llllll1l_opy_.format(str(e)))
def bstack11111l1l1_opy_():
  global bstack11lllll1l_opy_
  if bstack11lllll1l_opy_.isRunning():
    logger.info(bstack11l1ll1l_opy_)
    bstack11lllll1l_opy_.stop()
  bstack11lllll1l_opy_ = None
def bstack11111ll1_opy_(bstack1llll11lll_opy_=[]):
  global CONFIG
  bstack1lll1l1111_opy_ = []
  bstack1ll111l1ll_opy_ = [bstackl_opy_ (u"ࠨࡱࡶࠫও"), bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1llll11lll_opy_:
      bstack1lll111lll_opy_ = {}
      for k in bstack1ll111l1ll_opy_:
        val = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstackl_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1lll111lll_opy_[k] = val
      if(err[bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstackl_opy_ (u"ࠪࠫজ")):
        bstack1lll111lll_opy_[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstackl_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1lll1l1111_opy_.append(bstack1lll111lll_opy_)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1lll1l1111_opy_
def bstack11ll11lll_opy_(file_name):
  bstack1ll11lll1l_opy_ = []
  try:
    bstack1llll11l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1llll11l1_opy_):
      with open(bstack1llll11l1_opy_) as f:
        bstack11llll1ll_opy_ = json.load(f)
        bstack1ll11lll1l_opy_ = bstack11llll1ll_opy_
      os.remove(bstack1llll11l1_opy_)
    return bstack1ll11lll1l_opy_
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack1l111ll1_opy_():
  global bstack11l11111_opy_
  global bstack1ll1ll1lll_opy_
  global bstack1llllll11_opy_
  global bstack11l11ll1_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack11ll111l_opy_
  percy.shutdown()
  bstack1lllll11_opy_ = os.environ.get(bstackl_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1lllll11_opy_ in [bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1ll1ll1l1_opy_()
  if bstack11l11111_opy_:
    logger.warning(bstack1ll1lll1l_opy_.format(str(bstack11l11111_opy_)))
  else:
    try:
      bstack1l1lll1l11_opy_ = bstack1l1l1l1ll_opy_(bstackl_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1lll1l11_opy_.get(bstackl_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1lll1l11_opy_.get(bstackl_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1ll1lll1l_opy_.format(str(bstack1l1lll1l11_opy_[bstackl_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstackl_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1ll1l1l_opy_)
  global bstack11lllll1l_opy_
  if bstack11lllll1l_opy_:
    bstack11111l1l1_opy_()
  try:
    for driver in bstack1ll1ll1lll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111lll11_opy_)
  if bstack11ll111l_opy_ == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1ll1l1l1l1_opy_ = bstack11ll11lll_opy_(bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack11ll111l_opy_ == bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack11l11ll1_opy_) == 0:
    bstack11l11ll1_opy_ = bstack11ll11lll_opy_(bstackl_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack11l11ll1_opy_) == 0:
      bstack11l11ll1_opy_ = bstack11ll11lll_opy_(bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1lll11llll_opy_ = bstackl_opy_ (u"ࠩࠪর")
  if len(bstack1llllll11_opy_) > 0:
    bstack1lll11llll_opy_ = bstack11111ll1_opy_(bstack1llllll11_opy_)
  elif len(bstack11l11ll1_opy_) > 0:
    bstack1lll11llll_opy_ = bstack11111ll1_opy_(bstack11l11ll1_opy_)
  elif len(bstack1ll1l1l1l1_opy_) > 0:
    bstack1lll11llll_opy_ = bstack11111ll1_opy_(bstack1ll1l1l1l1_opy_)
  elif len(bstack1l11lll1_opy_) > 0:
    bstack1lll11llll_opy_ = bstack11111ll1_opy_(bstack1l11lll1_opy_)
  if bool(bstack1lll11llll_opy_):
    bstack1lllllll1l_opy_(bstack1lll11llll_opy_)
  else:
    bstack1lllllll1l_opy_()
  bstack1lll11lll_opy_(bstack111ll1l11_opy_, logger)
def bstack1l11l1111_opy_(self, *args):
  logger.error(bstack1l1ll1ll_opy_)
  bstack1l111ll1_opy_()
  sys.exit(1)
def bstack11111l11_opy_(err):
  logger.critical(bstack1llll111_opy_.format(str(err)))
  bstack1lllllll1l_opy_(bstack1llll111_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111ll1_opy_)
  bstack1ll1ll1l1_opy_()
  sys.exit(1)
def bstack1ll1l11111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lllllll1l_opy_(message, True)
  atexit.unregister(bstack1l111ll1_opy_)
  bstack1ll1ll1l1_opy_()
  sys.exit(1)
def bstack11llllll1_opy_():
  global CONFIG
  global bstack1llll1ll11_opy_
  global bstack11lll111l_opy_
  global bstack1l11ll1l1_opy_
  CONFIG = bstack1ll111llll_opy_()
  bstack111l11l1l_opy_()
  bstack11l1l1l1_opy_()
  CONFIG = bstack1l1l1llll_opy_(CONFIG)
  update(CONFIG, bstack11lll111l_opy_)
  update(CONFIG, bstack1llll1ll11_opy_)
  CONFIG = bstack1lll1l1ll_opy_(CONFIG)
  bstack1l11ll1l1_opy_ = bstack1ll1ll1111_opy_(CONFIG)
  bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1l11ll1l1_opy_)
  if (bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack1llll1ll11_opy_) or (
          bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack11lll111l_opy_):
    if os.getenv(bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack11ll1llll_opy_()
  elif (bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack11lll111l_opy_ and bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack1llll1ll11_opy_):
    del (CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1ll111ll_opy_(CONFIG):
    bstack11111l11_opy_(bstack1lll11l11_opy_)
  bstack1l1lll11l_opy_()
  bstack11ll11ll1_opy_()
  if bstack1l11ll111_opy_:
    CONFIG[bstackl_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1l1l1l11l_opy_(CONFIG)
    logger.info(bstack111l1l111_opy_.format(CONFIG[bstackl_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack111l1ll1l_opy_(config, bstack1111l1ll_opy_):
  global CONFIG
  global bstack1l11ll111_opy_
  CONFIG = config
  bstack1l11ll111_opy_ = bstack1111l1ll_opy_
def bstack11ll11ll1_opy_():
  global CONFIG
  global bstack1l11ll111_opy_
  if bstackl_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack1111l1lll_opy_)
    bstack1l11ll111_opy_ = True
    bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1l1l1l11l_opy_(config):
  bstack1lll11111l_opy_ = bstackl_opy_ (u"࠭ࠧূ")
  app = config[bstackl_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111ll111l_opy_:
      if os.path.exists(app):
        bstack1lll11111l_opy_ = bstack1l1ll1l1_opy_(config, app)
      elif bstack11l1111ll_opy_(app):
        bstack1lll11111l_opy_ = app
      else:
        bstack11111l11_opy_(bstack1llll1l11_opy_.format(app))
    else:
      if bstack11l1111ll_opy_(app):
        bstack1lll11111l_opy_ = app
      elif os.path.exists(app):
        bstack1lll11111l_opy_ = bstack1l1ll1l1_opy_(app)
      else:
        bstack11111l11_opy_(bstack1llll1l111_opy_)
  else:
    if len(app) > 2:
      bstack11111l11_opy_(bstack1lll11111_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstackl_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack1lll11111l_opy_ = bstack1l1ll1l1_opy_(config, app[bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack11111l11_opy_(bstack1llll1l11_opy_.format(app))
      else:
        bstack11111l11_opy_(bstack1lll11111_opy_)
    else:
      for key in app:
        if key in bstack1ll1ll111_opy_:
          if key == bstackl_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack1lll11111l_opy_ = bstack1l1ll1l1_opy_(config, app[key])
            else:
              bstack11111l11_opy_(bstack1llll1l11_opy_.format(app))
          else:
            bstack1lll11111l_opy_ = app[key]
        else:
          bstack11111l11_opy_(bstack111l1l11_opy_)
  return bstack1lll11111l_opy_
def bstack11l1111ll_opy_(bstack1lll11111l_opy_):
  import re
  bstack1l11111l1_opy_ = re.compile(bstackl_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack11llllll_opy_ = re.compile(bstackl_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstackl_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack1lll11111l_opy_ or re.fullmatch(bstack1l11111l1_opy_, bstack1lll11111l_opy_) or re.fullmatch(bstack11llllll_opy_, bstack1lll11111l_opy_):
    return True
  else:
    return False
def bstack1l1ll1l1_opy_(config, path, bstack11l111l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack11l11111l_opy_ = bstack11l1l1111_opy_(md5_hash)
  bstack1lll11111l_opy_ = None
  if bstack11l11111l_opy_:
    logger.info(bstack1l11l1lll_opy_.format(bstack11l11111l_opy_, md5_hash))
    return bstack11l11111l_opy_
  bstack1lll1ll1l_opy_ = MultipartEncoder(
    fields={
      bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠬࡸࡢࠨ৏")), bstackl_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack11l111l1_opy_
    }
  )
  response = requests.post(bstack1l111l1l_opy_, data=bstack1lll1ll1l_opy_,
                           headers={bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1lll1ll1l_opy_.content_type},
                           auth=(config[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack1lll11111l_opy_ = res[bstackl_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1ll11l11l1_opy_.format(bstack1lll11111l_opy_))
    bstack1l1llll1ll_opy_(md5_hash, bstack1lll11111l_opy_)
  except ValueError as err:
    bstack11111l11_opy_(bstack1l11l111_opy_.format(str(err)))
  return bstack1lll11111l_opy_
def bstack1l1lll11l_opy_():
  global CONFIG
  global bstack11l11l11_opy_
  bstack1111l111l_opy_ = 0
  bstack1l111l1l1_opy_ = 1
  if bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1l111l1l1_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1111l111l_opy_ = len(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack11l11l11_opy_ = int(bstack1l111l1l1_opy_) * int(bstack1111l111l_opy_)
def bstack11l1l1111_opy_(md5_hash):
  bstack11111l1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫ৚")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstackl_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack11111l1l_opy_):
    bstack1ll111l11l_opy_ = json.load(open(bstack11111l1l_opy_, bstackl_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1ll111l11l_opy_:
      bstack1111ll1l_opy_ = bstack1ll111l11l_opy_[md5_hash]
      bstack1ll111111_opy_ = datetime.datetime.now()
      bstack1llll1l1ll_opy_ = datetime.datetime.strptime(bstack1111ll1l_opy_[bstackl_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstackl_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1ll111111_opy_ - bstack1llll1l1ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1111ll1l_opy_[bstackl_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack1111ll1l_opy_[bstackl_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack1l1llll1ll_opy_(md5_hash, bstack1lll11111l_opy_):
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬৢ")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack111l1111l_opy_):
    os.makedirs(bstack111l1111l_opy_)
  bstack11111l1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ৤")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack1l1lllll1_opy_ = {
    bstackl_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack1lll11111l_opy_,
    bstackl_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstackl_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack11111l1l_opy_):
    bstack1ll111l11l_opy_ = json.load(open(bstack11111l1l_opy_, bstackl_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1ll111l11l_opy_ = {}
  bstack1ll111l11l_opy_[md5_hash] = bstack1l1lllll1_opy_
  with open(bstack11111l1l_opy_, bstackl_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1ll111l11l_opy_, outfile)
def bstack11ll1ll11_opy_(self):
  return
def bstack1ll11l11_opy_(self):
  return
def bstack1l1ll11ll_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1lllll_opy_(self):
  global bstack111lllll1_opy_
  global bstack11ll111l1_opy_
  global bstack111lll1l1_opy_
  try:
    if bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack111lllll1_opy_ and self.session_id != None and bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstackl_opy_ (u"ࠩࠪ৯")) != bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack111l1l1l_opy_ = bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack111l1l1l_opy_ == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack111l111ll_opy_(logger)
      if self != None:
        bstack11l1ll111_opy_(self, bstack111l1l1l_opy_, bstackl_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstackl_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack111lll1l1_opy_(self)
  self.session_id = None
def bstack1ll11lllll_opy_(self, command_executor=bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1l11lllll_opy_ = bstack1l1l11111_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstackl_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstackl_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll11l1ll_opy_.bstack1ll111l111_opy_(self)
  return bstack1l11lllll_opy_
def bstack1l1ll1lll1_opy_(self, driver_command, *args, **kwargs):
  global bstack11111lll_opy_
  response = bstack11111lll_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1lll11l1ll_opy_.bstack1ll1lll1l1_opy_({
          bstackl_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstackl_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1lll11l1ll_opy_.current_test_uuid() if bstack1lll11l1ll_opy_.current_test_uuid() else bstack1lll11l1ll_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1lll1lll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll111l1_opy_
  global bstack1ll1l111l_opy_
  global bstack111111l1l_opy_
  global bstack1111lll1l_opy_
  global bstack1l1ll1l111_opy_
  global bstack111lllll1_opy_
  global bstack1l1l11111_opy_
  global bstack1ll1ll1lll_opy_
  global bstack1lllll11l_opy_
  global bstack11l1llll1_opy_
  CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack111lllll1_opy_) + str(__version__)
  command_executor = bstack1ll11l1111_opy_()
  logger.debug(bstack1lll1lll1l_opy_.format(command_executor))
  proxy = bstack111111l1_opy_(CONFIG, proxy)
  bstack11l1l1l11_opy_ = 0 if bstack1ll1l111l_opy_ < 0 else bstack1ll1l111l_opy_
  try:
    if bstack1111lll1l_opy_ is True:
      bstack11l1l1l11_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1ll1l111_opy_ is True:
      bstack11l1l1l11_opy_ = int(threading.current_thread().name)
  except:
    bstack11l1l1l11_opy_ = 0
  bstack1l11ll1ll_opy_ = bstack11ll1l111_opy_(CONFIG, bstack11l1l1l11_opy_)
  logger.debug(bstack1ll1l111_opy_.format(str(bstack1l11ll1ll_opy_)))
  if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack11llll111_opy_(CONFIG[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack1111lll1_opy_(bstack1l11ll1ll_opy_)
  if desired_capabilities:
    bstack111l111l_opy_ = bstack1l1l1llll_opy_(desired_capabilities)
    bstack111l111l_opy_[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack111ll11l_opy_(CONFIG)
    bstack1l11l1l11_opy_ = bstack11ll1l111_opy_(bstack111l111l_opy_)
    if bstack1l11l1l11_opy_:
      bstack1l11ll1ll_opy_ = update(bstack1l11l1l11_opy_, bstack1l11ll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack11111111_opy_(options, bstack1l11ll1ll_opy_)
  if not options:
    options = bstack1ll11l1l1l_opy_(bstack1l11ll1ll_opy_)
  bstack11l1llll1_opy_ = CONFIG.get(bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack11l1l1l11_opy_]
  if bstack1l1ll1l1ll_opy_.bstack1ll111lll_opy_(CONFIG, bstack11l1l1l11_opy_) and bstack1l1ll1l1ll_opy_.bstack11l1l111_opy_(bstack1l11ll1ll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1l1ll1l1ll_opy_.set_capabilities(bstack1l11ll1ll_opy_, CONFIG)
  if proxy and bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1l1ll_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11ll1ll_opy_)
  logger.info(bstack11ll1l11_opy_)
  if bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack1l1l11111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack1l1l11111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
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
    bstack1ll1llll1_opy_ = bstackl_opy_ (u"ࠫࠬ਍")
    if bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack1ll1llll1_opy_ = self.caps.get(bstackl_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack1ll1llll1_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack1ll1llll1_opy_:
      bstack11l1l111l_opy_(bstack1ll1llll1_opy_)
      if bstack11l1l1ll_opy_() <= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack1l1111111_opy_ + bstackl_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack1ll1llll1_opy_ + bstackl_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack11ll11ll_opy_.format(bstack1ll1llll1_opy_))
    else:
      logger.debug(bstack1llllll1ll_opy_.format(bstackl_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack1llllll1ll_opy_.format(e))
  if bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack111lllll1_opy_:
    bstack11lll11l1_opy_(bstack1ll1l111l_opy_, bstack1lllll11l_opy_)
  bstack11ll111l1_opy_ = self.session_id
  if bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack111lllll1_opy_ or bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack111lllll1_opy_ or bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack111lllll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1lll11l1ll_opy_.bstack1ll111l111_opy_(self)
  bstack1ll1ll1lll_opy_.append(self)
  if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack11l1l1l11_opy_]:
    bstack111111l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack11l1l1l11_opy_][bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack1ll1111l1l_opy_.format(bstack11ll111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llll1lll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lll11l111_opy_
      if(bstackl_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬਡ")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstackl_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstackl_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstackl_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstackl_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l1lll11_opy_)
            lines.insert(1, bstack11llll11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstackl_opy_ (u"ࠬࡽࠧਪ")) as bstack111ll11ll_opy_:
              bstack111ll11ll_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack111lllll1_opy_) + str(__version__)
        bstack11l1l1l11_opy_ = 0 if bstack1ll1l111l_opy_ < 0 else bstack1ll1l111l_opy_
        try:
          if bstack1111lll1l_opy_ is True:
            bstack11l1l1l11_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1ll1l111_opy_ is True:
            bstack11l1l1l11_opy_ = int(threading.current_thread().name)
        except:
          bstack11l1l1l11_opy_ = 0
        CONFIG[bstackl_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstackl_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack1l11ll1ll_opy_ = bstack11ll1l111_opy_(CONFIG, bstack11l1l1l11_opy_)
        logger.debug(bstack1ll1l111_opy_.format(str(bstack1l11ll1ll_opy_)))
        if CONFIG.get(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack1111lll1_opy_(bstack1l11ll1ll_opy_)
        if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack11l1l1l11_opy_]:
          bstack111111l1l_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack11l1l1l11_opy_][bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪ਴")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstackl_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11ll1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack1lll11l111_opy_ = True
      return bstack11l11ll11_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll1lllll1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll1l111l_opy_
    global bstack111111l1l_opy_
    global bstack1111lll1l_opy_
    global bstack1l1ll1l111_opy_
    global bstack111lllll1_opy_
    CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack111lllll1_opy_) + str(__version__)
    bstack11l1l1l11_opy_ = 0 if bstack1ll1l111l_opy_ < 0 else bstack1ll1l111l_opy_
    try:
      if bstack1111lll1l_opy_ is True:
        bstack11l1l1l11_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1ll1l111_opy_ is True:
        bstack11l1l1l11_opy_ = int(threading.current_thread().name)
    except:
      bstack11l1l1l11_opy_ = 0
    CONFIG[bstackl_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack1l11ll1ll_opy_ = bstack11ll1l111_opy_(CONFIG, bstack11l1l1l11_opy_)
    logger.debug(bstack1ll1l111_opy_.format(str(bstack1l11ll1ll_opy_)))
    if CONFIG.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack1111lll1_opy_(bstack1l11ll1ll_opy_)
    if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstackl_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack11l1l1l11_opy_]:
      bstack111111l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack11l1l1l11_opy_][bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack1lll1l1l_opy_ = bstackl_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack1l11ll1ll_opy_))
    browser = self.connect(bstack1lll1l1l_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll11ll11_opy_():
    global bstack1lll11l111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1lllll1_opy_
        bstack1lll11l111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll1lll1_opy_
      bstack1lll11l111_opy_ = True
    except Exception as e:
      pass
def bstack1l1ll111l_opy_(context, bstack1l1ll1lll_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack1l1ll1lll_opy_) + bstackl_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack1ll111l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstackl_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstackl_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack111l11ll_opy_(self, url):
  global bstack1l1l1l1l1_opy_
  try:
    bstack111llll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1lllll_opy_.format(str(err)))
  try:
    bstack1l1l1l1l1_opy_(self, url)
  except Exception as e:
    try:
      bstack11111ll1l_opy_ = str(e)
      if any(err_msg in bstack11111ll1l_opy_ for err_msg in bstack1lll1111l1_opy_):
        bstack111llll1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1lllll_opy_.format(str(err)))
    raise e
def bstack1lll1l1ll1_opy_(self):
  global bstack11ll11111_opy_
  bstack11ll11111_opy_ = self
  return
def bstack11l1l1ll1_opy_(self):
  global bstack1llll111ll_opy_
  bstack1llll111ll_opy_ = self
  return
def bstack11l111l11_opy_(self, test):
  global CONFIG
  global bstack1llll111ll_opy_
  global bstack11ll11111_opy_
  global bstack11ll111l1_opy_
  global bstack11l1lll1_opy_
  global bstack111111l1l_opy_
  global bstack1ll1111l1_opy_
  global bstack1l1lll111l_opy_
  global bstack1l1l111l_opy_
  global bstack1ll1ll1lll_opy_
  global bstack11l1llll1_opy_
  try:
    if not bstack11ll111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫ੊")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ"))) as f:
        bstack1lll1lll1_opy_ = json.loads(bstackl_opy_ (u"ࠧࢁ੍ࠢ") + f.read().strip() + bstackl_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ੎") + bstackl_opy_ (u"ࠢࡾࠤ੏"))
        bstack11ll111l1_opy_ = bstack1lll1lll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1ll1lll_opy_:
    for driver in bstack1ll1ll1lll_opy_:
      if bstack11ll111l1_opy_ == driver.session_id:
        if test:
          bstack1l11111ll_opy_ = str(test.data)
          if bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ੐"), None) and bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨੑ"), None):
            logger.info(bstackl_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥ੒"))
            bstack1l1ll1l1ll_opy_.bstack11111ll11_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1ll1ll11l1_opy_=bstack11l1llll1_opy_)
        if not bstack1llll1l11l_opy_ and bstack1l11111ll_opy_:
          bstack1ll111l1_opy_ = {
            bstackl_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ੓"): bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੔"),
            bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੕"): {
              bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੖"): bstack1l11111ll_opy_
            }
          }
          bstack1ll11l1l11_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੗").format(json.dumps(bstack1ll111l1_opy_))
          driver.execute_script(bstack1ll11l1l11_opy_)
        if bstack11l1lll1_opy_:
          bstack1lll111111_opy_ = {
            bstackl_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੘"): bstackl_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬਖ਼"),
            bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧਗ਼"): {
              bstackl_opy_ (u"ࠬࡪࡡࡵࡣࠪਜ਼"): bstack1l11111ll_opy_ + bstackl_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨੜ"),
              bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੝"): bstackl_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ਫ਼")
            }
          }
          if bstack11l1lll1_opy_.status == bstackl_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੟"):
            bstack111111111_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੠").format(json.dumps(bstack1lll111111_opy_))
            driver.execute_script(bstack111111111_opy_)
            bstack11l1ll111_opy_(driver, bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੡"))
          elif bstack11l1lll1_opy_.status == bstackl_opy_ (u"ࠬࡌࡁࡊࡎࠪ੢"):
            reason = bstackl_opy_ (u"ࠨࠢ੣")
            bstack1ll1ll1l11_opy_ = bstack1l11111ll_opy_ + bstackl_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ੤")
            if bstack11l1lll1_opy_.message:
              reason = str(bstack11l1lll1_opy_.message)
              bstack1ll1ll1l11_opy_ = bstack1ll1ll1l11_opy_ + bstackl_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ੥") + reason
            bstack1lll111111_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੦")] = {
              bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੧"): bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ੨"),
              bstackl_opy_ (u"ࠬࡪࡡࡵࡣࠪ੩"): bstack1ll1ll1l11_opy_
            }
            bstack111111111_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੪").format(json.dumps(bstack1lll111111_opy_))
            driver.execute_script(bstack111111111_opy_)
            bstack11l1ll111_opy_(driver, bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੫"), reason)
            bstack1l11111l_opy_(reason, str(bstack11l1lll1_opy_), str(bstack1ll1l111l_opy_), logger)
  elif bstack11ll111l1_opy_:
    try:
      data = {}
      bstack1l11111ll_opy_ = None
      if test:
        bstack1l11111ll_opy_ = str(test.data)
      if not bstack1llll1l11l_opy_ and bstack1l11111ll_opy_:
        data[bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭੬")] = bstack1l11111ll_opy_
      if bstack11l1lll1_opy_:
        if bstack11l1lll1_opy_.status == bstackl_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੭"):
          data[bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ੮")] = bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੯")
        elif bstack11l1lll1_opy_.status == bstackl_opy_ (u"ࠬࡌࡁࡊࡎࠪੰ"):
          data[bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ੱ")] = bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧੲ")
          if bstack11l1lll1_opy_.message:
            data[bstackl_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨੳ")] = str(bstack11l1lll1_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫੴ")]
      key = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ੵ")]
      url = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ੶").format(user, key, bstack11ll111l1_opy_)
      headers = {
        bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ੷"): bstackl_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ੸"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111llllll_opy_.format(str(e)))
  if bstack1llll111ll_opy_:
    bstack1l1lll111l_opy_(bstack1llll111ll_opy_)
  if bstack11ll11111_opy_:
    bstack1l1l111l_opy_(bstack11ll11111_opy_)
  bstack1ll1111l1_opy_(self, test)
def bstack1ll11ll1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1ll1l_opy_
  global CONFIG
  global bstack1ll1ll1lll_opy_
  global bstack11ll111l1_opy_
  bstack1l11llll_opy_ = None
  try:
    if bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭੹"), None):
      try:
        if not bstack11ll111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪ੺")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੻"), bstackl_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ੼"))) as f:
            bstack1lll1lll1_opy_ = json.loads(bstackl_opy_ (u"ࠦࢀࠨ੽") + f.read().strip() + bstackl_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ੾") + bstackl_opy_ (u"ࠨࡽࠣ੿"))
            bstack11ll111l1_opy_ = bstack1lll1lll1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1ll1lll_opy_:
        for driver in bstack1ll1ll1lll_opy_:
          if bstack11ll111l1_opy_ == driver.session_id:
            bstack1l11llll_opy_ = driver
    bstack1l11l1l1l_opy_ = bstack1l1ll1l1ll_opy_.bstack111lll1l_opy_(CONFIG, test.tags)
    if bstack1l11llll_opy_:
      threading.current_thread().isA11yTest = bstack1l1ll1l1ll_opy_.bstack11ll1l1l_opy_(bstack1l11llll_opy_, bstack1l11l1l1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l11l1l1l_opy_
  except:
    pass
  bstack11ll1ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1lll1_opy_
  bstack11l1lll1_opy_ = self._test
def bstack1llll11l_opy_():
  global bstack11l1l1lll_opy_
  try:
    if os.path.exists(bstack11l1l1lll_opy_):
      os.remove(bstack11l1l1lll_opy_)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ઀") + str(e))
def bstack1ll1l11l_opy_():
  global bstack11l1l1lll_opy_
  bstack1l1lll1l11_opy_ = {}
  try:
    if not os.path.isfile(bstack11l1l1lll_opy_):
      with open(bstack11l1l1lll_opy_, bstackl_opy_ (u"ࠨࡹࠪઁ")):
        pass
      with open(bstack11l1l1lll_opy_, bstackl_opy_ (u"ࠤࡺ࠯ࠧં")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11l1l1lll_opy_):
      bstack1l1lll1l11_opy_ = json.load(open(bstack11l1l1lll_opy_, bstackl_opy_ (u"ࠪࡶࡧ࠭ઃ")))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭઄") + str(e))
  finally:
    return bstack1l1lll1l11_opy_
def bstack11lll11l1_opy_(platform_index, item_index):
  global bstack11l1l1lll_opy_
  try:
    bstack1l1lll1l11_opy_ = bstack1ll1l11l_opy_()
    bstack1l1lll1l11_opy_[item_index] = platform_index
    with open(bstack11l1l1lll_opy_, bstackl_opy_ (u"ࠧࡽࠫࠣઅ")) as outfile:
      json.dump(bstack1l1lll1l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઆ") + str(e))
def bstack1ll1l11lll_opy_(bstack1ll1llll_opy_):
  global CONFIG
  bstack1ll1111l_opy_ = bstackl_opy_ (u"ࠧࠨઇ")
  if not bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઈ") in CONFIG:
    logger.info(bstackl_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ઉ"))
  try:
    platform = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઊ")][bstack1ll1llll_opy_]
    if bstackl_opy_ (u"ࠫࡴࡹࠧઋ") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"ࠬࡵࡳࠨઌ")]) + bstackl_opy_ (u"࠭ࠬࠡࠩઍ")
    if bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ઎") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫએ")]) + bstackl_opy_ (u"ࠩ࠯ࠤࠬઐ")
    if bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઑ") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ઒")]) + bstackl_opy_ (u"ࠬ࠲ࠠࠨઓ")
    if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨઔ") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩક")]) + bstackl_opy_ (u"ࠨ࠮ࠣࠫખ")
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧગ") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨઘ")]) + bstackl_opy_ (u"ࠫ࠱ࠦࠧઙ")
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ચ") in platform:
      bstack1ll1111l_opy_ += str(platform[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧછ")]) + bstackl_opy_ (u"ࠧ࠭ࠢࠪજ")
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨઝ") + str(e))
  finally:
    if bstack1ll1111l_opy_[len(bstack1ll1111l_opy_) - 2:] == bstackl_opy_ (u"ࠩ࠯ࠤࠬઞ"):
      bstack1ll1111l_opy_ = bstack1ll1111l_opy_[:-2]
    return bstack1ll1111l_opy_
def bstack11lll1l1_opy_(path, bstack1ll1111l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111l11l1_opy_ = ET.parse(path)
    bstack1l1ll11l1_opy_ = bstack111l11l1_opy_.getroot()
    bstack1llllll11l_opy_ = None
    for suite in bstack1l1ll11l1_opy_.iter(bstackl_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩટ")):
      if bstackl_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫઠ") in suite.attrib:
        suite.attrib[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪડ")] += bstackl_opy_ (u"࠭ࠠࠨઢ") + bstack1ll1111l_opy_
        bstack1llllll11l_opy_ = suite
    bstack1l11lll1l_opy_ = None
    for robot in bstack1l1ll11l1_opy_.iter(bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ણ")):
      bstack1l11lll1l_opy_ = robot
    bstack1ll11l11l_opy_ = len(bstack1l11lll1l_opy_.findall(bstackl_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧત")))
    if bstack1ll11l11l_opy_ == 1:
      bstack1l11lll1l_opy_.remove(bstack1l11lll1l_opy_.findall(bstackl_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨથ"))[0])
      bstack11111l111_opy_ = ET.Element(bstackl_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩદ"), attrib={bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩધ"): bstackl_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬન"), bstackl_opy_ (u"࠭ࡩࡥࠩ઩"): bstackl_opy_ (u"ࠧࡴ࠲ࠪપ")})
      bstack1l11lll1l_opy_.insert(1, bstack11111l111_opy_)
      bstack11l11l1ll_opy_ = None
      for suite in bstack1l11lll1l_opy_.iter(bstackl_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ")):
        bstack11l11l1ll_opy_ = suite
      bstack11l11l1ll_opy_.append(bstack1llllll11l_opy_)
      bstack1ll11l1lll_opy_ = None
      for status in bstack1llllll11l_opy_.iter(bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩબ")):
        bstack1ll11l1lll_opy_ = status
      bstack11l11l1ll_opy_.append(bstack1ll11l1lll_opy_)
    bstack111l11l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨભ") + str(e))
def bstack1ll1l11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1111lll_opy_
  global CONFIG
  if bstackl_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣમ") in options:
    del options[bstackl_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤય")]
  bstack11ll111ll_opy_ = bstack1ll1l11l_opy_()
  for bstack1ll11ll111_opy_ in bstack11ll111ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ર"), str(bstack1ll11ll111_opy_), bstackl_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ઱"))
    bstack11lll1l1_opy_(path, bstack1ll1l11lll_opy_(bstack11ll111ll_opy_[bstack1ll11ll111_opy_]))
  bstack1llll11l_opy_()
  return bstack1l1111lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l11lll1_opy_(self, ff_profile_dir):
  global bstack1llll11l1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1llll11l1l_opy_(self, ff_profile_dir)
def bstack1lll1l111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11lllllll_opy_
  bstack11lll1l11_opy_ = []
  if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫલ") in CONFIG:
    bstack11lll1l11_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬળ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ઴")],
      pabot_args[bstackl_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧવ")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠧ࡮ࡩࡷࡧࠥશ")),
      pabot_args[bstackl_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤષ")],
      platform[0],
      bstack11lllllll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢસ")] or [(bstackl_opy_ (u"ࠣࠤહ"), None)]
    for platform in enumerate(bstack11lll1l11_opy_)
  ]
def bstack11111llll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1llllll_opy_=bstackl_opy_ (u"ࠩࠪ઺")):
  global bstack1lll1111ll_opy_
  self.platform_index = platform_index
  self.bstack11lll1ll1_opy_ = bstack1l1llllll_opy_
  bstack1lll1111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1111l_opy_
  global bstack1l111lll_opy_
  if not bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ઻") in item.options:
    item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ઼࠭")] = []
  for v in item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧઽ")]:
    if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬા") in v:
      item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩિ")].remove(v)
    if bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨી") in v:
      item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫુ")].remove(v)
  item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")].insert(0, bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭ૃ").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")].insert(0, bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ૅ").format(item.bstack11lll1ll1_opy_))
  if bstack1l111lll_opy_:
    item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].insert(0, bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫે").format(bstack1l111lll_opy_))
  return bstack1lll1111l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll1lll1ll_opy_(command, item_index):
  os.environ[bstackl_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪૈ")] = json.dumps(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૉ")][item_index % bstack1l1l1l11_opy_])
  global bstack1l111lll_opy_
  if bstack1l111lll_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૊"), bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩો") + str(
      item_index) + bstackl_opy_ (u"࠭ࠠࠨૌ") + bstack1l111lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ્࠭"),
                                    bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ૎") + str(item_index), 1)
def bstack1ll1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111l11111_opy_
  bstack1ll1lll1ll_opy_(command, item_index)
  return bstack111l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11lll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111l11111_opy_
  bstack1ll1lll1ll_opy_(command, item_index)
  return bstack111l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111l11111_opy_
  bstack1ll1lll1ll_opy_(command, item_index)
  return bstack111l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1111ll11_opy_(self, runner, quiet=False, capture=True):
  global bstack1111llll1_opy_
  bstack1ll1l1l1ll_opy_ = bstack1111llll1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ૏")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧૐ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l1l1ll_opy_
def bstack1ll11llll1_opy_(self, name, context, *args):
  os.environ[bstackl_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ૑")] = json.dumps(CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૒")][int(threading.current_thread()._name) % bstack1l1l1l11_opy_])
  global bstack1111ll1ll_opy_
  if name == bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ૓"):
    bstack1111ll1ll_opy_(self, name, context, *args)
    try:
      if not bstack1llll1l11l_opy_:
        bstack1l11llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11ll_opy_(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૔")) else context.browser
        bstack1l1ll1lll_opy_ = str(self.feature.name)
        bstack1l1ll111l_opy_(context, bstack1l1ll1lll_opy_)
        bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૕") + json.dumps(bstack1l1ll1lll_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬ૖"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૗").format(str(e)))
  elif name == bstackl_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૘"):
    bstack1111ll1ll_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstackl_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ૙")):
        self.driver_before_scenario = True
      if (not bstack1llll1l11l_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1ll1lll_opy_ = str(self.feature.name)
        bstack1l1ll1lll_opy_ = feature_name + bstackl_opy_ (u"࠭ࠠ࠮ࠢࠪ૚") + scenario_name
        bstack1l11llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11ll_opy_(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૛")) else context.browser
        if self.driver_before_scenario:
          bstack1l1ll111l_opy_(context, bstack1l1ll1lll_opy_)
          bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૜") + json.dumps(bstack1l1ll1lll_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬ૝"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ૞").format(str(e)))
  elif name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૟"):
    try:
      bstack1lllllllll_opy_ = args[0].status.name
      bstack1l11llll_opy_ = threading.current_thread().bstackSessionDriver if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૠ") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1lllllllll_opy_).lower() == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ૡ"):
        bstack1l1ll1llll_opy_ = bstackl_opy_ (u"ࠧࠨૢ")
        bstack111l1lll1_opy_ = bstackl_opy_ (u"ࠨࠩૣ")
        bstack1ll1111ll_opy_ = bstackl_opy_ (u"ࠩࠪ૤")
        try:
          import traceback
          bstack1l1ll1llll_opy_ = self.exception.__class__.__name__
          bstack1lll1l11l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111l1lll1_opy_ = bstackl_opy_ (u"ࠪࠤࠬ૥").join(bstack1lll1l11l1_opy_)
          bstack1ll1111ll_opy_ = bstack1lll1l11l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1ll11_opy_.format(str(e)))
        bstack1l1ll1llll_opy_ += bstack1ll1111ll_opy_
        bstack1ll111l1l_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ૦") + str(bstack111l1lll1_opy_)),
                            bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ૧"))
        if self.driver_before_scenario:
          bstack1l11l1ll1_opy_(getattr(context, bstackl_opy_ (u"࠭ࡰࡢࡩࡨࠫ૨"), None), bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ૩"), bstack1l1ll1llll_opy_)
          bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૪") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૫") + str(bstack111l1lll1_opy_)) + bstackl_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ૬"))
        if self.driver_before_scenario:
          bstack11l1ll111_opy_(bstack1l11llll_opy_, bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૭"), bstackl_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ૮") + str(bstack1l1ll1llll_opy_))
      else:
        bstack1ll111l1l_opy_(context, bstackl_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ૯"), bstackl_opy_ (u"ࠢࡪࡰࡩࡳࠧ૰"))
        if self.driver_before_scenario:
          bstack1l11l1ll1_opy_(getattr(context, bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭૱"), None), bstackl_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ૲"))
        bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ૳") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ૴")) + bstackl_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ૵"))
        if self.driver_before_scenario:
          bstack11l1ll111_opy_(bstack1l11llll_opy_, bstackl_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૶"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૷").format(str(e)))
  elif name == bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૸"):
    try:
      bstack1l11llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11ll_opy_(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨૹ")) else context.browser
      if context.failed is True:
        bstack1l1ll1111_opy_ = []
        bstack1l11l11ll_opy_ = []
        bstack111ll111_opy_ = []
        bstack1ll11ll1l_opy_ = bstackl_opy_ (u"ࠪࠫૺ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1ll1111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lll1l11l1_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l1l11l_opy_ = bstackl_opy_ (u"ࠫࠥ࠭ૻ").join(bstack1lll1l11l1_opy_)
            bstack1l11l11ll_opy_.append(bstack1ll1l1l11l_opy_)
            bstack111ll111_opy_.append(bstack1lll1l11l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1ll11_opy_.format(str(e)))
        bstack1l1ll1llll_opy_ = bstackl_opy_ (u"ࠬ࠭ૼ")
        for i in range(len(bstack1l1ll1111_opy_)):
          bstack1l1ll1llll_opy_ += bstack1l1ll1111_opy_[i] + bstack111ll111_opy_[i] + bstackl_opy_ (u"࠭࡜࡯ࠩ૽")
        bstack1ll11ll1l_opy_ = bstackl_opy_ (u"ࠧࠡࠩ૾").join(bstack1l11l11ll_opy_)
        if not self.driver_before_scenario:
          bstack1ll111l1l_opy_(context, bstack1ll11ll1l_opy_, bstackl_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ૿"))
          bstack1l11l1ll1_opy_(getattr(context, bstackl_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ଀"), None), bstackl_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଁ"), bstack1l1ll1llll_opy_)
          bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଂ") + json.dumps(bstack1ll11ll1l_opy_) + bstackl_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬଃ"))
          bstack11l1ll111_opy_(bstack1l11llll_opy_, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ଄"), bstackl_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧଅ") + str(bstack1l1ll1llll_opy_))
          bstack1ll1lll111_opy_ = bstack1l11l1ll_opy_(bstack1ll11ll1l_opy_, self.feature.name, logger)
          if (bstack1ll1lll111_opy_ != None):
            bstack1l11lll1_opy_.append(bstack1ll1lll111_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1ll111l1l_opy_(context, bstackl_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦଆ") + str(self.feature.name) + bstackl_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦଇ"), bstackl_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣଈ"))
          bstack1l11l1ll1_opy_(getattr(context, bstackl_opy_ (u"ࠫࡵࡧࡧࡦࠩଉ"), None), bstackl_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧଊ"))
          bstack1l11llll_opy_.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫଋ") + json.dumps(bstackl_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥଌ") + str(self.feature.name) + bstackl_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ଍")) + bstackl_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ଎"))
          bstack11l1ll111_opy_(bstack1l11llll_opy_, bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଏ"))
          bstack1ll1lll111_opy_ = bstack1l11l1ll_opy_(bstack1ll11ll1l_opy_, self.feature.name, logger)
          if (bstack1ll1lll111_opy_ != None):
            bstack1l11lll1_opy_.append(bstack1ll1lll111_opy_)
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଐ").format(str(e)))
  else:
    bstack1111ll1ll_opy_(self, name, context, *args)
  if name in [bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ଑"), bstackl_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ଒")]:
    bstack1111ll1ll_opy_(self, name, context, *args)
    if (name == bstackl_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨଓ") and self.driver_before_scenario) or (
            name == bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଔ") and not self.driver_before_scenario):
      try:
        bstack1l11llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11ll_opy_(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨକ")) else context.browser
        bstack1l11llll_opy_.quit()
      except Exception:
        pass
def bstack1111l1l1_opy_(config, startdir):
  return bstackl_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣଖ").format(bstackl_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଗ"))
notset = Notset()
def bstack1lll111l1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1l11lll_opy_
  if str(name).lower() == bstackl_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬଘ"):
    return bstackl_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧଙ")
  else:
    return bstack1l1l11lll_opy_(self, name, default, skip)
def bstack1ll1l1ll1_opy_(item, when):
  global bstack1l1l111ll_opy_
  try:
    bstack1l1l111ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1lll11ll_opy_():
  return
def bstack11l11lll_opy_(type, name, status, reason, bstack1ll1l111ll_opy_, bstack1l1l1lll_opy_):
  bstack1ll111l1_opy_ = {
    bstackl_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଚ"): type,
    bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଛ"): {}
  }
  if type == bstackl_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫଜ"):
    bstack1ll111l1_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଝ")][bstackl_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଞ")] = bstack1ll1l111ll_opy_
    bstack1ll111l1_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଟ")][bstackl_opy_ (u"࠭ࡤࡢࡶࡤࠫଠ")] = json.dumps(str(bstack1l1l1lll_opy_))
  if type == bstackl_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଡ"):
    bstack1ll111l1_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଢ")][bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧଣ")] = name
  if type == bstackl_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ତ"):
    bstack1ll111l1_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଥ")][bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଦ")] = status
    if status == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଧ"):
      bstack1ll111l1_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪନ")][bstackl_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ଩")] = json.dumps(str(reason))
  bstack1ll11l1l11_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧପ").format(json.dumps(bstack1ll111l1_opy_))
  return bstack1ll11l1l11_opy_
def bstack11lll1111_opy_(driver_command, response):
    if driver_command == bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଫ"):
        bstack1lll11l1ll_opy_.bstack1ll1lll1l1_opy_({
            bstackl_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪବ"): response[bstackl_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫଭ")],
            bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ମ"): bstack1lll11l1ll_opy_.current_test_uuid()
        })
def bstack1llll1ll1_opy_(item, call, rep):
  global bstack1llll1ll_opy_
  global bstack1ll1ll1lll_opy_
  global bstack1llll1l11l_opy_
  name = bstackl_opy_ (u"ࠧࠨଯ")
  try:
    if rep.when == bstackl_opy_ (u"ࠨࡥࡤࡰࡱ࠭ର"):
      bstack11ll111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1llll1l11l_opy_:
          name = str(rep.nodeid)
          bstack1ll11l111_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଱"), name, bstackl_opy_ (u"ࠪࠫଲ"), bstackl_opy_ (u"ࠫࠬଳ"), bstackl_opy_ (u"ࠬ࠭଴"), bstackl_opy_ (u"࠭ࠧଵ"))
          threading.current_thread().bstack1l1ll1ll1l_opy_ = name
          for driver in bstack1ll1ll1lll_opy_:
            if bstack11ll111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11l111_opy_)
      except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଶ").format(str(e)))
      try:
        bstack1l111111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩଷ"):
          status = bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩସ") if rep.outcome.lower() == bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪହ") else bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ଺")
          reason = bstackl_opy_ (u"ࠬ࠭଻")
          if status == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstackl_opy_ (u"ࠧࡪࡰࡩࡳࠬଽ") if status == bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨା") else bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨି")
          data = name + bstackl_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬୀ") if status == bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୁ") else name + bstackl_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨୂ") + reason
          bstack1lllll1ll_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨୃ"), bstackl_opy_ (u"ࠧࠨୄ"), bstackl_opy_ (u"ࠨࠩ୅"), bstackl_opy_ (u"ࠩࠪ୆"), level, data)
          for driver in bstack1ll1ll1lll_opy_:
            if bstack11ll111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lllll1ll_opy_)
      except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧେ").format(str(e)))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨୈ").format(str(e)))
  bstack1llll1ll_opy_(item, call, rep)
def bstack1lll1ll1l1_opy_(framework_name):
  global bstack111lllll1_opy_
  global bstack1lll11l111_opy_
  global bstack1ll1l1l111_opy_
  bstack111lllll1_opy_ = framework_name
  logger.info(bstack1l11ll11_opy_.format(bstack111lllll1_opy_.split(bstackl_opy_ (u"ࠬ࠳ࠧ୉"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l11ll1l1_opy_:
      Service.start = bstack11ll1ll11_opy_
      Service.stop = bstack1ll11l11_opy_
      webdriver.Remote.get = bstack111l11ll_opy_
      WebDriver.close = bstack1l1ll11ll_opy_
      WebDriver.quit = bstack1ll1lllll_opy_
      webdriver.Remote.__init__ = bstack1lll1lll11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1ll1l1ll_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1111llll_opy_ = getAccessibilityResultsSummary
    if not bstack1l11ll1l1_opy_ and bstack1lll11l1ll_opy_.on():
      webdriver.Remote.__init__ = bstack1ll11lllll_opy_
    if bstack1lll11l1ll_opy_.on():
      WebDriver.execute = bstack1l1ll1lll1_opy_
    bstack1lll11l111_opy_ = True
  except Exception as e:
    pass
  bstack1ll11ll11_opy_()
  if not bstack1lll11l111_opy_:
    bstack1ll1l11111_opy_(bstackl_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ୊"), bstack1111111l1_opy_)
  if bstack1ll11l1ll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l111l111_opy_
    except Exception as e:
      logger.error(bstack1lll1l1l1l_opy_.format(str(e)))
  if bstack1ll11llll_opy_():
    bstack1111l11ll_opy_(CONFIG, logger)
  if (bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ୋ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l11lll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1l1ll1_opy_
      except Exception as e:
        logger.warn(bstack11l111ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll1l1ll1_opy_
      except Exception as e:
        logger.debug(bstack1lll11l11l_opy_ + str(e))
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack11l111ll_opy_)
    Output.end_test = bstack11l111l11_opy_
    TestStatus.__init__ = bstack1ll11ll1ll_opy_
    QueueItem.__init__ = bstack11111llll_opy_
    pabot._create_items = bstack1lll1l111l_opy_
    try:
      from pabot import __version__ as bstack1ll111lll1_opy_
      if version.parse(bstack1ll111lll1_opy_) >= version.parse(bstackl_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨୌ")):
        pabot._run = bstack1llll1l1_opy_
      elif version.parse(bstack1ll111lll1_opy_) >= version.parse(bstackl_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱୍ࠩ")):
        pabot._run = bstack11lll1lll_opy_
      else:
        pabot._run = bstack1ll1l1l11_opy_
    except Exception as e:
      pabot._run = bstack1ll1l1l11_opy_
    pabot._create_command_for_execution = bstack1l1l1111_opy_
    pabot._report_results = bstack1ll1l11l1_opy_
  if bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ୎") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack1ll1l1lll1_opy_)
    Runner.run_hook = bstack1ll11llll1_opy_
    Step.run = bstack1111ll11_opy_
  if bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ୏") in str(framework_name).lower():
    if not bstack1l11ll1l1_opy_:
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
def bstack1111l1111_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ୐") in CONFIG and int(CONFIG[bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭୑")]) > 1:
    logger.warn(bstack1ll1111ll1_opy_)
def bstack111ll1ll_opy_(arg, bstack1l1111ll1_opy_, bstack1ll11lll1l_opy_=None):
  global CONFIG
  global bstack1l1111111_opy_
  global bstack1l11ll111_opy_
  global bstack1l11ll1l1_opy_
  global bstack1l1ll111l1_opy_
  bstack1lllll11_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ୒")
  if bstack1l1111ll1_opy_ and isinstance(bstack1l1111ll1_opy_, str):
    bstack1l1111ll1_opy_ = eval(bstack1l1111ll1_opy_)
  CONFIG = bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ୓")]
  bstack1l1111111_opy_ = bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ୔")]
  bstack1l11ll111_opy_ = bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୕")]
  bstack1l11ll1l1_opy_ = bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧୖ")]
  bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ୗ"), bstack1l11ll1l1_opy_)
  os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ୘")] = bstack1lllll11_opy_
  os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭୙")] = json.dumps(CONFIG)
  os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ୚")] = bstack1l1111111_opy_
  os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୛")] = str(bstack1l11ll111_opy_)
  os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩଡ଼")] = str(True)
  if bstack11l11l1l_opy_(arg, [bstackl_opy_ (u"ࠫ࠲ࡴࠧଢ଼"), bstackl_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭୞")]) != -1:
    os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧୟ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111llll11_opy_)
    return
  bstack1ll111ll1_opy_()
  global bstack11l11l11_opy_
  global bstack1ll1l111l_opy_
  global bstack11lllllll_opy_
  global bstack1l111lll_opy_
  global bstack11l11ll1_opy_
  global bstack1ll1l1l111_opy_
  global bstack1111lll1l_opy_
  arg.append(bstackl_opy_ (u"ࠢ࠮࡙ࠥୠ"))
  arg.append(bstackl_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦୡ"))
  arg.append(bstackl_opy_ (u"ࠤ࠰࡛ࠧୢ"))
  arg.append(bstackl_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤୣ"))
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
  if bstack1lllll11l1_opy_(CONFIG) and bstack1l1l1ll1l_opy_():
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
    logger.debug(bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ୤"))
  bstack11lllllll_opy_ = CONFIG.get(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୥"), {}).get(bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୦"))
  bstack1111lll1l_opy_ = True
  bstack1lll1ll1l1_opy_(bstack1l1l1lll1_opy_)
  os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ୧")] = CONFIG[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ୨")]
  os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ୩")] = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭୪")]
  os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ୫")] = bstack1l11ll1l1_opy_.__str__()
  from _pytest.config import main as bstack1111l11l_opy_
  bstack1111l11l_opy_(arg)
  if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ୬") in multiprocessing.current_process().__dict__.keys():
    for bstack1l11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1ll11lll1l_opy_.append(bstack1l11l11l_opy_)
def bstack1ll11ll1l1_opy_(arg):
  bstack1lll1ll1l1_opy_(bstack1111lllll_opy_)
  os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୭")] = str(bstack1l11ll111_opy_)
  from behave.__main__ import main as bstack1lllll1l1_opy_
  bstack1lllll1l1_opy_(arg)
def bstack1ll11l1l_opy_():
  logger.info(bstack1l1lll1lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭୮"), help=bstackl_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩ୯"))
  parser.add_argument(bstackl_opy_ (u"ࠩ࠰ࡹࠬ୰"), bstackl_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧୱ"), help=bstackl_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ୲"))
  parser.add_argument(bstackl_opy_ (u"ࠬ࠳࡫ࠨ୳"), bstackl_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬ୴"), help=bstackl_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨ୵"))
  parser.add_argument(bstackl_opy_ (u"ࠨ࠯ࡩࠫ୶"), bstackl_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ୷"), help=bstackl_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ୸"))
  bstack1l1111ll_opy_ = parser.parse_args()
  try:
    bstack1ll1l11ll_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ୹")
    if bstack1l1111ll_opy_.framework and bstack1l1111ll_opy_.framework not in (bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ୺"), bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ୻")):
      bstack1ll1l11ll_opy_ = bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭୼")
    bstack1l1ll11l1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l11ll_opy_)
    bstack1ll11ll1_opy_ = open(bstack1l1ll11l1l_opy_, bstackl_opy_ (u"ࠨࡴࠪ୽"))
    bstack1llll111l1_opy_ = bstack1ll11ll1_opy_.read()
    bstack1ll11ll1_opy_.close()
    if bstack1l1111ll_opy_.username:
      bstack1llll111l1_opy_ = bstack1llll111l1_opy_.replace(bstackl_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ୾"), bstack1l1111ll_opy_.username)
    if bstack1l1111ll_opy_.key:
      bstack1llll111l1_opy_ = bstack1llll111l1_opy_.replace(bstackl_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ୿"), bstack1l1111ll_opy_.key)
    if bstack1l1111ll_opy_.framework:
      bstack1llll111l1_opy_ = bstack1llll111l1_opy_.replace(bstackl_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ஀"), bstack1l1111ll_opy_.framework)
    file_name = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ஁")
    file_path = os.path.abspath(file_name)
    bstack11l1111l1_opy_ = open(file_path, bstackl_opy_ (u"࠭ࡷࠨஂ"))
    bstack11l1111l1_opy_.write(bstack1llll111l1_opy_)
    bstack11l1111l1_opy_.close()
    logger.info(bstack1lll111l_opy_)
    try:
      os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩஃ")] = bstack1l1111ll_opy_.framework if bstack1l1111ll_opy_.framework != None else bstackl_opy_ (u"ࠣࠤ஄")
      config = yaml.safe_load(bstack1llll111l1_opy_)
      config[bstackl_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஅ")] = bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩஆ")
      bstack1l111lll1_opy_(bstack11l11ll1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1lll_opy_.format(str(e)))
def bstack1l111lll1_opy_(bstack111l111l1_opy_, config, bstack1ll111ll1l_opy_={}):
  global bstack1l11ll1l1_opy_
  global bstack11ll111l_opy_
  if not config:
    return
  bstack1lll1l11_opy_ = bstack1ll1l11l1l_opy_ if not bstack1l11ll1l1_opy_ else (
    bstack11ll1l1l1_opy_ if bstackl_opy_ (u"ࠫࡦࡶࡰࠨஇ") in config else bstack11l1ll1l1_opy_)
  data = {
    bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧஈ"): config[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨஉ")],
    bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪஊ"): config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஋")],
    bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭஌"): bstack111l111l1_opy_,
    bstackl_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ஍"): os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭எ"), bstack11ll111l_opy_),
    bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧஏ"): bstack1lll111ll1_opy_,
    bstackl_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨஐ"): bstack11lll11l_opy_(),
    bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ஑"): {
      bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ஒ"): str(config[bstackl_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஓ")]) if bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஔ") in config else bstackl_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧக"),
      bstackl_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ஖"): bstack1lll1ll11_opy_(os.getenv(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ஗"), bstackl_opy_ (u"ࠢࠣ஘"))),
      bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪங"): bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩச"),
      bstackl_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ஛"): bstack1lll1l11_opy_,
      bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧஜ"): config[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ஝")] if config[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩஞ")] else bstackl_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣட"),
      bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ஠"): str(config[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஡")]) if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ஢") in config else bstackl_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧண"),
      bstackl_opy_ (u"ࠬࡵࡳࠨத"): sys.platform,
      bstackl_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ஥"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ஦")], bstack1ll111ll1l_opy_)
  try:
    response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠨࡒࡒࡗ࡙࠭஧"), bstack1ll11l1l1_opy_(bstack1l111ll1l_opy_), data, {
      bstackl_opy_ (u"ࠩࡤࡹࡹ࡮ࠧந"): (config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬன")], config[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧப")])
    })
    if response:
      logger.debug(bstack1ll11ll11l_opy_.format(bstack111l111l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1ll1l11l_opy_.format(str(e)))
def bstack1lll1ll11_opy_(framework):
  return bstackl_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ஫").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ஬").format(
    __version__)
def bstack1ll111ll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack11llllll1_opy_()
    logger.debug(bstack111lll111_opy_.format(str(CONFIG)))
    bstack1ll11lll1_opy_()
    bstack1ll1lll11l_opy_()
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ஭") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1lll11_opy_
  atexit.register(bstack1l111ll1_opy_)
  signal.signal(signal.SIGINT, bstack1l11l1111_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l1111_opy_)
def bstack1l1lll11_opy_(exctype, value, traceback):
  global bstack1ll1ll1lll_opy_
  try:
    for driver in bstack1ll1ll1lll_opy_:
      bstack11l1ll111_opy_(driver, bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨம"), bstackl_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧய") + str(value))
  except Exception:
    pass
  bstack1lllllll1l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lllllll1l_opy_(message=bstackl_opy_ (u"ࠪࠫர"), bstack1lll11lll1_opy_ = False):
  global CONFIG
  bstack11ll1l11l_opy_ = bstackl_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ற") if bstack1lll11lll1_opy_ else bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫல")
  try:
    if message:
      bstack1ll111ll1l_opy_ = {
        bstack11ll1l11l_opy_ : str(message)
      }
      bstack1l111lll1_opy_(bstack1lll11l1_opy_, CONFIG, bstack1ll111ll1l_opy_)
    else:
      bstack1l111lll1_opy_(bstack1lll11l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l1ll11_opy_.format(str(e)))
def bstack1lll1ll1_opy_(bstack1llll1111_opy_, size):
  bstack1l1l11ll1_opy_ = []
  while len(bstack1llll1111_opy_) > size:
    bstack111111lll_opy_ = bstack1llll1111_opy_[:size]
    bstack1l1l11ll1_opy_.append(bstack111111lll_opy_)
    bstack1llll1111_opy_ = bstack1llll1111_opy_[size:]
  bstack1l1l11ll1_opy_.append(bstack1llll1111_opy_)
  return bstack1l1l11ll1_opy_
def bstack1ll11lll11_opy_(args):
  if bstackl_opy_ (u"࠭࠭࡮ࠩள") in args and bstackl_opy_ (u"ࠧࡱࡦࡥࠫழ") in args:
    return True
  return False
def run_on_browserstack(bstack11l11l1l1_opy_=None, bstack1ll11lll1l_opy_=None, bstack1l1ll11lll_opy_=False):
  global CONFIG
  global bstack1l1111111_opy_
  global bstack1l11ll111_opy_
  global bstack11ll111l_opy_
  bstack1lllll11_opy_ = bstackl_opy_ (u"ࠨࠩவ")
  bstack1lll11lll_opy_(bstack111ll1l11_opy_, logger)
  if bstack11l11l1l1_opy_ and isinstance(bstack11l11l1l1_opy_, str):
    bstack11l11l1l1_opy_ = eval(bstack11l11l1l1_opy_)
  if bstack11l11l1l1_opy_:
    CONFIG = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩஶ")]
    bstack1l1111111_opy_ = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫஷ")]
    bstack1l11ll111_opy_ = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ஸ")]
    bstack1l1ll111l1_opy_.bstack11lll111_opy_(bstackl_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧஹ"), bstack1l11ll111_opy_)
    bstack1lllll11_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஺")
  if not bstack1l1ll11lll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111llll11_opy_)
      return
    if sys.argv[1] == bstackl_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ஻") or sys.argv[1] == bstackl_opy_ (u"ࠨ࠯ࡹࠫ஼"):
      logger.info(bstackl_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ஽").format(__version__))
      return
    if sys.argv[1] == bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩா"):
      bstack1ll11l1l_opy_()
      return
  args = sys.argv
  bstack1ll111ll1_opy_()
  global bstack11l11l11_opy_
  global bstack1l1l1l11_opy_
  global bstack1111lll1l_opy_
  global bstack1l1ll1l111_opy_
  global bstack1ll1l111l_opy_
  global bstack11lllllll_opy_
  global bstack1l111lll_opy_
  global bstack1llllll11_opy_
  global bstack11l11ll1_opy_
  global bstack1ll1l1l111_opy_
  global bstack1ll111111l_opy_
  bstack1l1l1l11_opy_ = len(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧி")])
  if not bstack1lllll11_opy_:
    if args[1] == bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬீ") or args[1] == bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧு"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧூ")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௃"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௄")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௅"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪெ")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ே"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧை")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௉"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨொ")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩோ"):
      bstack1lllll11_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪௌ")
      args = args[2:]
    else:
      if not bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ்ࠧ") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௎")]).lower() in [bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௏"), bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨௐ")]:
        bstack1lllll11_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௑")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௒")]).lower() == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௓"):
        bstack1lllll11_opy_ = bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௔")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௕")]).lower() == bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖"):
        bstack1lllll11_opy_ = bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ௗ")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௘")]).lower() == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௙"):
        bstack1lllll11_opy_ = bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௛")]).lower() == bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜"):
        bstack1lllll11_opy_ = bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௝")
        args = args[1:]
      else:
        os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௞")] = bstack1lllll11_opy_
        bstack11111l11_opy_(bstack11lllll1_opy_)
  os.environ[bstackl_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ௟")] = bstack1lllll11_opy_
  bstack11ll111l_opy_ = bstack1lllll11_opy_
  global bstack11l11ll11_opy_
  if bstack11l11l1l1_opy_:
    try:
      os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௠")] = bstack1lllll11_opy_
      bstack1l111lll1_opy_(bstack1llll1l1l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l1ll11_opy_.format(str(e)))
  global bstack1l1l11111_opy_
  global bstack111lll1l1_opy_
  global bstack1ll1111l1_opy_
  global bstack1l1l111l_opy_
  global bstack1l1lll111l_opy_
  global bstack11ll1ll1l_opy_
  global bstack1llll11l1l_opy_
  global bstack111l11111_opy_
  global bstack1lll1111ll_opy_
  global bstack1lll1111l_opy_
  global bstack1ll1l11l11_opy_
  global bstack1111ll1ll_opy_
  global bstack1111llll1_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l111ll11_opy_
  global bstack1l1l11lll_opy_
  global bstack1l1l111ll_opy_
  global bstack1l1111lll_opy_
  global bstack1llll1ll_opy_
  global bstack11111lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l11111_opy_ = webdriver.Remote.__init__
    bstack111lll1l1_opy_ = WebDriver.quit
    bstack1ll1l11l11_opy_ = WebDriver.close
    bstack1l1l1l1l1_opy_ = WebDriver.get
    bstack11111lll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l11ll11_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1lllll11l1_opy_(CONFIG) and bstack1l1l1ll1l_opy_():
    if bstack11l1l1ll_opy_() < version.parse(bstack1ll11lll_opy_):
      logger.error(bstack11lll1ll_opy_.format(bstack11l1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111ll11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lll1l1l1l_opy_.format(str(e)))
  if bstack1lllll11_opy_ != bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௡") or (bstack1lllll11_opy_ == bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௢") and not bstack11l11l1l1_opy_):
    bstack1111l1l1l_opy_()
  if (bstack1lllll11_opy_ in [bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௣"), bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"), bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ௥")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l11lll1_opy_
        bstack1l1lll111l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l111ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1l111l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll11l11l_opy_ + str(e))
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack11l111ll_opy_)
    if bstack1lllll11_opy_ != bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௦"):
      bstack1llll11l_opy_()
    bstack1ll1111l1_opy_ = Output.end_test
    bstack11ll1ll1l_opy_ = TestStatus.__init__
    bstack111l11111_opy_ = pabot._run
    bstack1lll1111ll_opy_ = QueueItem.__init__
    bstack1lll1111l_opy_ = pabot._create_command_for_execution
    bstack1l1111lll_opy_ = pabot._report_results
  if bstack1lllll11_opy_ == bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ௧"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack1ll1l1lll1_opy_)
    bstack1111ll1ll_opy_ = Runner.run_hook
    bstack1111llll1_opy_ = Step.run
  if bstack1lllll11_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௨"):
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
      logger.debug(bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ௩"))
  if bstack1lllll11_opy_ in bstack1l1ll1l11_opy_:
    try:
      framework_name = bstackl_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ௪") if bstack1lllll11_opy_ in [bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௫"), bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௬"), bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௭")] else bstack1l1llllll1_opy_(bstack1lllll11_opy_)
      bstack1lll11l1ll_opy_.launch(CONFIG, {
        bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ௮"): bstackl_opy_ (u"ࠪࡿ࠵ࢃ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ௯").format(framework_name) if bstack1lllll11_opy_ == bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௰") and bstack1lllll111l_opy_() else framework_name,
        bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௱"): bstack1111l11l1_opy_(framework_name),
        bstackl_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௲"): __version__
      })
    except Exception as e:
      logger.debug(bstack111l1l1ll_opy_.format(bstackl_opy_ (u"ࠧࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ௳"), str(e)))
  if bstack1lllll11_opy_ in bstack1lll11ll1l_opy_:
    try:
      framework_name = bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௴") if bstack1lllll11_opy_ in [bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௵"), bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௶")] else bstack1lllll11_opy_
      if bstack1l11ll1l1_opy_ and bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ௷") in CONFIG and CONFIG[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ௸")] == True:
        if bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭௹") in CONFIG:
          os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ௺")] = os.getenv(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ௻"), json.dumps(CONFIG[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௼")]))
          CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ௽")].pop(bstackl_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ௾"), None)
          CONFIG[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ௿")].pop(bstackl_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫఀ"), None)
        bstack11l1l11l1_opy_, bstack111lll1ll_opy_ = bstack1l1ll1l1ll_opy_.bstack1l1llll11l_opy_(CONFIG, bstack1lllll11_opy_, bstack1111l11l1_opy_(framework_name))
        if not bstack11l1l11l1_opy_ is None:
          os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬఁ")] = bstack11l1l11l1_opy_
          os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧం")] = str(bstack111lll1ll_opy_)
    except Exception as e:
      logger.debug(bstack111l1l1ll_opy_.format(bstackl_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩః"), str(e)))
  if bstack1lllll11_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪఄ"):
    bstack1111lll1l_opy_ = True
    if bstack11l11l1l1_opy_ and bstack1l1ll11lll_opy_:
      bstack11lllllll_opy_ = CONFIG.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨఅ"), {}).get(bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఆ"))
      bstack1lll1ll1l1_opy_(bstack111ll1l1l_opy_)
    elif bstack11l11l1l1_opy_:
      bstack11lllllll_opy_ = CONFIG.get(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪఇ"), {}).get(bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఈ"))
      global bstack1ll1ll1lll_opy_
      try:
        if bstack1ll11lll11_opy_(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఉ")]) and multiprocessing.current_process().name == bstackl_opy_ (u"ࠩ࠳ࠫఊ"):
          bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఋ")].remove(bstackl_opy_ (u"ࠫ࠲ࡳࠧఌ"))
          bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఍")].remove(bstackl_opy_ (u"࠭ࡰࡥࡤࠪఎ"))
          bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఏ")] = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఐ")][0]
          with open(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ఑")], bstackl_opy_ (u"ࠪࡶࠬఒ")) as f:
            bstack1ll1ll1ll1_opy_ = f.read()
          bstack1l11lll11_opy_ = bstackl_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣఓ").format(str(bstack11l11l1l1_opy_))
          bstack1ll1ll1l_opy_ = bstack1l11lll11_opy_ + bstack1ll1ll1ll1_opy_
          bstack1lll11ll1_opy_ = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఔ")] + bstackl_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨక")
          with open(bstack1lll11ll1_opy_, bstackl_opy_ (u"ࠧࡸࠩఖ")):
            pass
          with open(bstack1lll11ll1_opy_, bstackl_opy_ (u"ࠣࡹ࠮ࠦగ")) as f:
            f.write(bstack1ll1ll1l_opy_)
          import subprocess
          bstack1ll1lll11_opy_ = subprocess.run([bstackl_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤఘ"), bstack1lll11ll1_opy_])
          if os.path.exists(bstack1lll11ll1_opy_):
            os.unlink(bstack1lll11ll1_opy_)
          os._exit(bstack1ll1lll11_opy_.returncode)
        else:
          if bstack1ll11lll11_opy_(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఙ")]):
            bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")].remove(bstackl_opy_ (u"ࠬ࠳࡭ࠨఛ"))
            bstack11l11l1l1_opy_[bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")].remove(bstackl_opy_ (u"ࠧࡱࡦࡥࠫఝ"))
            bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")] = bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬట")][0]
          bstack1lll1ll1l1_opy_(bstack111ll1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstackl_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭డ")] = bstackl_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧఢ")
          mod_globals[bstackl_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨణ")] = os.path.abspath(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪత")])
          exec(open(bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫథ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstackl_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩద").format(str(e)))
          for driver in bstack1ll1ll1lll_opy_:
            bstack1ll11lll1l_opy_.append({
              bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨధ"): bstack11l11l1l1_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧన")],
              bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ఩"): str(e),
              bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬప"): multiprocessing.current_process().name
            })
            bstack11l1ll111_opy_(driver, bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఫ"), bstackl_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦబ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1ll1lll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11ll111_opy_, CONFIG, logger)
      bstack1lll1l1l11_opy_()
      bstack1111l1111_opy_()
      bstack1l1111ll1_opy_ = {
        bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ"): args[0],
        bstackl_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪమ"): CONFIG,
        bstackl_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬయ"): bstack1l1111111_opy_,
        bstackl_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧర"): bstack1l11ll111_opy_
      }
      percy.bstack1ll1l1lll_opy_()
      if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఱ") in CONFIG:
        bstack1l1111l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1l11ll_opy_ = manager.list()
        if bstack1ll11lll11_opy_(args):
          for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪల")]):
            if index == 0:
              bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫళ")] = args
            bstack1l1111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1111ll1_opy_, bstack1lll1l11ll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఴ")]):
            bstack1l1111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1111ll1_opy_, bstack1lll1l11ll_opy_)))
        for t in bstack1l1111l11_opy_:
          t.start()
        for t in bstack1l1111l11_opy_:
          t.join()
        bstack1llllll11_opy_ = list(bstack1lll1l11ll_opy_)
      else:
        if bstack1ll11lll11_opy_(args):
          bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭వ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1111ll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll1ll1l1_opy_(bstack111ll1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstackl_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭శ")] = bstackl_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧష")
          mod_globals[bstackl_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨస")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lllll11_opy_ == bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭హ") or bstack1lllll11_opy_ == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ఺"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack11l111ll_opy_)
    bstack1lll1l1l11_opy_()
    bstack1lll1ll1l1_opy_(bstack111l1111_opy_)
    if bstackl_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ఻") in args:
      i = args.index(bstackl_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ఼"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11l11l11_opy_))
    args.insert(0, str(bstackl_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩఽ")))
    if bstack1lll11l1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll11ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll11111l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstackl_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧా"),
        ).parse_args(bstack1lll11ll_opy_)
        args.insert(args.index(bstack1ll11111l1_opy_[0]), str(bstackl_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪి")))
        args.insert(args.index(bstack1ll11111l1_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫీ"))))
        if bstack11llll111_opy_(os.environ.get(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ు"))) and str(os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ూ"), bstackl_opy_ (u"ࠪࡲࡺࡲ࡬ࠨృ"))) != bstackl_opy_ (u"ࠫࡳࡻ࡬࡭ࠩౄ"):
          for bstack1ll1111111_opy_ in bstack1ll11111l1_opy_:
            args.remove(bstack1ll1111111_opy_)
          bstack1lll1l11l_opy_ = os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ౅")).split(bstackl_opy_ (u"࠭ࠬࠨె"))
          for bstack1l1lll1ll1_opy_ in bstack1lll1l11l_opy_:
            args.append(bstack1l1lll1ll1_opy_)
      except Exception as e:
        logger.error(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥే").format(e))
    pabot.main(args)
  elif bstack1lllll11_opy_ == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩై"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack11l111ll_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ౉") in a:
        bstack1ll1l111l_opy_ = int(a.split(bstackl_opy_ (u"ࠪ࠾ࠬొ"))[1])
      if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨో") in a:
        bstack11lllllll_opy_ = str(a.split(bstackl_opy_ (u"ࠬࡀࠧౌ"))[1])
      if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ్࠭") in a:
        bstack1l111lll_opy_ = str(a.split(bstackl_opy_ (u"ࠧ࠻ࠩ౎"))[1])
    bstack11llll11l_opy_ = None
    if bstackl_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ౏") in args:
      i = args.index(bstackl_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ౐"))
      args.pop(i)
      bstack11llll11l_opy_ = args.pop(i)
    if bstack11llll11l_opy_ is not None:
      global bstack1lllll11l_opy_
      bstack1lllll11l_opy_ = bstack11llll11l_opy_
    bstack1lll1ll1l1_opy_(bstack111l1111_opy_)
    run_cli(args)
    if bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ౑") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11lll1l_opy_.append(bstack1l11l11l_opy_)
  elif bstack1lllll11_opy_ == bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ౒"):
    bstack1l1l1111l_opy_ = bstack1llll1llll_opy_(args, logger, CONFIG, bstack1l11ll1l1_opy_)
    bstack1l1l1111l_opy_.bstack11l1l1l1l_opy_()
    bstack1lll1l1l11_opy_()
    bstack1l1ll1l111_opy_ = True
    bstack1ll1l1l111_opy_ = bstack1l1l1111l_opy_.bstack1l1llll11_opy_()
    bstack1l1l1111l_opy_.bstack1l1111ll1_opy_(bstack1llll1l11l_opy_)
    bstack11l11ll1_opy_ = bstack1l1l1111l_opy_.bstack1llll11111_opy_(bstack111ll1ll_opy_, {
      bstackl_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭౓"): bstack1l1111111_opy_,
      bstackl_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ౔"): bstack1l11ll111_opy_,
      bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐౕࠪ"): bstack1l11ll1l1_opy_
    })
    bstack1ll111111l_opy_ = 1 if len(bstack11l11ll1_opy_) > 0 else 0
  elif bstack1lllll11_opy_ == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨౖ"):
    try:
      from behave.__main__ import main as bstack1lllll1l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l11111_opy_(e, bstack1ll1l1lll1_opy_)
    bstack1lll1l1l11_opy_()
    bstack1l1ll1l111_opy_ = True
    bstack1l1llll1_opy_ = 1
    if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ౗") in CONFIG:
      bstack1l1llll1_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪౘ")]
    bstack11llll1l_opy_ = int(bstack1l1llll1_opy_) * int(len(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౙ")]))
    config = Configuration(args)
    bstack1l1ll111_opy_ = config.paths
    if len(bstack1l1ll111_opy_) == 0:
      import glob
      pattern = bstackl_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫౚ")
      bstack1ll1llll1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1llll1l_opy_)
      config = Configuration(args)
      bstack1l1ll111_opy_ = config.paths
    bstack11l1111l_opy_ = [os.path.normpath(item) for item in bstack1l1ll111_opy_]
    bstack1ll1l1ll1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1l11l11_opy_ = [item for item in bstack1ll1l1ll1l_opy_ if item not in bstack11l1111l_opy_]
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ౛"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l1111l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1ll11ll_opy_)))
                    for bstack1ll1ll11ll_opy_ in bstack11l1111l_opy_]
    bstack11l1llll_opy_ = []
    for spec in bstack11l1111l_opy_:
      bstack1lll1l1l1_opy_ = []
      bstack1lll1l1l1_opy_ += bstack1l1l11l11_opy_
      bstack1lll1l1l1_opy_.append(spec)
      bstack11l1llll_opy_.append(bstack1lll1l1l1_opy_)
    execution_items = []
    for bstack1lll1l1l1_opy_ in bstack11l1llll_opy_:
      for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౜")]):
        item = {}
        item[bstackl_opy_ (u"ࠨࡣࡵ࡫ࠬౝ")] = bstackl_opy_ (u"ࠩࠣࠫ౞").join(bstack1lll1l1l1_opy_)
        item[bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ౟")] = index
        execution_items.append(item)
    bstack11ll1111_opy_ = bstack1lll1ll1_opy_(execution_items, bstack11llll1l_opy_)
    for execution_item in bstack11ll1111_opy_:
      bstack1l1111l11_opy_ = []
      for item in execution_item:
        bstack1l1111l11_opy_.append(bstack1l1lll11l1_opy_(name=str(item[bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪౠ")]),
                                             target=bstack1ll11ll1l1_opy_,
                                             args=(item[bstackl_opy_ (u"ࠬࡧࡲࡨࠩౡ")],)))
      for t in bstack1l1111l11_opy_:
        t.start()
      for t in bstack1l1111l11_opy_:
        t.join()
  else:
    bstack11111l11_opy_(bstack11lllll1_opy_)
  if not bstack11l11l1l1_opy_:
    bstack1ll1ll1l1_opy_()
def browserstack_initialize(bstack1l1lll111_opy_=None):
  run_on_browserstack(bstack1l1lll111_opy_, None, True)
def bstack1ll1ll1l1_opy_():
  global CONFIG
  global bstack11ll111l_opy_
  global bstack1ll111111l_opy_
  bstack1lll11l1ll_opy_.stop()
  bstack1lll11l1ll_opy_.bstack11llll1l1_opy_()
  if bstack1l1ll1l1ll_opy_.bstack1ll11111ll_opy_(CONFIG):
    bstack1l1ll1l1ll_opy_.bstack1lllll1ll1_opy_()
  [bstack1l1ll11l11_opy_, bstack1lll1l111_opy_] = bstack1ll1llllll_opy_()
  if bstack1l1ll11l11_opy_ is not None and bstack11111lll1_opy_() != -1:
    sessions = bstack1l1l1ll1_opy_(bstack1l1ll11l11_opy_)
    bstack11ll1l1ll_opy_(sessions, bstack1lll1l111_opy_)
  if bstack11ll111l_opy_ == bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ౢ") and bstack1ll111111l_opy_ != 0:
    sys.exit(bstack1ll111111l_opy_)
def bstack1l1llllll1_opy_(bstack1lllllll1_opy_):
  if bstack1lllllll1_opy_:
    return bstack1lllllll1_opy_.capitalize()
  else:
    return bstackl_opy_ (u"ࠧࠨౣ")
def bstack1l1ll1ll1_opy_(bstack1l1ll11ll1_opy_):
  if bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭౤") in bstack1l1ll11ll1_opy_ and bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౥")] != bstackl_opy_ (u"ࠪࠫ౦"):
    return bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ౧")]
  else:
    bstack1l11111ll_opy_ = bstackl_opy_ (u"ࠧࠨ౨")
    if bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭౩") in bstack1l1ll11ll1_opy_ and bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ౪")] != None:
      bstack1l11111ll_opy_ += bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ౫")] + bstackl_opy_ (u"ࠤ࠯ࠤࠧ౬")
      if bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠪࡳࡸ࠭౭")] == bstackl_opy_ (u"ࠦ࡮ࡵࡳࠣ౮"):
        bstack1l11111ll_opy_ += bstackl_opy_ (u"ࠧ࡯ࡏࡔࠢࠥ౯")
      bstack1l11111ll_opy_ += (bstack1l1ll11ll1_opy_[bstackl_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ౰")] or bstackl_opy_ (u"ࠧࠨ౱"))
      return bstack1l11111ll_opy_
    else:
      bstack1l11111ll_opy_ += bstack1l1llllll1_opy_(bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ౲")]) + bstackl_opy_ (u"ࠤࠣࠦ౳") + (
              bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ౴")] or bstackl_opy_ (u"ࠫࠬ౵")) + bstackl_opy_ (u"ࠧ࠲ࠠࠣ౶")
      if bstack1l1ll11ll1_opy_[bstackl_opy_ (u"࠭࡯ࡴࠩ౷")] == bstackl_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣ౸"):
        bstack1l11111ll_opy_ += bstackl_opy_ (u"࡙ࠣ࡬ࡲࠥࠨ౹")
      bstack1l11111ll_opy_ += bstack1l1ll11ll1_opy_[bstackl_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭౺")] or bstackl_opy_ (u"ࠪࠫ౻")
      return bstack1l11111ll_opy_
def bstack11l1ll11l_opy_(bstack1l1l11l1_opy_):
  if bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠦࡩࡵ࡮ࡦࠤ౼"):
    return bstackl_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ౽")
  elif bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౾"):
    return bstackl_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ౿")
  elif bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಀ"):
    return bstackl_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಁ")
  elif bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤಂ"):
    return bstackl_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಃ")
  elif bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ಄"):
    return bstackl_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಅ")
  elif bstack1l1l11l1_opy_ == bstackl_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣಆ"):
    return bstackl_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಇ")
  else:
    return bstackl_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ಈ") + bstack1l1llllll1_opy_(
      bstack1l1l11l1_opy_) + bstackl_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಉ")
def bstack1ll1llll11_opy_(session):
  return bstackl_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫಊ").format(
    session[bstackl_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩಋ")], bstack1l1ll1ll1_opy_(session), bstack11l1ll11l_opy_(session[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬಌ")]),
    bstack11l1ll11l_opy_(session[bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ಍")]),
    bstack1l1llllll1_opy_(session[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩಎ")] or session[bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩಏ")] or bstackl_opy_ (u"ࠪࠫಐ")) + bstackl_opy_ (u"ࠦࠥࠨ಑") + (session[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಒ")] or bstackl_opy_ (u"࠭ࠧಓ")),
    session[bstackl_opy_ (u"ࠧࡰࡵࠪಔ")] + bstackl_opy_ (u"ࠣࠢࠥಕ") + session[bstackl_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ಖ")], session[bstackl_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬಗ")] or bstackl_opy_ (u"ࠫࠬಘ"),
    session[bstackl_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩಙ")] if session[bstackl_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪಚ")] else bstackl_opy_ (u"ࠧࠨಛ"))
def bstack11ll1l1ll_opy_(sessions, bstack1lll1l111_opy_):
  try:
    bstack1111l1l11_opy_ = bstackl_opy_ (u"ࠣࠤಜ")
    if not os.path.exists(bstack1l1lllll11_opy_):
      os.mkdir(bstack1l1lllll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstackl_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧಝ")), bstackl_opy_ (u"ࠪࡶࠬಞ")) as f:
      bstack1111l1l11_opy_ = f.read()
    bstack1111l1l11_opy_ = bstack1111l1l11_opy_.replace(bstackl_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨಟ"), str(len(sessions)))
    bstack1111l1l11_opy_ = bstack1111l1l11_opy_.replace(bstackl_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬಠ"), bstack1lll1l111_opy_)
    bstack1111l1l11_opy_ = bstack1111l1l11_opy_.replace(bstackl_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧಡ"),
                                              sessions[0].get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫಢ")) if sessions[0] else bstackl_opy_ (u"ࠨࠩಣ"))
    with open(os.path.join(bstack1l1lllll11_opy_, bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ತ")), bstackl_opy_ (u"ࠪࡻࠬಥ")) as stream:
      stream.write(bstack1111l1l11_opy_.split(bstackl_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨದ"))[0])
      for session in sessions:
        stream.write(bstack1ll1llll11_opy_(session))
      stream.write(bstack1111l1l11_opy_.split(bstackl_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩಧ"))[1])
    logger.info(bstackl_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩನ").format(bstack1l1lllll11_opy_));
  except Exception as e:
    logger.debug(bstack1l111l11_opy_.format(str(e)))
def bstack1l1l1ll1_opy_(bstack1l1ll11l11_opy_):
  global CONFIG
  try:
    host = bstackl_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ಩") if bstackl_opy_ (u"ࠨࡣࡳࡴࠬಪ") in CONFIG else bstackl_opy_ (u"ࠩࡤࡴ࡮࠭ಫ")
    user = CONFIG[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬಬ")]
    key = CONFIG[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧಭ")]
    bstack1ll1l111l1_opy_ = bstackl_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫಮ") if bstackl_opy_ (u"࠭ࡡࡱࡲࠪಯ") in CONFIG else bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩರ")
    url = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭ಱ").format(user, key, host, bstack1ll1l111l1_opy_,
                                                                                bstack1l1ll11l11_opy_)
    headers = {
      bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨಲ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ಳ"),
    }
    proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ಴")], response.json()))
  except Exception as e:
    logger.debug(bstack11lllll11_opy_.format(str(e)))
def bstack1ll1llllll_opy_():
  global CONFIG
  global bstack1lll111ll1_opy_
  try:
    if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨವ") in CONFIG:
      host = bstackl_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩಶ") if bstackl_opy_ (u"ࠧࡢࡲࡳࠫಷ") in CONFIG else bstackl_opy_ (u"ࠨࡣࡳ࡭ࠬಸ")
      user = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಹ")]
      key = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭಺")]
      bstack1ll1l111l1_opy_ = bstackl_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ಻") if bstackl_opy_ (u"ࠬࡧࡰࡱ಼ࠩ") in CONFIG else bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨಽ")
      url = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧಾ").format(user, key, host, bstack1ll1l111l1_opy_)
      headers = {
        bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧಿ"): bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬೀ"),
      }
      if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬು") in CONFIG:
        params = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩೂ"): CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨೃ")], bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೄ"): CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೅")]}
      else:
        params = {bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ೆ"): CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೇ")]}
      proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1111l111_opy_ = response.json()[0][bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭ೈ")]
        if bstack1111l111_opy_:
          bstack1lll1l111_opy_ = bstack1111l111_opy_[bstackl_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ೉")].split(bstackl_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫೊ"))[0] + bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧೋ") + bstack1111l111_opy_[
            bstackl_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪೌ")]
          logger.info(bstack1l111111l_opy_.format(bstack1lll1l111_opy_))
          bstack1lll111ll1_opy_ = bstack1111l111_opy_[bstackl_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ್ࠫ")]
          bstack1ll11l11ll_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ೎")]
          if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೏") in CONFIG:
            bstack1ll11l11ll_opy_ += bstackl_opy_ (u"ࠫࠥ࠭೐") + CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೑")]
          if bstack1ll11l11ll_opy_ != bstack1111l111_opy_[bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒")]:
            logger.debug(bstack1ll1ll111l_opy_.format(bstack1111l111_opy_[bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೓")], bstack1ll11l11ll_opy_))
          return [bstack1111l111_opy_[bstackl_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ೔")], bstack1lll1l111_opy_]
    else:
      logger.warn(bstack1l1l1l111_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll111_opy_.format(str(e)))
  return [None, None]
def bstack111llll1l_opy_(url, bstack1l1ll111ll_opy_=False):
  global CONFIG
  global bstack11l11111_opy_
  if not bstack11l11111_opy_:
    hostname = bstack1lllll111_opy_(url)
    is_private = bstack1llll1ll1l_opy_(hostname)
    if (bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ೕ") in CONFIG and not bstack11llll111_opy_(CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧೖ")])) and (is_private or bstack1l1ll111ll_opy_):
      bstack11l11111_opy_ = hostname
def bstack1lllll111_opy_(url):
  return urlparse(url).hostname
def bstack1llll1ll1l_opy_(hostname):
  for bstack1ll1l1111_opy_ in bstack111111ll_opy_:
    regex = re.compile(bstack1ll1l1111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1llll11ll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1l111l_opy_
  if not bstack1l1ll1l1ll_opy_.bstack1ll111lll_opy_(CONFIG, bstack1ll1l111l_opy_):
    logger.warning(bstackl_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ೗"))
    return {}
  try:
    results = driver.execute_script(bstackl_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࡷࡧࡱࡸࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤࡍࡅࡕࡡࡕࡉࡘ࡛ࡌࡕࡕࠪ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰࠣࡁࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡧࡹࡩࡳࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡵ࡬ࡷࡧࠫࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠰ࡧࡥࡹࡧࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡤࡨࡩࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣࡗࡋࡓࡖࡎࡗࡗࡤࡘࡅࡔࡒࡒࡒࡘࡋࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨࡺࡪࡴࡴࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠣࡧࡦࡺࡣࡩࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦ࡬ࡨࡧࡹ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁ࠮ࡁࠊࠡࠢࠣࠤࠧࠨࠢ೘"))
    return results
  except Exception:
    logger.error(bstackl_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣ೙"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1l111l_opy_
  if not bstack1l1ll1l1ll_opy_.bstack1ll111lll_opy_(CONFIG, bstack1ll1l111l_opy_):
    logger.warning(bstackl_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦ೚"))
    return {}
  try:
    bstack1l1llll1l1_opy_ = driver.execute_script(bstackl_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࡺࡪࡴࡴࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡉࡈࡘࡤࡘࡅࡔࡗࡏࡘࡘࡥࡓࡖࡏࡐࡅࡗ࡟ࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴࠠ࠾ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡲࡦ࡯ࡲࡺࡪࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣࡗࡋࡓࡖࡎࡗࡗࡤ࡙ࡕࡎࡏࡄࡖ࡞ࡥࡒࡆࡕࡓࡓࡓ࡙ࡅࠨ࠮ࠣࡪࡳ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡳࡱࡼࡥࠩࡧࡹࡩࡳࡺ࠮ࡥࡧࡷࡥ࡮ࡲ࠮ࡴࡷࡰࡱࡦࡸࡹࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡥࡩࡪࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡓࡖࡏࡐࡅࡗ࡟࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪࡼࡥ࡯ࡶࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨ࡮ࡪࡩࡴࠩࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠢࠣࠤ೛"))
    return bstack1l1llll1l1_opy_
  except Exception:
    logger.error(bstackl_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥ೜"))
    return {}