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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11lll11l11_opy_, bstack111111ll_opy_, bstack11lll11ll_opy_, bstack1lllll1l11_opy_
from bstack_utils.messages import bstack111lllll_opy_, bstack1lll1l1l1l_opy_
from bstack_utils.proxy import bstack1ll1l1l1l_opy_, bstack1l1ll1ll11_opy_
from browserstack_sdk.bstack1l1l11ll_opy_ import *
from browserstack_sdk.bstack1l11l1l11l_opy_ import *
bstack1l1ll111l1_opy_ = Config.get_instance()
def bstack1l11111l1l_opy_(config):
    return config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪგ")]
def bstack11llll11ll_opy_(config):
    return config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬდ")]
def bstack1l1lll1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1lllll1_opy_(obj):
    values = []
    bstack11ll11ll1l_opy_ = re.compile(bstackl_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢე"), re.I)
    for key in obj.keys():
        if bstack11ll11ll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1llllll_opy_(config):
    tags = []
    tags.extend(bstack11l1lllll1_opy_(os.environ))
    tags.extend(bstack11l1lllll1_opy_(config))
    return tags
def bstack11ll1l1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll1llll1_opy_(bstack11ll11l1ll_opy_):
    if not bstack11ll11l1ll_opy_:
        return bstackl_opy_ (u"ࠫࠬვ")
    return bstackl_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨზ").format(bstack11ll11l1ll_opy_.name, bstack11ll11l1ll_opy_.email)
def bstack11lllll11l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll11l111_opy_ = repo.common_dir
        info = {
            bstackl_opy_ (u"ࠨࡳࡩࡣࠥთ"): repo.head.commit.hexsha,
            bstackl_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥი"): repo.git.rev_parse(repo.head.commit, short=True),
            bstackl_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣკ"): repo.active_branch.name,
            bstackl_opy_ (u"ࠤࡷࡥ࡬ࠨლ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨმ"): bstack11ll1llll1_opy_(repo.head.commit.committer),
            bstackl_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧნ"): repo.head.commit.committed_datetime.isoformat(),
            bstackl_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧო"): bstack11ll1llll1_opy_(repo.head.commit.author),
            bstackl_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦპ"): repo.head.commit.authored_datetime.isoformat(),
            bstackl_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣჟ"): repo.head.commit.message,
            bstackl_opy_ (u"ࠣࡴࡲࡳࡹࠨრ"): repo.git.rev_parse(bstackl_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦს")),
            bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦტ"): bstack11ll11l111_opy_,
            bstackl_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢუ"): subprocess.check_output([bstackl_opy_ (u"ࠧ࡭ࡩࡵࠤფ"), bstackl_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤქ"), bstackl_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥღ")]).strip().decode(
                bstackl_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧყ")),
            bstackl_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦშ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧჩ"): repo.git.rev_list(
                bstackl_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦც").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11lll11111_opy_ = []
        for remote in remotes:
            bstack11l1ll1ll1_opy_ = {
                bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥძ"): remote.name,
                bstackl_opy_ (u"ࠨࡵࡳ࡮ࠥწ"): remote.url,
            }
            bstack11lll11111_opy_.append(bstack11l1ll1ll1_opy_)
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧჭ"): bstackl_opy_ (u"ࠣࡩ࡬ࡸࠧხ"),
            **info,
            bstackl_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥჯ"): bstack11lll11111_opy_
        }
    except Exception as err:
        print(bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨჰ").format(err))
        return {}
def bstack11ll1lll_opy_():
    env = os.environ
    if (bstackl_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤჱ") in env and len(env[bstackl_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥჲ")]) > 0) or (
            bstackl_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧჳ") in env and len(env[bstackl_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨჴ")]) > 0):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨჵ"): bstackl_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥჶ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨჷ"): env.get(bstackl_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢჸ")),
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢჹ"): env.get(bstackl_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣჺ")),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ჻"): env.get(bstackl_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢჼ"))
        }
    if env.get(bstackl_opy_ (u"ࠤࡆࡍࠧჽ")) == bstackl_opy_ (u"ࠥࡸࡷࡻࡥࠣჾ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨჿ"))):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄀ"): bstackl_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᄁ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᄂ"): env.get(bstackl_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᄃ")),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᄄ"): env.get(bstackl_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᄅ")),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᄆ"): env.get(bstackl_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᄇ"))
        }
    if env.get(bstackl_opy_ (u"ࠨࡃࡊࠤᄈ")) == bstackl_opy_ (u"ࠢࡵࡴࡸࡩࠧᄉ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᄊ"))):
        return {
            bstackl_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄋ"): bstackl_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᄌ"),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄍ"): env.get(bstackl_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᄎ")),
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄏ"): env.get(bstackl_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᄐ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄑ"): env.get(bstackl_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᄒ"))
        }
    if env.get(bstackl_opy_ (u"ࠥࡇࡎࠨᄓ")) == bstackl_opy_ (u"ࠦࡹࡸࡵࡦࠤᄔ") and env.get(bstackl_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᄕ")) == bstackl_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᄖ"):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᄗ"): bstackl_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᄘ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᄙ"): None,
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄚ"): None,
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᄛ"): None
        }
    if env.get(bstackl_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᄜ")) and env.get(bstackl_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᄝ")):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᄞ"): bstackl_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᄟ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᄠ"): env.get(bstackl_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᄡ")),
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᄢ"): None,
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᄣ"): env.get(bstackl_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᄤ"))
        }
    if env.get(bstackl_opy_ (u"ࠢࡄࡋࠥᄥ")) == bstackl_opy_ (u"ࠣࡶࡵࡹࡪࠨᄦ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᄧ"))):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᄨ"): bstackl_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᄩ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᄪ"): env.get(bstackl_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᄫ")),
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᄬ"): None,
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄭ"): env.get(bstackl_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᄮ"))
        }
    if env.get(bstackl_opy_ (u"ࠥࡇࡎࠨᄯ")) == bstackl_opy_ (u"ࠦࡹࡸࡵࡦࠤᄰ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᄱ"))):
        return {
            bstackl_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄲ"): bstackl_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᄳ"),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄴ"): env.get(bstackl_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᄵ")),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄶ"): env.get(bstackl_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᄷ")),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᄸ"): env.get(bstackl_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᄹ"))
        }
    if env.get(bstackl_opy_ (u"ࠢࡄࡋࠥᄺ")) == bstackl_opy_ (u"ࠣࡶࡵࡹࡪࠨᄻ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᄼ"))):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᄽ"): bstackl_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᄾ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᄿ"): env.get(bstackl_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᅀ")),
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅁ"): env.get(bstackl_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᅂ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅃ"): env.get(bstackl_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᅄ"))
        }
    if env.get(bstackl_opy_ (u"ࠦࡈࡏࠢᅅ")) == bstackl_opy_ (u"ࠧࡺࡲࡶࡧࠥᅆ") and bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᅇ"))):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅈ"): bstackl_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᅉ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅊ"): env.get(bstackl_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᅋ")),
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅌ"): env.get(bstackl_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᅍ")) or env.get(bstackl_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᅎ")),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅏ"): env.get(bstackl_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᅐ"))
        }
    if bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᅑ"))):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᅒ"): bstackl_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᅓ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅔ"): bstackl_opy_ (u"ࠨࡻࡾࡽࢀࠦᅕ").format(env.get(bstackl_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᅖ")), env.get(bstackl_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᅗ"))),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅘ"): env.get(bstackl_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᅙ")),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅚ"): env.get(bstackl_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᅛ"))
        }
    if bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᅜ"))):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅝ"): bstackl_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᅞ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅟ"): bstackl_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᅠ").format(env.get(bstackl_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᅡ")), env.get(bstackl_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᅢ")), env.get(bstackl_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᅣ")), env.get(bstackl_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᅤ"))),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅥ"): env.get(bstackl_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᅦ")),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅧ"): env.get(bstackl_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᅨ"))
        }
    if env.get(bstackl_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᅩ")) and env.get(bstackl_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᅪ")):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstackl_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᅬ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): bstackl_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᅮ").format(env.get(bstackl_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᅯ")), env.get(bstackl_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᅰ")), env.get(bstackl_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᅱ"))),
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅲ"): env.get(bstackl_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᅳ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅴ"): env.get(bstackl_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᅵ"))
        }
    if any([env.get(bstackl_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᅶ")), env.get(bstackl_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᅷ")), env.get(bstackl_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᅸ"))]):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅹ"): bstackl_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᅺ"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅻ"): env.get(bstackl_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᅼ")),
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅽ"): env.get(bstackl_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᅾ")),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅿ"): env.get(bstackl_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᆀ"))
        }
    if env.get(bstackl_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᆁ")):
        return {
            bstackl_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆂ"): bstackl_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᆃ"),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆄ"): env.get(bstackl_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᆅ")),
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆆ"): env.get(bstackl_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᆇ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆈ"): env.get(bstackl_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᆉ"))
        }
    if env.get(bstackl_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᆊ")) or env.get(bstackl_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᆋ")):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆌ"): bstackl_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᆍ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆎ"): env.get(bstackl_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᆏ")),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆐ"): bstackl_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᆑ") if env.get(bstackl_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᆒ")) else None,
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆓ"): env.get(bstackl_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᆔ"))
        }
    if any([env.get(bstackl_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᆕ")), env.get(bstackl_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᆖ")), env.get(bstackl_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᆗ"))]):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᆘ"): bstackl_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᆙ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆚ"): None,
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆛ"): env.get(bstackl_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᆜ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆝ"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᆞ"))
        }
    if env.get(bstackl_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᆟ")):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆠ"): bstackl_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᆡ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆢ"): env.get(bstackl_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᆣ")),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆤ"): bstackl_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᆥ").format(env.get(bstackl_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᆦ"))) if env.get(bstackl_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᆧ")) else None,
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆨ"): env.get(bstackl_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᆩ"))
        }
    if bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᆪ"))):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨᆫ"): bstackl_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥᆬ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆭ"): env.get(bstackl_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣᆮ")),
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆯ"): env.get(bstackl_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤᆰ")),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆱ"): env.get(bstackl_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᆲ"))
        }
    if bstack11llll111_opy_(env.get(bstackl_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥᆳ"))):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᆴ"): bstackl_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧᆵ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆶ"): bstackl_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢᆷ").format(env.get(bstackl_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫᆸ")), env.get(bstackl_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬᆹ")), env.get(bstackl_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩᆺ"))),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆻ"): env.get(bstackl_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨᆼ")),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆽ"): env.get(bstackl_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨᆾ"))
        }
    if env.get(bstackl_opy_ (u"ࠢࡄࡋࠥᆿ")) == bstackl_opy_ (u"ࠣࡶࡵࡹࡪࠨᇀ") and env.get(bstackl_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤᇁ")) == bstackl_opy_ (u"ࠥ࠵ࠧᇂ"):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇃ"): bstackl_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧᇄ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇅ"): bstackl_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥᇆ").format(env.get(bstackl_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬᇇ"))),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇈ"): None,
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇉ"): None,
        }
    if env.get(bstackl_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢᇊ")):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇋ"): bstackl_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣᇌ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇍ"): None,
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇎ"): env.get(bstackl_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥᇏ")),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇐ"): env.get(bstackl_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇑ"))
        }
    if any([env.get(bstackl_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣᇒ")), env.get(bstackl_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨᇓ")), env.get(bstackl_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧᇔ")), env.get(bstackl_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤᇕ"))]):
        return {
            bstackl_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇖ"): bstackl_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨᇗ"),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇘ"): None,
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇙ"): env.get(bstackl_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᇚ")) or None,
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇛ"): env.get(bstackl_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇜ"), 0)
        }
    if env.get(bstackl_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᇝ")):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᇞ"): bstackl_opy_ (u"ࠦࡌࡵࡃࡅࠤᇟ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇠ"): None,
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇡ"): env.get(bstackl_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇢ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇣ"): env.get(bstackl_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣᇤ"))
        }
    if env.get(bstackl_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᇥ")):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇦ"): bstackl_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣᇧ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇨ"): env.get(bstackl_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇩ")),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇪ"): env.get(bstackl_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᇫ")),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇬ"): env.get(bstackl_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᇭ"))
        }
    return {bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇮ"): None}
def get_host_info():
    return {
        bstackl_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣᇯ"): platform.node(),
        bstackl_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤᇰ"): platform.system(),
        bstackl_opy_ (u"ࠣࡶࡼࡴࡪࠨᇱ"): platform.machine(),
        bstackl_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᇲ"): platform.version(),
        bstackl_opy_ (u"ࠥࡥࡷࡩࡨࠣᇳ"): platform.architecture()[0]
    }
def bstack1l1l1ll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll1l1lll_opy_():
    if bstack1l1ll111l1_opy_.get_property(bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᇴ")):
        return bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᇵ")
    return bstackl_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬᇶ")
def bstack11l1ll11l1_opy_(driver):
    info = {
        bstackl_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᇷ"): driver.capabilities,
        bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᇸ"): driver.session_id,
        bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᇹ"): driver.capabilities.get(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᇺ"), None),
        bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᇻ"): driver.capabilities.get(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᇼ"), None),
        bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᇽ"): driver.capabilities.get(bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᇾ"), None),
    }
    if bstack11ll1l1lll_opy_() == bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᇿ"):
        info[bstackl_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪሀ")] = bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩሁ") if bstack1111l1ll_opy_() else bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ሂ")
    return info
