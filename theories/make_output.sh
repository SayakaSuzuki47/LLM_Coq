#!/bin/bash
data_dir_path=#Coqtopで実行した後の出力群を保存したフォルダ先を指定する．
input_dir_path="${data_dir_path}input/"
v_dir_path="${data_dir_path}coqtop_data/"
output_dir_path="${data_dir_path}response/line/"

#responseの作成(次の行)
#別で作成したディレクトリ一覧を取得する
files=($(find $input_dir_path -name "*.txt"))

for file in ${files[@]}
do
	read_file="${file/$input_dir_path}"
	read_file_name=$(basename "$read_file")
	dir_name="${read_file/$read_file_name}"
	output_dir="${output_dir_path}${dir_name}"
	mkdir -p $output_dir
	read_file=${read_file%.*}
	IFS="_" read -ra elements <<< "$read_file"
	last_index=$((${#elements[@]} - 1 ))
	last_element=${elements[$last_index]}
	last_element=$((last_element + 1 ))
	elements[$last_index]=$last_element
	v_read_file=$(IFS="_"; echo "${elements[*]}")
	v_file_path="${v_dir_path}${v_read_file}.v"
	output_file_path="${output_dir_path}${read_file}.txt"
	tail -n 1 $v_file_path > $output_file_path
done