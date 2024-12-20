import sys
import datetime
import glob
import zipfile
import gc
import os
import os
import shutil
import datetime
import logging	# we neeed this "logging" library. do not delete this "import" !
from logging import getLogger, getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, ERROR, CRITICAL, FATAL
import time
# coding: UTF-8
if len(sys.argv) > 1: 		# if there is not the 1st args, stop this program ! 
	reminder = sys.argv[1]
else:
	sys.exit()
lastmonth = ''

# LOGDIR='/usr/dfws/etc/Akamai_Programs/1170772/log'
# logdir = '/home/loan01/LOG/AKAMAI_H031S3482'
logdir = 'c:/home/loan01/LOG/AKAMAI_H031S3482'
logkangen_dir = 'logkangen'
slush = '/'

def initialize_global():
	global python_debug_log
	python_debug_log = logdir + slush + logkangen_dir + slush + 'python_debug_log_' + str(nowdatetime) + '.log'

# initiate the logging compornent --- start
logger = getLogger(__name__)
logger.setLevel(DEBUG)
format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
###　logger.setFormatter(format)
sh = StreamHandler()
sh.setLevel(DEBUG)
sh_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(sh_formatter)
logger.addHandler(sh)
what_time_is_it_now = datetime.datetime.now()
### nowdatetime = type(what_time_is_it_now.strftime('%Y%m%d%H%M%S'))
nowdatetime = what_time_is_it_now.strftime('%Y%m%d%H%M%S')
initialize_global()
# global python_debug_log
# python_debug_log = logdir + slush + logkangen_dir + slush + 'python_debug_log_' + str(nowdatetime) + '.log'
fh = FileHandler(python_debug_log)
fh.setLevel(INFO)
fh_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)
# initiate the logging compornent --- end

folderArray = []

weekdir1 = ''
weekdir2 = ''
weekdir3 = ''
weekdir4 = ''

def execute_or_not():

	current_date = datetime.datetime.now()
	weekly_number = current_date.isocalendar()[1]
	this_week_reminder = weekly_number % 4

	write_log_record('INFO', 'this program have the argument: ' + reminder)
	### if unicode(reminder).isnumeric() != True:
	if reminder.isnumeric() != True:
		write_log_record('CRIT', 'the argument is empty. stop this program')
		save_log_file()
		sys.exit()
	### elif unicode(reminder) < 0:
	elif int(reminder) < 0:
		write_log_record('CRIT', 'the argument is less than zero. stop this program')
		save_log_file()
		sys.exit()
	### elif unicode(reminder) > 3:
	elif int(reminder) > 3:
		write_log_record('CRIT', 'the argument is more than three. stop this program')
		save_log_file()
		sys.exit()

	write_log_record('INFO', 'this week reminder: ' + str(this_week_reminder))
	if int(reminder) == int(this_week_reminder):
		write_log_record('INFO', 'match the argument. and start this program')
	else:
		write_log_record('CRIT', 'not match the argument. and stop this program')
		save_log_file()
		sys.exit()

def calc_last_month():
	global lastmonth
	lastmonth = ''
	today = datetime.datetime.today()
	thismonth = datetime.datetime(today.year, today.month, 1)
	lastmonthdate = thismonth + datetime.timedelta(days=-1)
	lastmonth = lastmonthdate.strftime("%Y%m")
	return lastmonth
	
def get_all_folders():
	folder_names = glob.glob(logdir + slush + logkangen_dir + slush + '20*-20*')
	for folder_name in folder_names:
		folderArray.append(folder_name)
		write_log_record('INFO', 'There is a ' + folder_name + ' folder')

	folderArray.sort()	# python array needs .sort()
	write_log_record('INFO', 'display the folders which is sorted asc')
	element_cnt = len(folderArray)
	for folder_name in folderArray:
		write_log_record('INFO', os.path.basename(folder_name))
	

