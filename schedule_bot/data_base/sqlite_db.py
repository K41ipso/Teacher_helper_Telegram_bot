import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
	global base, cur
	base = sq.connect('schedule.db')
	cur = base.cursor()
	if base:
		print('Data base reg is connected.')
	base.execute('CREATE TABLE IF NOT EXISTS stud(user_id TEXT, name TEXT, clock TEXT, callendar TEXT, status_sum TEXT)')
	base.commit()



#registration 

#проверка регистрации
def sql_prov_reg(data):
	r = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	if bool(r) is False:
		return ''
	else:
		return str(r)

async def sql_add_name(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()

async def sql_delite_name(data):
	cur.execute('DELETE FROM stud WHERE user_id ==? AND clock ==?', (data, 'REG',))
	base.commit()



#проверка на админа
def sql_adm_check(data):
	r = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ? AND status_sum == ?', (data, 'REG', 'ADMIN',)).fetchone()
	if bool(r) is False:
		return 0
	else:
		return 1



#изменить админ статус
async def sql_chenge_stat_adm(data):
	cur.execute('UPDATE stud SET status_sum == ? WHERE user_id == ? AND clock == ?', ('ADMIN', data, 'REG',))
	base.commit()

async def sql_chenge_stat_user(data):
	cur.execute('UPDATE stud SET status_sum == ? WHERE user_id == ? AND clock == ?', ('USER', data, 'REG',))
	base.commit()



#pictures
async def sql_add_pic(state):
	r = cur.execute('SELECT status_sum FROM stud WHERE clock == ?', ('01A',)).fetchone()
	if bool(r) is False:
		async with state.proxy() as data:
			cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
			base.commit()
	else:
		cur.execute('DELETE FROM stud WHERE clock == ?', ('01A',))
		base.commit()
		async with state.proxy() as data:
			cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
			base.commit()


def sql_start_pic():
	r = cur.execute('SELECT status_sum FROM stud WHERE clock == ?', ('01A',)).fetchone()
	return r


#новый урок
async def sql_add_lesson(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()


#вывести время
async def sql_time(data):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	return r

async def sql_timer(data, time):
	r = cur.execute('SELECT callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',))
		base.commit()
	cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', (data, '_', time, time, 'boofer',))
	base.commit()

async def bezop_dob_les(data):
	r = cur.execute('SELECT callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',))
		base.commit()

#добавка в буфер времени (часа)
async def sql_hour_timer(data, hour):
	cur.execute('UPDATE stud SET clock == ? WHERE user_id == ? AND status_sum == ?', (hour, data, 'boofer',))
	base.commit()

#(минуты)
async def sql_min_timer(data, minutes):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	cur.execute('UPDATE stud SET clock == ? WHERE user_id == ? AND status_sum == ?', (f'{str(r)[2:4]}{minutes}', data, 'boofer',))
	base.commit()

def sql_timer_insert(data):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	return r

async def sql_got_les(data):
	cur.execute('UPDATE stud SET status_sum == ? WHERE user_id == ? AND status_sum == ?', ('🔴', data, 'boofer',))
	base.commit()

async def sql_got_les_admin(data):
	idu = cur.execute('SELECT name FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',)).fetchone()
	cur.execute('UPDATE stud SET user_id == ?, status_sum == ? WHERE user_id == ? AND status_sum == ?', (str(idu)[2:-3], '🔴', data, 'boofer',))
	base.commit()

#хуй!

#занято?
def sql_zanyato_time(data):
	x = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	minutes = int(str(x[0])[-2:])
	hour = int(str(x[0])[:-3])
	if minutes > 0:
		if minutes < 59:
			if minutes < 11:
				if minutes >= 9:
					perhour1 = f'{hour-1}:{minutes+1}:00'
					perhour2 = f'{hour+1}:0{minutes-1}:00'
				else:
					perhour1 = f'{hour-1}:0{minutes+1}:00'
					perhour2 = f'{hour+1}:0{minutes-1}:00'
			else:
				perhour1 = f'{hour-1}:{minutes+1}:00'
				perhour2 = f'{hour+1}:{minutes-1}:00'
		else:
			perhour1 = f'{hour}:00:00'
			perhour2 = f'{hour+1}:{minutes-1}:00'
	else:
		perhour1 = f'{hour-1}:0{minutes+1}:00'
		perhour2 = f'{hour}:59:00'
	if len(perhour1) < 8:
		perhour1 = f'0{perhour1}'
	if len(perhour2) < 8:
		perhour2 = f'0{perhour2}'
	v = cur.execute('SELECT name FROM stud WHERE (clock BETWEEN ? AND ?) AND callendar == ? AND status_sum != ?', (perhour1, perhour2, x[1], 'boofer',)).fetchall()
	if not v:
		return 'no'
	else:
		return 'yes'


