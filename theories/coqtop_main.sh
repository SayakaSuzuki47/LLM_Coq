#!/bin/bash

# dataのファイル
data_dir_path= #dataのあるフォルダのパス

#vファイルの一覧取得
input_dir_path="${data_dir_path}theories"
files=($(find $input_dir_path -name "*.v"))

#実行するソースファイル
sh_file="coqtop_v_line.sh" 

# リストの要素を順番に処理するループ
result_path= #拡張子がtxtのファイルがあるフォルダ一覧のテキストファイルのパス

for file in ${files[@]}
do
	file="${file/$input_dir_path}"
    # ファイルを実行
    source "$sh_file" "$file" "$data_dir_path"
done