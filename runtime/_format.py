from typing import Optional

class _ImageTAG:
    def __init__(self, 
                 img_rel_path:str, 
                 img_abs_path:str,
                 tag_string:Optional[str] = None) -> None:
        
        self.relaive_path = img_rel_path
        self.absolute_path = img_abs_path
        self.tag_string = tag_string

class _HyperlinkTAG:
    def __init__(self,
                 url:str,
                 tag_string:Optional[str] = None) -> None:
        self.url = url

    