def bstack1111l1ll_opy_():
    if bstack1l1ll111l1_opy_.get_property(bstackl_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫሃ")):
        return True
    if bstack11llll111_opy_(os.environ.get(bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧሄ"), None)):
        return True
    return False
def bstack11l111l1l_opy_(bstack11ll111l1l_opy_, url, data, config):
    headers = config.get(bstackl_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨህ"), None)
    proxies = bstack1ll1l1l1l_opy_(config, url)
    auth = config.get(bstackl_opy_ (u"ࠨࡣࡸࡸ࡭࠭ሆ"), None)
    response = requests.request(
            bstack11ll111l1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll1ll1_opy_(bstack1llll1111_opy_, size):
    bstack1l1l11ll1_opy_ = []
    while len(bstack1llll1111_opy_) > size:
        bstack111111lll_opy_ = bstack1llll1111_opy_[:size]
        bstack1l1l11ll1_opy_.append(bstack111111lll_opy_)
        bstack1llll1111_opy_ = bstack1llll1111_opy_[size:]
    bstack1l1l11ll1_opy_.append(bstack1llll1111_opy_)
    return bstack1l1l11ll1_opy_
def bstack11l1llll1l_opy_(message, bstack11ll1l11ll_opy_=False):
    os.write(1, bytes(message, bstackl_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨሇ")))
    os.write(1, bytes(bstackl_opy_ (u"ࠪࡠࡳ࠭ለ"), bstackl_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪሉ")))
    if bstack11ll1l11ll_opy_:
        with open(bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫሊ") + os.environ[bstackl_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬላ")] + bstackl_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬሌ"), bstackl_opy_ (u"ࠨࡣࠪል")) as f:
            f.write(message + bstackl_opy_ (u"ࠩ࡟ࡲࠬሎ"))
def bstack11lll111ll_opy_():
    return os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ሏ")].lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩሐ")
def bstack1ll11l1l1_opy_(bstack11ll1l11l1_opy_):
    return bstackl_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫሑ").format(bstack11lll11l11_opy_, bstack11ll1l11l1_opy_)
def bstack111l11lll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"࡚࠭ࠨሒ")
def bstack11ll11l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstackl_opy_ (u"࡛ࠧࠩሓ"))) - datetime.datetime.fromisoformat(start.rstrip(bstackl_opy_ (u"ࠨ࡜ࠪሔ")))).total_seconds() * 1000
def bstack11ll1111l1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫሕ")
def bstack11ll1lllll_opy_(bstack11ll11llll_opy_):
    date_format = bstackl_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨሖ")
    bstack11ll1l111l_opy_ = datetime.datetime.strptime(bstack11ll11llll_opy_, date_format)
    return bstack11ll1l111l_opy_.isoformat() + bstackl_opy_ (u"ࠫ࡟࠭ሗ")
def bstack11ll1ll1l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬመ")
    else:
        return bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ሙ")
def bstack11llll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬሚ")
def bstack11ll1l1111_opy_(val):
    return val.__str__().lower() == bstackl_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧማ")
def bstack1l1l11l11l_opy_(bstack11lll111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11lll111l1_opy_ as e:
                print(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤሜ").format(func.__name__, bstack11lll111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll1l1l11_opy_(bstack11ll11l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11l1l1_opy_(cls, *args, **kwargs)
            except bstack11lll111l1_opy_ as e:
                print(bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥም").format(bstack11ll11l1l1_opy_.__name__, bstack11lll111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll1l1l11_opy_
    else:
        return decorator
def bstack1ll1ll1111_opy_(bstack1l111ll1l1_opy_):
    if bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨሞ") in bstack1l111ll1l1_opy_ and bstack11ll1l1111_opy_(bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩሟ")]):
        return False
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨሠ") in bstack1l111ll1l1_opy_ and bstack11ll1l1111_opy_(bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩሡ")]):
        return False
    return True
