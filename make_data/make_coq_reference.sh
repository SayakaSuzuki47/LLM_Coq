#データに使用するCoqファイルの場所
input_dir="../data/test_coq_source"
#Coqtopを実行した後の出力を入れるディレクトリをそれぞれ指定する(ディレクトリは空にする)．
output_dir="../data/test_coq_lv"
output_dir_l="../data/test_coq_l"

#input_dirからCoqファイル一覧を作成する．
files=($(find $input_dir -name "*.v"))

# 各ファイルに対して処理を繰り返す
for file in ${files[@]}; 
do
    #実行結果をinput_dirと同じ構造にするためのフォルダ名取得
	read_file="${file/$input_dir}"
	read_file_name=$(basename "$read_file")
	dir_name="${read_file/$read_file_name}"
    # ファイル名から拡張子を取り除いて.txtを追加する
    file_name=${file/$input_dir}
    output_file_name="${file_name%.*}.txt"
    #実際の出力ファイル名
    output_file=$output_dir${output_file_name}
    output_file_l=$output_dir_l${output_file_name}
    # 出力ファイルのパスを指定してCoqtopを実行し、結果をファイルに保存する
    coqtop -batch -lv $file 1>$output_file & 
    coqtop -batch -l $file 1>$output_file_l & 
done