def sql_test(data):
	x = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'boofer',)).fetchone()
	minutes = int(str(x[0])[-2:])
	hour = int(str(x[0])[:-3])
	return minutes, hour



#вывод списка всех занятий
def sql_lesson_list(data):
	r = cur.execute('SELECT callendar, clock, status_sum FROM stud WHERE user_id == ? AND clock != ? AND (status_sum == ? OR status_sum == ? OR status_sum == ?)', (data, 'REG', '🔴', '🟢', '🟡',)).fetchall()
	return r

#вывод списка всех оплат ученика
def sql_payment_list(data):
	r = cur.execute('SELECT clock, callendar, status_sum FROM stud WHERE user_id == ? AND clock != ? AND (status_sum == ? OR status_sum == ? OR status_sum == ?)', (data, 'REG', 's🔴', 's🟢', 's🟡',)).fetchall()
	return r

#имя пользователя
def nametag_user(data):
	r = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	return str(r)

#new payment
async def new_payment_red(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()

#стоимость индивидуального занятия
def ind_cost():
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('individual cost',)).fetchone()
	return r

#стоимость индивидуального занятия
async def sql_add_ind_cost(state):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('individual cost',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ?', ('individual cost',))
		base.commit()
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()

#стоимость группового занятия
def group_cost():
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('group cost',)).fetchone()
	return r

#стоимость группового занятия
async def sql_add_group_cost(state):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('group cost',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ?', ('group cost',))
		base.commit()
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()

#запрос для while оплаты
def sql_dont_payd_check(data):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, '🔴',)).fetchone()
	if bool(r) is False:
		return 0
	else:
		return 1

def sql_sum_dnt_pay_les(data):
	r = cur.execute('SELECT COUNT(*) as count FROM stud WHERE user_id == ? AND status_sum == ?', (data, '🔴',)).fetchone()
	return r

#внесение оплаты
def sql_solopay_ind(data):
		r = cur.execute('SELECT clock, callendar, name FROM stud WHERE user_id == ? AND status_sum == ?', (data, 's🔴',)).fetchone()
		us = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, '🔴',)).fetchone()
		if bool(us) is True:
			s = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('individual cost',)).fetchone()
			itog = int(r[0]) - int(str(s)[2:-3])
			if itog > 0:
				cur.execute('UPDATE stud SET clock == ? WHERE user_id == ? AND name == ?', (itog, data, f'{r[2]}',))
				base.commit()
			elif itog == 0: 
				cur.execute('UPDATE stud SET clock == ?, status_sum == ? WHERE user_id == ? AND name == ?', (itog, 's🟢', data, f'{r[2]}',))
				base.commit()
			else:
				cur.execute('UPDATE stud SET clock == ?, status_sum == ? WHERE user_id == ? AND name == ?', (0, 's🟢', data, f'{r[2]}',))
				base.commit()
				sos = cur.execute('SELECT clock, callendar, name FROM stud WHERE user_id == ? AND status_sum == ?', (data, 's🔴',)).fetchone()
				cur.execute('UPDATE stud SET clock == ?, status_sum == ? WHERE user_id == ? AND name == ?', (itog, 's🟢', data, f'{sos[2]}',))
				base.commit()
			cur.execute('UPDATE stud SET name == ?, status_sum == ? WHERE user_id == ? AND clock = ? AND callendar == ? AND status_sum == ?',\
			 (f'({r[1]}, {r[2]})', '🟢', data, f'{str(us[0])}', f'{str(us[1])}', '🔴',))	
			base.commit()


#для автоматической оплаты
def sql_auto_pay(data):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('individual cost',)).fetchone()
	v = cur.execute('SELECT clock FROM stud WHERE user_id == ?', ('group cost',)).fetchone()
	sum_ost = cur.execute('SELECT SUM(clock) as sum FROM stud WHERE user_id == ? AND (status_sum == ? OR status_sum == ? OR status_sum == ?)', (data, 's🔴', 's🟡', 'help to pay',)).fetchone()
	return r, v, sum_ost

