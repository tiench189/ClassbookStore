enableVadb = 'true' 

def checkEnableVadb():
    print 'ok'
    return dict(items=enableVadb)

def source_file():
    """

    @return: source file to pull
    """
    source_file_pull = "/sdcard/TVB/clsBook.sqlite"
    return dict(source=source_file_pull)