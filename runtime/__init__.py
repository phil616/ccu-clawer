from ._shared_dict import _SharedDict
from ._task_queue import put_task, get_task
from ._format import _ImageTAG as ImageTAG
from ._format import _HyperlinkTAG as HyperlinkTAG

safe_dict = _SharedDict()