def get_last_4_folders():
	global weekdir1
	global weekdir2
	global weekdir3
	global weekdir4

	element_cnt = len(folderArray)
	weekdir1 = folderArray[element_cnt - 4]
	weekdir2 = folderArray[element_cnt - 3]
	weekdir3 = folderArray[element_cnt - 2]
	weekdir4 = folderArray[element_cnt - 1]

	write_log_record('INFO', '1st folder which isIdentified for : ' + os.path.basename(weekdir1))
	write_log_record('INFO', '2nd folder which isIdentified for : ' + os.path.basename(weekdir2))
	write_log_record('INFO', '3rd folder which isIdentified for : ' + os.path.basename(weekdir3))
	write_log_record('INFO', '4th folder which isIdentified for : ' + os.path.basename(weekdir4))

	gc.collect()	# system.gc();

def concat_4_weeks_files():
	joint4weeksfile = logdir + slush + logkangen_dir + slush + 'joint4weeks.txt'
	joint4weeksfile_lf = logdir + slush + logkangen_dir + slush + 'joint4weeks_lf.txt'
	unzip_c_and_stdout(weekdir1, joint4weeksfile)
	unzip_c_and_stdout(weekdir2, joint4weeksfile)
	unzip_c_and_stdout(weekdir3, joint4weeksfile)
	unzip_c_and_stdout(weekdir4, joint4weeksfile)
	# delete crlf kaigyo
	with open(joint4weeksfile, 'rb') as file: 
		content_lf = file.read().replace(b'\r\n', b'')
		# decode to UTF-8
		content_lf_str = content_lf.decode('utf-8')
		write_log_record('INFO', 'decode utf-8')
	# 
	with open(joint4weeksfile_lf, 'a', encoding='utf-8') as output_file_lf:
		output_file_lf.write(content_lf_str)
		# output_file_lf.close
		write_log_record('INFO', 'write : ' + os.path.basename(joint4weeksfile_lf))

	os.remove(joint4weeksfile)
	write_log_record('INFO', 'remove the chukan file in Japanese: ' + os.path.basename(joint4weeksfile))

def unzip_c_and_stdout(zip_file_path, joint4weeksfile):
	text_file_names = glob.glob(zip_file_path + slush + 'alllog*.txt')
	zip_file_names = glob.glob(zip_file_path + slush + 'alllog*.zip')
	for zip_file_name in zip_file_names:
		try:
			with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
				text_file_names = zip_file.namelist()
				for text_file_name in text_file_names:
					with zip_file.open(text_file_name) as file:
						content = file.read().decode('utf-8')
						with open(joint4weeksfile, 'a', encoding='utf-8') as output_file:
							output_file.write(content)
							# output_file.close
			write_log_record('INFO', 'we can browse this zip file: ' + os.path.basename(zip_file_path))
		except AttributeError as e:
			write_log_record('CRIT', 'we can not browse this file: ' + os.path.basename(zip_file_path))
			write_log_record('CRIT', 'we have to stop this program. because ' + e)
			sys.exit()

