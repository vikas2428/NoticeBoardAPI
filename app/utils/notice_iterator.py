class NoticeIterator:
    """
    Custom iterator for traversing notices one at a time.
    """

    def __init__(self, notices):
        self.notices = notices
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.notices):
            raise StopIteration

        notice = self.notices[self.index]
        self.index += 1

        return notice


def notice_generator(notices):
    """
    Generator that yields notices one at a time.
    """

    for notice in notices:
        yield notice