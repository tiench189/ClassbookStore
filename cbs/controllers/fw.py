@request.restful()
def version():
    response.view = 'generic.json'
    def POST(*args, **vars):
        try:
            if len(args) != 1:
                raise Exception()
            if args[0] == "CB":
                fw_file = osFileServer.listdir('/fw', 'cb.*.dat', files_only = True)
            elif args[0] == "CBT":
                fw_file = osFileServer.listdir('/fw', 'cbt.*.dat', files_only = True)
            else:
                raise Exception()
            if len(fw_file) == 0:
                raise Exception()
            else:
                fw_file = fw_file[0].split('.')[1]
            return dict(fw=fw_file)
        except Exception as ex:
            return dict(error="Parameters is not valid!")
    return locals()


@request.restful()
def download():
    response.view = 'generic.json'
    def POST(*args, **vars):
        try:
            if len(args) != 1:
                raise Exception()
            if args[0] == "CB":
                fw_file = osFileServer.listdir('/fw', 'cb.*.dat', True, files_only = True)
            elif args[0] == "CBT":
                fw_file = osFileServer.listdir('/fw', 'cbt.*.dat', True, files_only = True)
            else:
                raise Exception()
            if len(fw_file) == 0:
                raise Exception()
            response.headers['Content-Disposition'] = "attachment; filename=fw.dat"
            return response.stream(osFileServer.open(path = fw_file[0], mode = 'rb'))
        except Exception as ex:
            return dict(error="Parameters is not valid!")
    return locals()