def bstack1lllll111l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll11l1111_opy_(hub_url):
    if bstack11l1l1ll_opy_() <= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨሢ")):
        if hub_url != bstackl_opy_ (u"ࠩࠪሣ"):
            return bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦሤ") + hub_url + bstackl_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣሥ")
        return bstack11lll11ll_opy_
    if hub_url != bstackl_opy_ (u"ࠬ࠭ሦ"):
        return bstackl_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣሧ") + hub_url + bstackl_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣረ")
    return bstack1lllll1l11_opy_
def bstack11ll111lll_opy_():
    return isinstance(os.getenv(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧሩ")), str)
def bstack1lllll111_opy_(url):
    return urlparse(url).hostname
def bstack1llll1ll1l_opy_(hostname):
    for bstack1ll1l1111_opy_ in bstack111111ll_opy_:
        regex = re.compile(bstack1ll1l1111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1lll111_opy_(bstack11ll111111_opy_, file_name, logger):
    bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫሪ")), bstack11ll111111_opy_)
    try:
        if not os.path.exists(bstack111l1111l_opy_):
            os.makedirs(bstack111l1111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬራ")), bstack11ll111111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstackl_opy_ (u"ࠫࡼ࠭ሬ")):
                pass
            with open(file_path, bstackl_opy_ (u"ࠧࡽࠫࠣር")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111lllll_opy_.format(str(e)))
def bstack11l1lll1l1_opy_(file_name, key, value, logger):
    file_path = bstack11l1lll111_opy_(bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ሮ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll1l11_opy_ = json.load(open(file_path, bstackl_opy_ (u"ࠧࡳࡤࠪሯ")))
        else:
            bstack1l1lll1l11_opy_ = {}
        bstack1l1lll1l11_opy_[key] = value
        with open(file_path, bstackl_opy_ (u"ࠣࡹ࠮ࠦሰ")) as outfile:
            json.dump(bstack1l1lll1l11_opy_, outfile)
def bstack1l1l1l1ll_opy_(file_name, logger):
    file_path = bstack11l1lll111_opy_(bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩሱ"), file_name, logger)
    bstack1l1lll1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstackl_opy_ (u"ࠪࡶࠬሲ")) as bstack1lll1llll1_opy_:
            bstack1l1lll1l11_opy_ = json.load(bstack1lll1llll1_opy_)
    return bstack1l1lll1l11_opy_
def bstack1lll11lll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨሳ") + file_path + bstackl_opy_ (u"ࠬࠦࠧሴ") + str(e))
def bstack11l1l1ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstackl_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣስ")
def bstack111ll11l_opy_(config):
    if bstackl_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሶ") in config:
        del (config[bstackl_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧሷ")])
        return False
    if bstack11l1l1ll_opy_() < version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨሸ")):
        return False
    if bstack11l1l1ll_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩሹ")):
        return True
    if bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫሺ") in config and config[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬሻ")] is False:
        return False
    else:
        return True
def bstack11l11l1l_opy_(args_list, bstack11ll1ll1ll_opy_):
    index = -1
    for value in bstack11ll1ll1ll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l1l1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ሼ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧሽ"), exception=exception)
    def bstack1l1111l1l1_opy_(self):
        if self.result != bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨሾ"):
            return None
        if bstackl_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧሿ") in self.exception_type:
            return bstackl_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦቀ")
        return bstackl_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧቁ")
    def bstack11ll1111ll_opy_(self):
        if self.result != bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቂ"):
            return None
        if self.bstack1l1l1l1111_opy_:
            return self.bstack1l1l1l1111_opy_
        return bstack11l1ll1lll_opy_(self.exception)
def bstack11l1ll1lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11lll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l1l11ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111l11ll_opy_(config, logger):
    try:
        import playwright
        bstack11l1ll11ll_opy_ = playwright.__file__
        bstack11ll11ll11_opy_ = os.path.split(bstack11l1ll11ll_opy_)
        bstack11ll1l1l1l_opy_ = bstack11ll11ll11_opy_[0] + bstackl_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩቃ")
        os.environ[bstackl_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪቄ")] = bstack1l1ll1ll11_opy_(config)
        with open(bstack11ll1l1l1l_opy_, bstackl_opy_ (u"ࠨࡴࠪቅ")) as f:
            bstack1ll1ll1ll1_opy_ = f.read()
            bstack11l1ll1l11_opy_ = bstackl_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨቆ")
            bstack11ll11111l_opy_ = bstack1ll1ll1ll1_opy_.find(bstack11l1ll1l11_opy_)
            if bstack11ll11111l_opy_ == -1:
              process = subprocess.Popen(bstackl_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢቇ"), shell=True, cwd=bstack11ll11ll11_opy_[0])
              process.wait()
              bstack11ll1ll11l_opy_ = bstackl_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫቈ")
              bstack11ll1ll111_opy_ = bstackl_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤ቉")
              bstack11l1llll11_opy_ = bstack1ll1ll1ll1_opy_.replace(bstack11ll1ll11l_opy_, bstack11ll1ll111_opy_)
              with open(bstack11ll1l1l1l_opy_, bstackl_opy_ (u"࠭ࡷࠨቊ")) as f:
                f.write(bstack11l1llll11_opy_)
    except Exception as e:
        logger.error(bstack1lll1l1l1l_opy_.format(str(e)))
def bstack11lll11l_opy_():
  try:
    bstack11l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧቋ"))
    bstack11lll1111l_opy_ = []
    if os.path.exists(bstack11l1lll1ll_opy_):
      with open(bstack11l1lll1ll_opy_) as f:
        bstack11lll1111l_opy_ = json.load(f)
      os.remove(bstack11l1lll1ll_opy_)
    return bstack11lll1111l_opy_
  except:
    pass
  return []
def bstack11l1l111l_opy_(bstack1ll1llll1_opy_):
  try:
    bstack11lll1111l_opy_ = []
    bstack11l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨቌ"))
    if os.path.exists(bstack11l1lll1ll_opy_):
      with open(bstack11l1lll1ll_opy_) as f:
        bstack11lll1111l_opy_ = json.load(f)
    bstack11lll1111l_opy_.append(bstack1ll1llll1_opy_)
    with open(bstack11l1lll1ll_opy_, bstackl_opy_ (u"ࠩࡺࠫቍ")) as f:
        json.dump(bstack11lll1111l_opy_, f)
  except:
    pass
def bstack111l111ll_opy_(logger, bstack11ll1lll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstackl_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭቎"), bstackl_opy_ (u"ࠫࠬ቏"))
    if test_name == bstackl_opy_ (u"ࠬ࠭ቐ"):
        test_name = threading.current_thread().__dict__.get(bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬቑ"), bstackl_opy_ (u"ࠧࠨቒ"))
    bstack11ll1lll11_opy_ = bstackl_opy_ (u"ࠨ࠮ࠣࠫቓ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll1lll1l_opy_:
        bstack11l1l1l11_opy_ = os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩቔ"), bstackl_opy_ (u"ࠪ࠴ࠬቕ"))
        bstack1ll1lll111_opy_ = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩቖ"): test_name, bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ቗"): bstack11ll1lll11_opy_, bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬቘ"): bstack11l1l1l11_opy_}
        bstack11l1lll11l_opy_ = []
        bstack11ll111l11_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭቙"))
        if os.path.exists(bstack11ll111l11_opy_):
            with open(bstack11ll111l11_opy_) as f:
                bstack11l1lll11l_opy_ = json.load(f)
        bstack11l1lll11l_opy_.append(bstack1ll1lll111_opy_)
        with open(bstack11ll111l11_opy_, bstackl_opy_ (u"ࠨࡹࠪቚ")) as f:
            json.dump(bstack11l1lll11l_opy_, f)
    else:
        bstack1ll1lll111_opy_ = {bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧቛ"): test_name, bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩቜ"): bstack11ll1lll11_opy_, bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪቝ"): str(multiprocessing.current_process().name)}
        if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ቞") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1lll111_opy_)
  except Exception as e:
      logger.warn(bstackl_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ቟").format(e))
def bstack1l11111l_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll111ll1_opy_ = []
    bstack1ll1lll111_opy_ = {bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬበ"): test_name, bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧቡ"): error_message, bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨቢ"): index}
    bstack11l1ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫባ"))
    if os.path.exists(bstack11l1ll1l1l_opy_):
        with open(bstack11l1ll1l1l_opy_) as f:
            bstack11ll111ll1_opy_ = json.load(f)
    bstack11ll111ll1_opy_.append(bstack1ll1lll111_opy_)
    with open(bstack11l1ll1l1l_opy_, bstackl_opy_ (u"ࠫࡼ࠭ቤ")) as f:
        json.dump(bstack11ll111ll1_opy_, f)
  except Exception as e:
    logger.warn(bstackl_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣብ").format(e))
def bstack1l11l1ll_opy_(bstack1ll11ll1l_opy_, name, logger):
  try:
    bstack1ll1lll111_opy_ = {bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫቦ"): name, bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ቧ"): bstack1ll11ll1l_opy_, bstackl_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧቨ"): str(threading.current_thread()._name)}
    return bstack1ll1lll111_opy_
  except Exception as e:
    logger.warn(bstackl_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨቩ").format(e))
  return
def bstack1111l11l1_opy_(framework):
    if framework.lower() == bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪቪ"):
        return bstack1llll1llll_opy_.version()
    elif framework.lower() == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪቫ"):
        return RobotHandler.version()
    elif framework.lower() == bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬቬ"):
        import behave
        return behave.__version__
    else:
        return bstackl_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧቭ")