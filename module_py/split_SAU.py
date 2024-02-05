import re

#split for ##System and ##User and ##Assistant
def split_for_SAU(file_path):
    with open(file_path) as f:
        pattern = re.compile(r"##System\n|##User\n|##Assistant\n")
        SAU_lst=re.split(pattern,f.read())
        SAU_dct={"##System":[SAU_lst[1]],"##User":SAU_lst[2::2],"##Assistant":SAU_lst[3::2]}
    return SAU_dct