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
from uuid import uuid4
from bstack_utils.helper import bstack111l11lll_opy_, bstack11ll11l11l_opy_
from bstack_utils.bstack11ll11l1_opy_ import bstack111l1llll1_opy_
class bstack1l11l1l1l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l11llllll_opy_=None, framework=None, tags=[], scope=[], bstack1111lllll1_opy_=None, bstack1111ll1111_opy_=True, bstack1111l1llll_opy_=None, bstack111l111l1_opy_=None, result=None, duration=None, bstack1l11l1ll11_opy_=None, meta={}):
        self.bstack1l11l1ll11_opy_ = bstack1l11l1ll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111ll1111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l11llllll_opy_ = bstack1l11llllll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
        self.bstack111l111l1_opy_ = bstack111l111l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11ll1ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111ll11l1_opy_(self):
        bstack1111lll11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭Ꮑ"): bstack1111lll11l_opy_,
            bstackl_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭Ꮒ"): bstack1111lll11l_opy_,
            bstackl_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᏃ"): bstack1111lll11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstackl_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᏄ") + key)
            setattr(self, key, val)
    def bstack1111lll1l1_opy_(self):
        return {
            bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏅ"): self.name,
            bstackl_opy_ (u"ࠨࡤࡲࡨࡾ࠭Ꮖ"): {
                bstackl_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᏇ"): bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᏈ"),
                bstackl_opy_ (u"ࠫࡨࡵࡤࡦࠩᏉ"): self.code
            },
            bstackl_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᏊ"): self.scope,
            bstackl_opy_ (u"࠭ࡴࡢࡩࡶࠫᏋ"): self.tags,
            bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᏌ"): self.framework,
            bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᏍ"): self.bstack1l11llllll_opy_
        }
    def bstack1111lll111_opy_(self):
        return {
         bstackl_opy_ (u"ࠩࡰࡩࡹࡧࠧᏎ"): self.meta
        }
    def bstack1111ll1l1l_opy_(self):
        return {
            bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭Ꮟ"): {
                bstackl_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᏐ"): self.bstack1111lllll1_opy_
            }
        }
    def bstack1111ll1l11_opy_(self, bstack1111lll1ll_opy_, details):
        step = next(filter(lambda st: st[bstackl_opy_ (u"ࠬ࡯ࡤࠨᏑ")] == bstack1111lll1ll_opy_, self.meta[bstackl_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏒ")]), None)
        step.update(details)
    def bstack1111ll1ll1_opy_(self, bstack1111lll1ll_opy_):
        step = next(filter(lambda st: st[bstackl_opy_ (u"ࠧࡪࡦࠪᏓ")] == bstack1111lll1ll_opy_, self.meta[bstackl_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᏔ")]), None)
        step.update({
            bstackl_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ꮥ"): bstack111l11lll_opy_()
        })
    def bstack1l11lll111_opy_(self, bstack1111lll1ll_opy_, result, duration=None):
        bstack1111l1llll_opy_ = bstack111l11lll_opy_()
        if bstack1111lll1ll_opy_ is not None and self.meta.get(bstackl_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏖ")):
            step = next(filter(lambda st: st[bstackl_opy_ (u"ࠫ࡮ࡪࠧᏗ")] == bstack1111lll1ll_opy_, self.meta[bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏘ")]), None)
            step.update({
                bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᏙ"): bstack1111l1llll_opy_,
                bstackl_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᏚ"): duration if duration else bstack11ll11l11l_opy_(step[bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᏛ")], bstack1111l1llll_opy_),
                bstackl_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᏜ"): result.result,
                bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᏝ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111ll1lll_opy_):
        if self.meta.get(bstackl_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᏞ")):
            self.meta[bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏟ")].append(bstack1111ll1lll_opy_)
        else:
            self.meta[bstackl_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏠ")] = [ bstack1111ll1lll_opy_ ]
    def bstack1111llll1l_opy_(self):
        return {
            bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᏡ"): self.bstack1l11ll1ll1_opy_(),
            **self.bstack1111lll1l1_opy_(),
            **self.bstack1111ll11l1_opy_(),
            **self.bstack1111lll111_opy_()
        }
    def bstack1111ll11ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ꮲ"): self.bstack1111l1llll_opy_,
            bstackl_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᏣ"): self.duration,
            bstackl_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᏤ"): self.result.result
        }
        if data[bstackl_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᏥ")] == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏦ"):
            data[bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᏧ")] = self.result.bstack1l1111l1l1_opy_()
            data[bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᏨ")] = [{bstackl_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᏩ"): self.result.bstack11ll1111ll_opy_()}]
        return data
    def bstack1111l1ll1l_opy_(self):
        return {
            bstackl_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏪ"): self.bstack1l11ll1ll1_opy_(),
            **self.bstack1111lll1l1_opy_(),
            **self.bstack1111ll11l1_opy_(),
            **self.bstack1111ll11ll_opy_(),
            **self.bstack1111lll111_opy_()
        }
    def bstack1l1l1l1l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstackl_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᏫ") in event:
            return self.bstack1111llll1l_opy_()
        elif bstackl_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ꮼ") in event:
            return self.bstack1111l1ll1l_opy_()
    def bstack1l11l11ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1111l1llll_opy_ = time if time else bstack111l11lll_opy_()
        self.duration = duration if duration else bstack11ll11l11l_opy_(self.bstack1l11llllll_opy_, self.bstack1111l1llll_opy_)
        if result:
            self.result = result
class bstack1l11l1lll1_opy_(bstack1l11l1l1l1_opy_):
    def __init__(self, hooks=[], bstack1l1l111lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l1l111lll_opy_ = bstack1l1l111lll_opy_
        super().__init__(*args, **kwargs, bstack111l111l1_opy_=bstackl_opy_ (u"ࠬࡺࡥࡴࡶࠪᏭ"))
    @classmethod
    def bstack1111l1lll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstackl_opy_ (u"࠭ࡩࡥࠩᏮ"): id(step),
                bstackl_opy_ (u"ࠧࡵࡧࡻࡸࠬᏯ"): step.name,
                bstackl_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᏰ"): step.keyword,
            })
        return bstack1l11l1lll1_opy_(
            **kwargs,
            meta={
                bstackl_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᏱ"): {
                    bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨᏲ"): feature.name,
                    bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩᏳ"): feature.filename,
                    bstackl_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᏴ"): feature.description
                },
                bstackl_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᏵ"): {
                    bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᏶"): scenario.name
                },
                bstackl_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᏷"): steps,
                bstackl_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᏸ"): bstack111l1llll1_opy_(test)
            }
        )
    def bstack1111llll11_opy_(self):
        return {
            bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᏹ"): self.hooks
        }
    def bstack1111llllll_opy_(self):
        if self.bstack1l1l111lll_opy_:
            return {
                bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᏺ"): self.bstack1l1l111lll_opy_
            }
        return {}
    def bstack1111l1ll1l_opy_(self):
        return {
            **super().bstack1111l1ll1l_opy_(),
            **self.bstack1111llll11_opy_()
        }
    def bstack1111llll1l_opy_(self):
        return {
            **super().bstack1111llll1l_opy_(),
            **self.bstack1111llllll_opy_()
        }
    def bstack1l11l11ll1_opy_(self):
        return bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᏻ")
class bstack1l11ll111l_opy_(bstack1l11l1l1l1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack111l111l1_opy_=bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᏼ"))
    def bstack1l1l11ll11_opy_(self):
        return self.hook_type
    def bstack1111ll111l_opy_(self):
        return {
            bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᏽ"): self.hook_type
        }
    def bstack1111l1ll1l_opy_(self):
        return {
            **super().bstack1111l1ll1l_opy_(),
            **self.bstack1111ll111l_opy_()
        }
    def bstack1111llll1l_opy_(self):
        return {
            **super().bstack1111llll1l_opy_(),
            **self.bstack1111ll111l_opy_()
        }
    def bstack1l11l11ll1_opy_(self):
        return bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ᏾")