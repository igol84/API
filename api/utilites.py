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
        ftp.storbinary('STOR ' + check_file_name_and_get_new_name(file.filename), file.file)


def del_dir(directory: str, ftp):
    if directory_exists(directory, ftp):
        names = ftp.nlst(directory)
        for name in names:
            ftp.delete(name)
        ftp.rmd(directory)


def translit(word: str) -> str:
    ru = "А-а-Б-б-В-в-Ґ-ґ-Г-г-Д-д-Е-е-Ё-ё-Є-є-Ж-ж-З-з-И-и-І-і-Ї-ї-Й-й-К-к-Л-л-М-м-Н-н-О-о-П-п-Р-р-С-с-Т-т-У-у-Ф-ф-Х" \
         "-х-Ц-ц-Ч-ч-Ш-ш-Щ-щ-Ъ-ъ-Ы-ы-Ь-ь-Э-э-Ю-ю-Я-я".split('-')
    en = "A-a-B-b-V-v-G-g-G-g-D-d-E-e-E-e-E-e-ZH-zh-Z-z-I-i-I-i-I-i-J-j-K-k-L-l-M-m-N-n-O-o-P-p-R-r-S-s-T-t-U-u-F-" \
         "f-H-h-TS-ts-CH-ch-SH-sh-SCH-sch-'-'-Y-y-'-'-E-e-YU-yu-YA-ya".split('-')
    result: str = ''
    for letter in word:
        if letter in ru:
            index = ru.index(letter)
            result += en[index]
        else:
            result += letter
    return result


def create_url(value: str) -> str:
    return translit(value.replace(' ', '-')).lower()


def check_file_name_and_get_new_name(value):
    names = {
        'main.jpg': '02.jpg', 'main_b.jpg': '03.jpg', 'main_s.jpg': '01.jpg',
        'bottom.jpg': '12.jpg', 'bottom_b.jpg': '13.jpg', 'bottom_s.jpg': '11.jpg',
        'front.jpg': '22.jpg', 'front_b.jpg': '23.jpg', 'front_s.jpg': '21.jpg',
        'back.jpg': '32.jpg', 'back_b.jpg': '33.jpg', 'back_s.jpg': '31.jpg',
        'smal.jpg': '4.jpg', 'my.jpg': '5.jpg'
    }
    for name in names:
        if value.endswith(name):
            return names[name]
    return value


if __name__ == '__main__':
    print(create_url('теКст топ'))
