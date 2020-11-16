from .site import SiteChapter


class WebChapter(SiteChapter):
    """Chapter object to capture special behavior of Electronic Dig chapter."""

    def __init__(self, name, parent, path):
        super().__init__(name=name, parent=parent, path=path)
        self.href = path.as_posix().replace(
            'https:/', 'https://').replace('http:/', 'http://')

    def update_href(self, start_path):
        """Dummy function, self.href doesn't change."""
        return
