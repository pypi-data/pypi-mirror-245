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
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll11l1l1_opy_, bstack11l111l1l_opy_
class bstack1ll1l1111l_opy_:
  working_dir = os.getcwd()
  bstack1111l1ll_opy_ = False
  config = {}
  binary_path = bstackl_opy_ (u"࠭ࠧዖ")
  bstack111ll1l1ll_opy_ = bstackl_opy_ (u"ࠧࠨ዗")
  bstack111ll1llll_opy_ = False
  bstack11l1111ll1_opy_ = None
  bstack11l11ll111_opy_ = {}
  bstack11l11l1ll1_opy_ = 300
  bstack11l11ll11l_opy_ = False
  logger = None
  bstack111llll11l_opy_ = False
  bstack111lll1lll_opy_ = bstackl_opy_ (u"ࠨࠩዘ")
  bstack11l11ll1l1_opy_ = {
    bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩዙ") : 1,
    bstackl_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫዚ") : 2,
    bstackl_opy_ (u"ࠫࡪࡪࡧࡦࠩዛ") : 3,
    bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬዜ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1l11l_opy_(self):
    bstack11l111l11l_opy_ = bstackl_opy_ (u"࠭ࠧዝ")
    bstack11l11l11l1_opy_ = sys.platform
    bstack111lll111l_opy_ = bstackl_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ዞ")
    if re.match(bstackl_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣዟ"), bstack11l11l11l1_opy_) != None:
      bstack11l111l11l_opy_ = bstack11lll1l1l1_opy_ + bstackl_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥዠ")
      self.bstack111lll1lll_opy_ = bstackl_opy_ (u"ࠪࡱࡦࡩࠧዡ")
    elif re.match(bstackl_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤዢ"), bstack11l11l11l1_opy_) != None:
      bstack11l111l11l_opy_ = bstack11lll1l1l1_opy_ + bstackl_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨዣ")
      bstack111lll111l_opy_ = bstackl_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤዤ")
      self.bstack111lll1lll_opy_ = bstackl_opy_ (u"ࠧࡸ࡫ࡱࠫዥ")
    else:
      bstack11l111l11l_opy_ = bstack11lll1l1l1_opy_ + bstackl_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦዦ")
      self.bstack111lll1lll_opy_ = bstackl_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨዧ")
    return bstack11l111l11l_opy_, bstack111lll111l_opy_
  def bstack11l111111l_opy_(self):
    try:
      bstack11l11111ll_opy_ = [os.path.join(expanduser(bstackl_opy_ (u"ࠥࢂࠧየ")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫዩ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l11111ll_opy_:
        if(self.bstack11l111l1l1_opy_(path)):
          return path
      raise bstackl_opy_ (u"࡛ࠧ࡮ࡢ࡮ࡥࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤዪ")
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣያ").format(e))
  def bstack11l111l1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111lll1ll1_opy_(self, bstack11l111l11l_opy_, bstack111lll111l_opy_):
    try:
      bstack11l11l1lll_opy_ = self.bstack11l111111l_opy_()
      bstack111lll11l1_opy_ = os.path.join(bstack11l11l1lll_opy_, bstackl_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪዬ"))
      bstack111llllll1_opy_ = os.path.join(bstack11l11l1lll_opy_, bstack111lll111l_opy_)
      if os.path.exists(bstack111llllll1_opy_):
        self.logger.info(bstackl_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥይ").format(bstack111llllll1_opy_))
        return bstack111llllll1_opy_
      if os.path.exists(bstack111lll11l1_opy_):
        self.logger.info(bstackl_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢዮ").format(bstack111lll11l1_opy_))
        return self.bstack11l1111lll_opy_(bstack111lll11l1_opy_, bstack111lll111l_opy_)
      self.logger.info(bstackl_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣዯ").format(bstack11l111l11l_opy_))
      response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠫࡌࡋࡔࠨደ"), bstack11l111l11l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111lll11l1_opy_, bstackl_opy_ (u"ࠬࡽࡢࠨዱ")) as file:
          file.write(response.content)
        self.logger.info(bstack111llll1ll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࡥ࡭ࡳࡧࡲࡺࡡࡽ࡭ࡵࡥࡰࡢࡶ࡫ࢁࠧዲ"))
        return self.bstack11l1111lll_opy_(bstack111lll11l1_opy_, bstack111lll111l_opy_)
      else:
        raise(bstack111llll1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࡷࡹࡧࡴࡶࡵࡢࡧࡴࡪࡥࡾࠤዳ"))
    except:
      self.logger.error(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧዴ"))
  def bstack111llll111_opy_(self, bstack11l111l11l_opy_, bstack111lll111l_opy_):
    try:
      bstack111llllll1_opy_ = self.bstack111lll1ll1_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_)
      bstack111ll1l1l1_opy_ = self.bstack111lll11ll_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_, bstack111llllll1_opy_)
      return bstack111llllll1_opy_, bstack111ll1l1l1_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨድ").format(e))
    return bstack111llllll1_opy_, False
  def bstack111lll11ll_opy_(self, bstack11l111l11l_opy_, bstack111lll111l_opy_, bstack111llllll1_opy_, bstack11l111ll1l_opy_ = 0):
    if bstack11l111ll1l_opy_ > 1:
      return False
    if bstack111llllll1_opy_ == None or os.path.exists(bstack111llllll1_opy_) == False:
      self.logger.warn(bstackl_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣዶ"))
      bstack111llllll1_opy_ = self.bstack111lll1ll1_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_)
      self.bstack111lll11ll_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_, bstack111llllll1_opy_, bstack11l111ll1l_opy_+1)
    bstack11l111ll11_opy_ = bstackl_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤዷ")
    command = bstackl_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫዸ").format(bstack111llllll1_opy_)
    bstack11l1111l1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l111ll11_opy_, bstack11l1111l1l_opy_) != None:
      return True
    else:
      self.logger.error(bstackl_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧዹ"))
      bstack111llllll1_opy_ = self.bstack111lll1ll1_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_)
      self.bstack111lll11ll_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_, bstack111llllll1_opy_, bstack11l111ll1l_opy_+1)
  def bstack11l1111lll_opy_(self, bstack111lll11l1_opy_, bstack111lll111l_opy_):
    try:
      working_dir = os.path.dirname(bstack111lll11l1_opy_)
      shutil.unpack_archive(bstack111lll11l1_opy_, working_dir)
      bstack111llllll1_opy_ = os.path.join(working_dir, bstack111lll111l_opy_)
      os.chmod(bstack111llllll1_opy_, 0o755)
      return bstack111llllll1_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣዺ"))
  def bstack111lllll11_opy_(self):
    try:
      percy = str(self.config.get(bstackl_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧዻ"), bstackl_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣዼ"))).lower()
      if percy != bstackl_opy_ (u"ࠥࡸࡷࡻࡥࠣዽ"):
        return False
      self.bstack111ll1llll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨዾ").format(e))
  def init(self, bstack1111l1ll_opy_, config, logger):
    self.bstack1111l1ll_opy_ = bstack1111l1ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lllll11_opy_():
      return
    self.bstack11l11ll111_opy_ = config.get(bstackl_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫዿ"), {})
    try:
      bstack11l111l11l_opy_, bstack111lll111l_opy_ = self.bstack111ll1l11l_opy_()
      bstack111llllll1_opy_, bstack111ll1l1l1_opy_ = self.bstack111llll111_opy_(bstack11l111l11l_opy_, bstack111lll111l_opy_)
      if bstack111ll1l1l1_opy_:
        self.binary_path = bstack111llllll1_opy_
        thread = Thread(target=self.bstack111lll1l1l_opy_)
        thread.start()
      else:
        self.bstack111llll11l_opy_ = True
        self.logger.error(bstackl_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥጀ").format(bstack111llllll1_opy_))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣጁ").format(e))
  def bstack111ll1lll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࠬጂ"), bstackl_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬጃ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstackl_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢጄ").format(logfile))
      self.bstack111ll1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧጅ").format(e))
  def bstack111lll1l1l_opy_(self):
    bstack11l11l11ll_opy_ = self.bstack11l11l1l1l_opy_()
    if bstack11l11l11ll_opy_ == None:
      self.bstack111llll11l_opy_ = True
      self.logger.error(bstackl_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣጆ"))
      return False
    command_args = [bstackl_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢጇ") if self.bstack1111l1ll_opy_ else bstackl_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫገ")]
    bstack111lllll1l_opy_ = self.bstack111llll1l1_opy_()
    if bstack111lllll1l_opy_ != None:
      command_args.append(bstackl_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢጉ").format(bstack111lllll1l_opy_))
    env = os.environ.copy()
    env[bstackl_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢጊ")] = bstack11l11l11ll_opy_
    bstack11l111l111_opy_ = [self.binary_path]
    self.bstack111ll1lll1_opy_()
    self.bstack11l1111ll1_opy_ = self.bstack11l1111111_opy_(bstack11l111l111_opy_ + command_args, env)
    self.logger.debug(bstackl_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦጋ"))
    bstack11l111ll1l_opy_ = 0
    while self.bstack11l1111ll1_opy_.poll() == None:
      bstack11l1111l11_opy_ = self.bstack11l11l1l11_opy_()
      if bstack11l1111l11_opy_:
        self.logger.debug(bstackl_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢጌ"))
        self.bstack11l11ll11l_opy_ = True
        return True
      bstack11l111ll1l_opy_ += 1
      self.logger.debug(bstackl_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣግ").format(bstack11l111ll1l_opy_))
      time.sleep(2)
    self.logger.error(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦጎ").format(bstack11l111ll1l_opy_))
    self.bstack111llll11l_opy_ = True
    return False
  def bstack11l11l1l11_opy_(self, bstack11l111ll1l_opy_ = 0):
    try:
      if bstack11l111ll1l_opy_ > 10:
        return False
      bstack11l111llll_opy_ = os.environ.get(bstackl_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧጏ"), bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩጐ"))
      bstack111lll1l11_opy_ = bstack11l111llll_opy_ + bstack11lll11ll1_opy_
      response = requests.get(bstack111lll1l11_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11l11l1l1l_opy_(self):
    bstack11l11l111l_opy_ = bstackl_opy_ (u"ࠩࡤࡴࡵ࠭጑") if self.bstack1111l1ll_opy_ else bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬጒ")
    bstack11ll1l11l1_opy_ = bstackl_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠥጓ").format(self.config[bstackl_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪጔ")], bstack11l11l111l_opy_)
    uri = bstack1ll11l1l1_opy_(bstack11ll1l11l1_opy_)
    try:
      response = bstack11l111l1l_opy_(bstackl_opy_ (u"࠭ࡇࡆࡖࠪጕ"), uri, {}, {bstackl_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ጖"): (self.config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ጗")], self.config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጘ")])})
      if response.status_code == 200:
        bstack11l11lll11_opy_ = response.json()
        if bstackl_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤጙ") in bstack11l11lll11_opy_:
          return bstack11l11lll11_opy_[bstackl_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥጚ")]
        else:
          raise bstackl_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬጛ").format(bstack11l11lll11_opy_)
      else:
        raise bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨጜ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣጝ").format(e))
  def bstack111llll1l1_opy_(self):
    bstack111lll1111_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦጞ"))
    try:
      if bstackl_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪጟ") not in self.bstack11l11ll111_opy_:
        self.bstack11l11ll111_opy_[bstackl_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫጠ")] = 2
      with open(bstack111lll1111_opy_, bstackl_opy_ (u"ࠫࡼ࠭ጡ")) as fp:
        json.dump(self.bstack11l11ll111_opy_, fp)
      return bstack111lll1111_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧጢ").format(e))
  def bstack11l1111111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll1lll_opy_ == bstackl_opy_ (u"࠭ࡷࡪࡰࠪጣ"):
        bstack111ll1ll11_opy_ = [bstackl_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨጤ"), bstackl_opy_ (u"ࠨ࠱ࡦࠫጥ")]
        cmd = bstack111ll1ll11_opy_ + cmd
      cmd = bstackl_opy_ (u"ࠩࠣࠫጦ").join(cmd)
      self.logger.debug(bstackl_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢጧ").format(cmd))
      with open(self.bstack111ll1l1ll_opy_, bstackl_opy_ (u"ࠦࡦࠨጨ")) as bstack11l111l1ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l111l1ll_opy_, text=True, stderr=bstack11l111l1ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111llll11l_opy_ = True
      self.logger.error(bstackl_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢጩ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l11ll11l_opy_:
        self.logger.info(bstackl_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢጪ"))
        cmd = [self.binary_path, bstackl_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥጫ")]
        self.bstack11l1111111_opy_(cmd)
        self.bstack11l11ll11l_opy_ = False
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣጬ").format(cmd, e))
  def bstack1ll1l1lll_opy_(self):
    if not self.bstack111ll1llll_opy_:
      return
    try:
      bstack11l11111l1_opy_ = 0
      while not self.bstack11l11ll11l_opy_ and bstack11l11111l1_opy_ < self.bstack11l11l1ll1_opy_:
        if self.bstack111llll11l_opy_:
          self.logger.info(bstackl_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢጭ"))
          return
        time.sleep(1)
        bstack11l11111l1_opy_ += 1
      os.environ[bstackl_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩጮ")] = str(self.bstack11l11ll1ll_opy_())
      self.logger.info(bstackl_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧጯ"))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨጰ").format(e))
  def bstack11l11ll1ll_opy_(self):
    if self.bstack1111l1ll_opy_:
      return
    try:
      bstack11l11l1111_opy_ = [platform[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫጱ")].lower() for platform in self.config.get(bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪጲ"), [])]
      bstack111ll1ll1l_opy_ = sys.maxsize
      bstack11l111lll1_opy_ = bstackl_opy_ (u"ࠨࠩጳ")
      for browser in bstack11l11l1111_opy_:
        if browser in self.bstack11l11ll1l1_opy_:
          bstack111lllllll_opy_ = self.bstack11l11ll1l1_opy_[browser]
        if bstack111lllllll_opy_ < bstack111ll1ll1l_opy_:
          bstack111ll1ll1l_opy_ = bstack111lllllll_opy_
          bstack11l111lll1_opy_ = browser
      return bstack11l111lll1_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥጴ").format(e))