def help_payment(data):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'help to pay',)).fetchone()
	if bool(r) is False:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', (data, '-', 0, '-', 'help to pay',))
		base.commit()


#список транзакций
def sql_transaction_list(data):
	trans_list = cur.execute('SELECT callendar, clock, name, status_sum FROM stud WHERE user_id == ? AND (status_sum == ? OR status_sum == ?)', (data, '🔴', '🟢',)).fetchall()
	return trans_list


#список транзакции со стороны оплат
def sql_payment_transaction_list(data):
	trans_list = cur.execute('SELECT callendar, clock, name, status_sum FROM stud WHERE user_id == ? AND (status_sum == ? OR status_sum == ? OR status_sum == ?)', (data, 's🔴', 's🟢', 's🟡',)).fetchall()
	return trans_list


def sql_transaction_list_check(data):
	trans_list = cur.execute('SELECT callendar, clock, name, status_sum FROM stud WHERE user_id == ? AND status_sum == ?', (data, '🟢',)).fetchall()
	return trans_list




def sql_poof(data, i):
	r = cur.execute('SELECT status_sum FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',))
		base.commit()
	cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', (data, '-', i[1], i[0], 'poof',))
	base.commit()


async def sql_pooper_poo(data, i):
	r = cur.execute('SELECT status_sum FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',))
		base.commit()
	cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', (data, i[2], i[1], i[0], 'poof',))
	base.commit()



async def chenge_calendar(data, calend):
	r = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	cur.execute('UPDATE stud SET callendar == ? WHERE user_id == ? AND clock = ? AND callendar == ?', (calend, data, r[0], r[1],))	
	base.commit()

async def adm_chenge_calendar(data, calend, userdata):
	r = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	cur.execute('UPDATE stud SET callendar == ? WHERE user_id == ? AND clock = ? AND callendar == ?', (calend, userdata, r[0], r[1],))	
	base.commit()

def adm_new_calendar(data):
	r = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	adm = cur.execute('SELECT user_id FROM stud WHERE clock == ? AND status_sum == ?', ('REG', 'ADMIN',)).fetchone()
	name = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	return adm, name, r

async def finish_clock_chenger(state, data, userdata):
	r = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, "poof",)).fetchone()
	cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',))
	base.commit()
	cur.execute('UPDATE stud SET clock == ? WHERE user_id == ? AND clock == ? AND callendar == ?', ('??', userdata, r[0], r[1],))
	base.commit()
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()
	
