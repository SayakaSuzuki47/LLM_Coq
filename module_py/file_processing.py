import os

#フォルダ内の特定の拡張子のパスの一覧を取得する
#末端のファイルまで探す
#input_pathは目的のフォルダへのパス
#extは拡張子を指定する．
def read_file_path_list(input_path, ext):
  result=[]
  for dir,dirs,files in os.walk(input_path):
    file_lst=[os.path.relpath(os.path.join(dir, file), input_path) for file in files if file.endswith(ext)]
    result=result+file_lst
  return(result)