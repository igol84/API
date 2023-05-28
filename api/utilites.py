from fastapi import UploadFile



def chdir(directory, ftp):
    if directory_exists(directory, ftp) is False:  # (or negate, whatever you prefer for readability)
        ftp.mkd(directory)
    ftp.cwd(directory)


# Check if directory exists (in current location)
def directory_exists(directory, ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == directory and f.upper().startswith('D'):
            return True
    return False


def file_exists(file_name, ftp):
    filelist = []
    ftp.retrlines('NLST', filelist.append)
    for file in filelist:
        print(file)
        if file == file_name:
            return True
    return False


def save_file(directory: str, file: bytes, file_name: str, ftp):
    chdir(directory, ftp)
    ftp.storbinary('STOR ' + file_name, file)


def save_files(directory: str, files: list[UploadFile], ftp):
    chdir(directory, ftp)
    for file in files:
        ftp.storbinary('STOR ' + file.filename, file.file)


def del_dir(directory: str, ftp):
    if directory_exists(directory, ftp):
        names = ftp.nlst(directory)
        for name in names:
            ftp.delete(name)
        ftp.rmd(directory)