def classify_by_folders():

	nowdatetime = get_datetime()
	lastmonth = calc_last_month()

	org_file= logdir + slush + logkangen_dir + slush + 'joint4weeks_lf.txt'
	unexpanded_file = logdir + slush + logkangen_dir + slush + 'unexpanded_lf.txt'
	sort_1st_file = logdir + slush + logkangen_dir + slush + 'sort_1st_lf.txt'
	global result_file
	result_file = logdir + slush + logkangen_dir + slush + 'Akamai_result_crlf_' + lastmonth + '_' + nowdatetime + '.txt'
	
	folderpath = ""
	cnt = 0
	prev_folderpath = ""
	prev_cnt = 0
	work_1st_array = []
	work_2nd_array = []
	sorted_1st_array = []
	sorted_2nd_array = []

	# now, replace one space to one tab space
	with open(org_file, 'r', encoding='utf-8') as org_file_lines:
		unexpanded_content = org_file_lines.read().replace(' ', '\t')
	write_log_record('INFO', 'replace the hankaku space to tab space')
	
	with open(unexpanded_file, 'w', encoding='utf-8') as unexpanded_lines:
		unexpanded_lines.write(unexpanded_content)
	write_log_record('INFO', 'write : ' + os.path.basename(unexpanded_file))

	with open(unexpanded_file, 'r', encoding='utf-8') as unexpanded_file_lines:
		work_lines = unexpanded_file_lines.readlines()
	write_log_record('INFO', 'collect the data in variant')
	
	sorted_lines = sorted(work_lines, key=lambda x: int(x.split('\t')[1]))
	write_log_record('INFO', 'sort the data by folderpath asc')
	
	with open(sort_1st_file, 'w', encoding='utf-8') as sort_1st_lines:
		sort_1st_lines.writelines(sorted_lines)
	write_log_record('INFO', 'write : ' + os.path.basename(sort_1st_file))

	write_log_record('INFO', 'start the kensu summary count by the control break')
	prev_folderpath = ''	# initialized by "ARIENAI" strings
	with open(sort_1st_file, 'r', encoding='utf-8') as sort_1st_line:
		lines = sort_1st_line.readlines()
		for line in lines:
			folderpath, cnt = line.split('\t')
			folderpath = folderpath.split('?')[0]	# remove query string (if exists)
			folderpath = os.path.dirname(folderpath) +	'/'	# remove files string
			if prev_folderpath != folderpath:
				if prev_folderpath == '':
					prev_folderpath = folderpath
					prev_cnt = cnt
				else:
					work_1st_array.append(prev_folderpath + '\t' + str(prev_cnt))
					# ---
					prev_folderpath =''
					prev_cnt = 0
					prev_folderpath = folderpath
					prev_cnt = cnt
			else:
				prev_cnt = int(prev_cnt) + int(cnt)
	write_log_record('INFO', 'finish the kensu summary count by the control break')
	
	sorted_1st_array = sorted(work_1st_array, key=lambda x: x.split('\t')[0])	# sort by folderpath
	write_log_record('INFO', 'sort by folderpath asc')

	write_log_record('INFO', 'start the kensu re-count by the control break')
	prev_folderpath = ''
	prev_cnt = 0
	for sorted_1st_item in sorted_1st_array:
		folderpath, cnt = sorted_1st_item.split('\t')
		if prev_folderpath != folderpath:
			if prev_folderpath == '':
				prev_folderpath = folderpath
				prev_cnt = cnt
			else:
				work_2nd_array.append(prev_folderpath + '\t' + str(prev_cnt) + '\r\n')
				prev_folderpath =''
				prev_cnt = 0
				prev_folderpath = folderpath
				prev_cnt = cnt
		else:
			prev_cnt = int(prev_cnt) + int(cnt)
	write_log_record('INFO', 'finish the kensu re-count by the control break')

	sorted_2nd_array = sorted(work_2nd_array, key=lambda x: int(x.split('\t')[1]), reverse=True)
	write_log_record('INFO', 'sort by kensu count desc')

	with open(result_file, 'w', encoding='utf-8') as result_line:
		for sorted_2nd_item in sorted_2nd_array:
			result_line.write(sorted_2nd_item.rstrip() + '\n')
	write_log_record('INFO', 'write : ' + os.path.basename(result_file))

	os.remove(org_file)
	os.remove(unexpanded_file)
	os.remove(sort_1st_file)
	write_log_record('INFO', 'remove 3 chukan files : ' + os.path.basename(org_file) + ', ' + os.path.basename(unexpanded_file) + ', ' + os.path.basename(sort_1st_file))

	gc.collect()

