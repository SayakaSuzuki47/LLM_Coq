#!bin/bash
data_dir_path=#input dirname
output_path="${data_dir_path}dir_name.txt"
#ファイル一覧の取得
data_input_dir_path="${data_dir_path}input/"
files=($(find $data_input_dir_path -name "*.txt"))

for file in ${files[@]}
do
	file_name=$(basename $file)
	dir="${file/$file_name}"
	dir_name="${dir/$data_input_dir_path}"
	echo "$dir_name" >>"$output_path"
done
sort -u $output_path > "${data_dir_path}dir_names.txt"