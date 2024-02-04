#!/bin/bash
#実行したいファイル名
file=$1
data_dir_path=$2

read_file="${file%.*}"
read_file_name=$(basename "$read_file")

#vファイルが入っているフォルダを指定する．
input_file_path="${data_dir_path}theories${file}"
#vファイルのn行目まで実行した後の返答ファイルを保存する場所を指定する．
output_dir_path_coq="${data_dir_path}coqtop_data${read_file}/"
#vファイルのn行目までとShow.実行した後の返答ファイルを保存する場所を指定する．
output_dir_path_coq_show="${data_dir_path}coqtop_data_show${read_file}/"

#元のvファイルが入っているフォルダと同じ構造にする．
#そのためにフォルダがなければ作成する．
mkdir -p $output_dir_path_coq
mkdir -p $output_dir_path_coq_show

line_num=1
while read line
do
    file_line_name="${output_dir_path_coq}${read_file_name}_${line_num}"
    file_line_show_name="${output_dir_path_coq_show}${read_file_name}_show_${line_num}"
    vline_file="${file_line_name}.v"
    vline_file_show="${file_line_show_name}.v"

    #n行ごとのvファイルを作る
    cat  $input_file_path | awk "NR<=$line_num {print}" | tee  $vline_file | tee $vline_file_show
    #n行ごとのvファイルにShow.を付けたファイルを作る．
    echo "Show." >> "$vline_file_show"

    output_coqtop_file="${vline_file%.*}.txt"
    output_coqtop_show="${vline_file_show%.*}.txt"

    # 出力ファイルのパスを指定してCoqtopを実行し、結果をファイルに保存する
    cat "$vline_file" | coqtop | tee "$output_coqtop_file"
    cat "$vline_file_show" | coqtop | tee "$output_coqtop_show"

    line_num=$((++line_num))
done < $input_file_path
\end{Bash}

\begin{Bash}{}{vファイルを一度にcoqtop-emacsで実行する}
#!/bin/bash
data_dir_path=#input data_dir_path
output_dir_path=#input output_dir_path
#ファイル一覧の取得
input_dir_path="${data_dir_path}"
#vファイルのみ取得
files=($(find ${input_dir_path} -name "*.v"))

for file in ${files[@]}
do
	#echo $file
	#元のフォルダと同じ構造にするためのフォルダ作り
	read_file="${file/$input_dir_path}"
	read_file_name=$(basename "$read_file" .v)
	dir_name="${read_file/$read_file_name.v}"
	output_dir="${output_dir_path}${dir_name}"
	mkdir -p $output_dir

	output_file_path="${output_dir}${read_file_name}"
	output_name="${output_file_path}.txt"
    #Coqtop emacsで実行
	cat "$file" | coqtop -emacs | tee "$output_name" 
done