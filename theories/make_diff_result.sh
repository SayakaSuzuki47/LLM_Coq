#!/bin/bash
data_dir_path=#input dir path
output_dir_path="${data_dir_path}input/"
#ファイル一覧の取得
input_dir_path="${data_dir_path}coqtop_data/"
input_dir_show="${data_dir_path}coqtop_data_show/"
files=($(find $input_dir_show -name "*.txt"))

for file_show in ${files[@]}
do
	#echo $file_show
	#フォルダ作り
	read_file="${file_show/$input_dir_show}"
	read_file_name=$(basename "$read_file")
	dir_name="${read_file/$read_file_name}"
	output_dir="${output_dir_path}${dir_name}"
	mkdir -p $output_dir

	#元とshowでのtxt差分作り
	file_origin="${input_dir_path}${dir_name}${read_file_name/_show}"
	output_file_path="${output_dir}${read_file_name/_show}"
	diff_result=$(diff "$file_origin" "$file_show")  
	if [[ -n "$diff_result" ]]; then
		echo "$diff_result" > "$output_file_path"
	fi 
done