
class DamonFsOps:
    def read(self):
        pass

    def write(self):
        pass
class DamonCtx:
    idx = None
    kdamond = None

    def stage(self):
        pass

    def read(self):
        pass

class Kdamond:
    def set_fs(self, fs):
        self.fs = fs

    def stage(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def commit(self):
        pass
    def commit_schemes_quota_goals(self):
        pass
    def update_schemes_stats(self):
        pass
    def update_schemes_tried_regions(self):
        pass
    def update_schemes_tried_bytes(self):
        pass
    def clear_schemmes_tried_regions(self):
        pass

class Kdamonds:
    kdamonds = None

    def __init__(self, kdamonds):
        self.kdamonds = kdamonds
        for idx, kdamond in enumerate(self.kdamonds):
            kdamond.idx = idx
            kdamond.kdamonds = self

    def from_debugfs(self):
        pass

    def from_sysfs(self):
        pass
