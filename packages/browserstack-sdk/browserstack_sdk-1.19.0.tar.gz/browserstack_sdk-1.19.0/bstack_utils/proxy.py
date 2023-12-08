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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l11lll1l_opy_
def bstack111ll111l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111ll1l111_opy_(bstack111ll11lll_opy_, bstack111ll111ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111ll11lll_opy_):
        with open(bstack111ll11lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111ll111l1_opy_(bstack111ll11lll_opy_):
        pac = get_pac(url=bstack111ll11lll_opy_)
    else:
        raise Exception(bstackl_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪጵ").format(bstack111ll11lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstackl_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧጶ"), 80))
        bstack111ll11ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111ll11ll1_opy_ = bstackl_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ጷ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111ll111ll_opy_, bstack111ll11ll1_opy_)
    return proxy_url
def bstack1lllll11l1_opy_(config):
    return bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩጸ") in config or bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫጹ") in config
def bstack1l1ll1ll11_opy_(config):
    if not bstack1lllll11l1_opy_(config):
        return
    if config.get(bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫጺ")):
        return config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬጻ"))
    if config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧጼ")):
        return config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨጽ"))
def bstack1ll1l1l1l_opy_(config, bstack111ll111ll_opy_):
    proxy = bstack1l1ll1ll11_opy_(config)
    proxies = {}
    if config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨጾ")) or config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪጿ")):
        if proxy.endswith(bstackl_opy_ (u"ࠧ࠯ࡲࡤࡧࠬፀ")):
            proxies = bstack1llll1111l_opy_(proxy, bstack111ll111ll_opy_)
        else:
            proxies = {
                bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧፁ"): proxy
            }
    return proxies
def bstack1llll1111l_opy_(bstack111ll11lll_opy_, bstack111ll111ll_opy_):
    proxies = {}
    global bstack111ll11l1l_opy_
    if bstackl_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬፂ") in globals():
        return bstack111ll11l1l_opy_
    try:
        proxy = bstack111ll1l111_opy_(bstack111ll11lll_opy_, bstack111ll111ll_opy_)
        if bstackl_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥፃ") in proxy:
            proxies = {}
        elif bstackl_opy_ (u"ࠦࡍ࡚ࡔࡑࠤፄ") in proxy or bstackl_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦፅ") in proxy or bstackl_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧፆ") in proxy:
            bstack111ll11l11_opy_ = proxy.split(bstackl_opy_ (u"ࠢࠡࠤፇ"))
            if bstackl_opy_ (u"ࠣ࠼࠲࠳ࠧፈ") in bstackl_opy_ (u"ࠤࠥፉ").join(bstack111ll11l11_opy_[1:]):
                proxies = {
                    bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩፊ"): bstackl_opy_ (u"ࠦࠧፋ").join(bstack111ll11l11_opy_[1:])
                }
            else:
                proxies = {
                    bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫፌ"): str(bstack111ll11l11_opy_[0]).lower() + bstackl_opy_ (u"ࠨ࠺࠰࠱ࠥፍ") + bstackl_opy_ (u"ࠢࠣፎ").join(bstack111ll11l11_opy_[1:])
                }
        elif bstackl_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢፏ") in proxy:
            bstack111ll11l11_opy_ = proxy.split(bstackl_opy_ (u"ࠤࠣࠦፐ"))
            if bstackl_opy_ (u"ࠥ࠾࠴࠵ࠢፑ") in bstackl_opy_ (u"ࠦࠧፒ").join(bstack111ll11l11_opy_[1:]):
                proxies = {
                    bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫፓ"): bstackl_opy_ (u"ࠨࠢፔ").join(bstack111ll11l11_opy_[1:])
                }
            else:
                proxies = {
                    bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ፕ"): bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤፖ") + bstackl_opy_ (u"ࠤࠥፗ").join(bstack111ll11l11_opy_[1:])
                }
        else:
            proxies = {
                bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩፘ"): proxy
            }
    except Exception as e:
        print(bstackl_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣፙ"), bstack11l11lll1l_opy_.format(bstack111ll11lll_opy_, str(e)))
    bstack111ll11l1l_opy_ = proxies
    return proxies