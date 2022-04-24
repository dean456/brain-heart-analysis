python main.py -e -i testData\eeg\s01_ex01_s01.csv -s 125 -o eeg_result_single_file
python main.py -e -i testData\eeg -s 200 -o eeg_result_multiple_files
python main.py -c -w testData\ekg_wfdb\100 -s 360 -o ekg_result_single_file
python main.py -c -i testData\ekg_csv\sub01_220217_pre_0100.TXT -s 125 -b -n ID,L1,L2,L3,L4,L5 -o ekg_result_single_file -t
python main.py -c -i testData\ekg_csv -s 125 -b -n ID,L1,L2,L3,L4,L5 -o ekg_result_multiple_files
pause