def send_admin_change_time(data):
	r = cur.execute('SELECT clock, callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, "poof",)).fetchone()
	s = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	adm = cur.execute('SELECT user_id FROM stud WHERE status_sum == ?', ('ADMIN',)).fetchone()
	return r, s, adm



def changed_tim(data, userdata):
	r = cur.execute('SELECT name, clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	s = cur.execute('SELECT callendar FROM stud WHERE user_id == ? AND clock == ?', (userdata, '??',)).fetchone()
	cur.execute('UPDATE stud SET clock == ? WHERE user_id == ? AND clock == ?', (f'{r[0]}:{r[1]}', userdata, '??',))
	base.commit()
	return f'[{str(s)[2:-3]}] - ({r[0]}:{r[1]})'


def sql_pay_lists(data):
	r = cur.execute('SELECT name, callendar FROM stud WHERE user_id == ? AND name != ? AND status_sum == ?', (data, '_', '🟢',)).fetchall()
	return r


def send_check(data):
	r = cur.execute('SELECT name, callendar FROM stud WHERE user_id == ? AND (status_sum == ? OR status_sum == ? OR status_sum == ?)', (data, 's🔴', 's🟢', 's🟡',)).fetchall()
	return r

async def vznos_new(data, vznos):
	r = cur.execute('SELECT name, clock, callendar FROM stud WHERE user_id = ? AND status_sum == ?', (data, 'poof',)).fetchone()
	cur.execute('UPDATE stud SET clock == ?, callendar == ? WHERE user_id == ? AND clock == ? AND callendar == ?', (vznos, f'{str(vznos)}, {str(r[2]).split()[1]}', data, r[1], r[2],))
	base.commit()
	cur.execute('UPDATE stud SET clock == ?, callendar == ? WHERE user_id == ? AND status_sum == ?', (vznos, f'{str(vznos)}, {str(r[2]).split()[1]}', data, 'poof',))
	base.commit()

def obnov_check(data, doc):
	r = cur.execute('SELECT name, clock, callendar FROM stud WHERE user_id = ? AND status_sum == ?', (data, 'poof',)).fetchone()
	cur.execute('UPDATE stud SET name == ? WHERE user_id == ? AND name == ? AND clock == ? AND callendar == ?', (doc, data, r[0], r[1], r[2],))
	base.commit()
	cur.execute('UPDATE stud SET name == ? WHERE user_id == ? AND status_sum == ?', (doc, data,'poof',))
	base.commit()
	v = cur.execute('SELECT callendar FROM stud WHERE user_id = ? AND status_sum == ?', (data, 'poof',)).fetchone()
	return v

def sql_admin_name():
	s = cur.execute('SELECT user_id FROM stud WHERE status_sum == ?', ('ADMIN',)).fetchone()
	return s

def info_red_payp(data):
	s = cur.execute('SELECT user_id FROM stud WHERE status_sum == ?', ('ADMIN',)).fetchone()
	r = cur.execute('SELECT callendar FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	name = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	return [s, r, name]

def get_name(data):
	s = cur.execute('SELECT name FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	return s

def sql_delete_payment_xianzai(data):
	r = cur.execute('SELECT callendar, name FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'poof',)).fetchone()
	cur.execute('DELETE FROM stud WHERE user_id == ? AND name == ? AND callendar == ? AND status_sum != ?', (data, r[1], r[0], 'poof',))
	base.commit()
	return r[0]

def sql_my_students(data):
	me = cur.execute('SELECT status_sum FROM stud WHERE user_id == ? AND clock == ?', (data, 'REG',)).fetchone()
	students1 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	students2 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ? LIMIT 10', (data, 'REG',)).fetchall()
	if len(students1) > len(students2):
		return me, students2, 1
	else:
		return me, students1, 0

def sql_my_students_nomer_2(data):
	students1 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	students2 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ? LIMIT 20', (data, 'REG',)).fetchall()
	if len(students1) > len(students2):
		return 0, students2[9:], 1
	else:
		return 0, students2[9:], 0

def sql_my_students_nomer_3(data):
	students1 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	students2 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ? LIMIT 30', (data, 'REG',)).fetchall()
	if len(students1) > len(students2):
		return 0, students2[19:], 1
	else:
		return 0, students2[19:], 0

def sql_my_students_nomer_4(data):
	students1 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	students2 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ? LIMIT 40', (data, 'REG',)).fetchall()
	if len(students1) > len(students2):
		return 0, students2[29:], 1
	else:
		return 0, students2[29:], 0

def sql_my_students_nomer_5(data):
	students1 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	students2 = cur.execute('SELECT name FROM stud WHERE user_id != ? AND  clock == ? LIMIT 50', (data, 'REG',)).fetchall()
	if len(students1) > len(students2):
		return 0, students2[39:], 1
	else:
		return 0, students2[39:], 0

def user_list_for_admin(data):
	stud = cur.execute('SELECT user_id, name FROM stud WHERE user_id != ? AND  clock == ?', (data, 'REG',)).fetchall()
	return stud

async def new_redact_for_admin(data, state):
	r = cur.execute('SELECT clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',)).fetchone()
	if bool(r) is True:
		cur.execute('DELETE FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',))
		base.commit()
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()

def admin_redact_user(data):
	r = cur.execute('SELECT name, clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',)).fetchone()
	return r

def prov_user(data):
	r = cur.execute('SELECT status_sum FROM stud WHERE user_id == ? AND clock == ? AND status_sum == ?', (data, 'REG', 'ADMIN',)).fetchone()
	if bool(r) is True:
		return 0
	return 1

def idusers(data):
	r = cur.execute('SELECT name, clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',)).fetchone()
	return r

def idprov_user(data):
	r = cur.execute('SELECT status_sum FROM stud WHERE user_id == ? AND clock == ? AND status_sum == ?', (data, 'REG', 'ADMIN',)).fetchone()
	s = cur.execute('SELECT name, clock FROM stud WHERE user_id == ? AND status_sum == ?', (data, 'admin_redact',)).fetchone()
	if bool(r) is True:
		return 0, s
	return 1, s