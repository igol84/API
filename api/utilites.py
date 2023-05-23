import ftplib


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


def save_file(directory: str, file: bytes, file_name: str):
    ftp = ftplib.FTP('ftp.sweetshoes.com.ua', 'pictures@sweetshoes.com.ua', '[cf^SMFN%%x]')
    chdir(directory, ftp)
    ftp.storbinary('STOR ' + file_name, file)
    ftp.quit()