def save_result_file():

	lastmonth = calc_last_month()

	lastmonth_folder_name = 'TOP250-' + lastmonth
	generate_lastmonth_folder = logdir + slush + logkangen_dir + slush + lastmonth_folder_name
	
	### result_file_pattern = 'Akamai_result_*.txt'
	### result_file = glob.glob(os.path.join(logdir, slush, logkangen_dir, slush, result_file_pattern))

	if os.path.isdir(generate_lastmonth_folder) == False:
		os.makedirs(generate_lastmonth_folder)
		write_log_record('INFO', 'generate a new folder: ' + generate_lastmonth_folder)
	else:
		write_log_record('WARN', 'the folder already exists : ' + generate_lastmonth_folder)
	
	shutil.move(result_file, generate_lastmonth_folder)
	write_log_record('INFO', 'move the result file: ' + os.path.basename(generate_lastmonth_folder))

def generate_top_250_file():

	nowdatetime = get_datetime()

	lastmonth = calc_last_month()
	lastmonth_folder_name = 'TOP250-' + lastmonth
	lastmonth_folder_path = logdir + slush + logkangen_dir + slush + lastmonth_folder_name
	top_250_result_file = lastmonth_folder_path + slush + 'Akamai_result_top_250_' + lastmonth + '_' + nowdatetime + '.txt'
	result_file_name_only = os.path.basename(result_file)
	now_result_file = lastmonth_folder_path + slush +result_file_name_only

	with open(now_result_file, 'r', encoding='utf-8') as infile:
		lines = [next(infile) for _ in range(250)]
	write_log_record('INFO', 'collect top 250 record from the result file to a variant') 
	
	with open(top_250_result_file, 'w', encoding='utf-8') as outfile:
		outfile.writelines(lines)
	write_log_record('INFO', 'generate the top 250 record file: ' + os.path.basename(top_250_result_file))

def save_log_file():

	time.sleep(0.5)
	logger.removeHandler(fh)	# remove logging file handler
	fh.close()					# close logging file handler

	lastmonth = calc_last_month()

	lastmonth_folder_name = 'TOP250-' + lastmonth
	generate_lastmonth_folder = logdir + slush + logkangen_dir + slush + lastmonth_folder_name
	lastmonth_folder_path = logdir + slush + logkangen_dir + slush + lastmonth_folder_name

	if os.path.isdir(generate_lastmonth_folder) == False:
		os.makedirs(generate_lastmonth_folder)
	
	shutil.move(python_debug_log, lastmonth_folder_path)

def write_log_record(loglevel, eventmessage): 

	if loglevel == 'DEBUG': 
		logger.debug(eventmessage)
	elif loglevel == 'INFO':
		logger.info(eventmessage) 
	elif loglevel == 'WARN':
		logger.warning(eventmessage) 
	elif loglevel == 'ERR': 
		logger.error(eventmessage) 
	elif loglevel == 'CRIT':
		logger.critical(eventmessage)
	else:
		logger.info(loglevel + '? unknown loglevel !')

def get_datetime():

	what_time_is_it_now = datetime.datetime.now()
	### nowdatetime = type(what_time_is_it_now.strftime('%Y%m%d%H%M%S'))		# to use the file name to be identified 
	nowdatetime = what_time_is_it_now.strftime('%Y%m%d%H%M%S')
	return nowdatetime

if __name__ == '__main__':

	# Author: COBOL PROGRAMMER
 	# Date: 2024-12-20
 	# Description: This Python 3 program was written in the COBOL language. Hurrah, COBOL !

	write_log_record('INFO', 'welcome to the bugbug program !') 

	execute_or_not()	# check the weekly number. if this week have the corecct weekly number, start this program 
	# lsatmonth = calc_last_month()
	get_all_folders()
	get_last_4_folders()
	concat_4_weeks_files()
	classify_by_folders()
	save_result_file()
	generate_top_250_file()

	write_log_record('INFO', 'good luck, have a nice day !') 
	save_log_file()

	gc.collect()

	exit()
