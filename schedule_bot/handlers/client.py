from aiogram import types, Dispatcher
from create_bot import dp, bot 
from keyboards import start_button, kb_client, kb_admin, kb_time, time_min, time_min2, time_min3, time_min4, time_min5, time_min6, time_min7, time_min8, time_min9, Rtime_min10, \
Rtime_min11, Rtime_min12, Rtime_min13, Rtime_min14, Rtime_min15, Rtime_min16, Rtime_min17, Rtime_min18, Rtime_min19, time_min20, time_min21, time_min22, time_min23, time_min00, choise_user_keyboard
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, InputFile
from data_base import sqlite_db
import asyncio
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
import datetime
import time

#для текущей даты
now = datetime.datetime.now()

#машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


#класс машина состояний для регистрации
class FSMReg(StatesGroup):
	name = State()

#класс машина состояний для смены админ статуса
class FSMAdmstat(StatesGroup):
	status_sum = State()

#класс машина состояний для внесения нового урока
class FSMNewLesson(StatesGroup):
	callendar = State()
	clock = State()

#класс машина состояний для времени
class FSMTime(StatesGroup):
	timer = State()

#класс машина состояний для внесения картинки
class FSMPic1(StatesGroup):
	status_sum = State()

#класс машина состояний для внесения стоимости одного занятия
class FSMPay_cost(StatesGroup):
	cost = State()

#класс машина состояний для внесения стоимости группового занятия
class FSMPay_cost_group(StatesGroup):
	cost = State()


#класс машина состояний для внесения оплаты
class FSMPayment_new(StatesGroup):
	symma = State()
	file = State()


#класс машина состояний для просмотра чека
class FSMCheckList(StatesGroup):
	num = State()


class FSMRedactorLes(StatesGroup):
	num = State()


class FSMRedTimer(StatesGroup):
	num = State()
	com = State()

class FSMCheck_pay(StatesGroup):
	sym = State()

class FSMChangePayw(StatesGroup):
	first = State()

class FSMch_p_vz(StatesGroup):
	vznos = State()

class FSMch_pr_check(StatesGroup):
	check = State()

class FSMzapros_red_pay(StatesGroup):
	zapros = State()


#Admin

class FSMAdmChoiceYch(StatesGroup):
	user = State()

class FSMAdmMesYch(StatesGroup):
	user = State()

class FSMAnswerAdminMessage(StatesGroup):
	user = State()


#registration and join - (1)


async def commands_start(message : types.Message):
	await bot.send_photo(chat_id=message.from_user.id, photo=sqlite_db.sql_start_pic()[0], caption='Если вы тут впервые, пройдите регистрацию по кнопке. \n \nЕсли вы зарегистрированы, нажмите кнопку "войти".', reply_markup=start_button)



async def callback_registr(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='✅', callback_data="got")))
	if sqlite_db.sql_prov_reg(call.from_user.id) == '':
		await FSMReg.name.set()
		await bot.send_message(chat_id=call.from_user.id, text='Чтобы зарегестрироваться, введите\nсвое ФИО в таком формате: \n\n*(Иванов Иван Иванович)*📍', parse_mode="Markdown")
	else:
		r = str(sqlite_db.sql_prov_reg(call.from_user.id))
		await bot.send_message(call.from_user.id, text=f'{(str(r)[2:-3]).split()[1]}, вы и так зарегистрированы в системе!\n\nЕсли хотите поменять свое имя,\nнажмите кнопку ниже или войдите\nпод этим именем.', \
			reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Войти', callback_data="join")).add(InlineKeyboardButton(text='Сменить имя', callback_data="change_name")))


async def load_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
		data['name'] = message.text
		data['clock'] = 'REG'
		data['callendar'] = 'no'
		data['status_sum'] = 'USER'
	await sqlite_db.sql_add_name(state)
	await state.finish()
	if len(str(sqlite_db.sql_prov_reg(message.from_user.id)).split()) < 3:
		await message.answer ('ваше имя слишком короткое!\nПридется зарегистрироваться заново.\n\n(читайте сообщения бота внимательнее!)', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Ввести снова >>>', callback_data="yes_change")))
	else:
		await message.answer('вы успешно зарегистрировались!', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Войти', callback_data="join")))


async def callback_join(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='✅', callback_data="join_da1")))
	r = str(sqlite_db.sql_prov_reg(call.from_user.id))
	if r == '':
		await bot.send_message(call.from_user.id, text='К сожалению, вы не зарегистрированы :(', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Регистрация', callback_data="registration")))
	else:
		if sqlite_db.sql_adm_check(call.from_user.id) == 1:
			await bot.send_message(chat_id=call.from_user.id, reply_markup=kb_admin, text=f'Здравствуй, {(str(r)[2:-3]).split()[1]}! \n \
				\nЗдесь вы можете планировать занятия со своим учениками, \nредактировать их и подтверждать статусы оплаты!')
		else:
			await bot.send_message(chat_id=call.from_user.id, reply_markup=kb_client, text=f'Здравствуй, {(str(r)[2:-3]).split()[1]}! \n \
				\nЗдесь ты можешь планировать занятия со своим учителем, \nредактировать их и отмечать статус оплаты, \nприкрепляя чеки из твоего онлайн банка!')
			sqlite_db.help_payment(call.from_user.id)


async def callback_change_name(message: Message):
	await bot.send_message(message.from_user.id, text='Ваше старое имя удалиться и придется заново проходить регистрацию, вы уверены?\n(но уже отмеченые тут ваши занятия и оплаты останутся под старым именем).',\
	 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Уверен(а)', callback_data="yes_change")).add(InlineKeyboardButton(text='Отмена', callback_data="registration")))


async def callback_yver_change_name(message: Message):
	await sqlite_db.sql_delite_name(message.from_user.id)
	await bot.send_message(message.from_user.id, text='Ваше старое имя удалено, пройдите регистрацию заново.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Регистрация', callback_data="registration")))



#admin panel - (2)

async def my_students(message : types.Message):
	res = sqlite_db.sql_my_students(message.from_user.id)
	if str(res[0])[2:-3] == 'ADMIN':
		stud_list = []
		count = 0
		for i in res[1]:
			count += 1
			stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
			if len(res[1]) == count:
				if res[2] == 1:
					stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
					stud_list.append(([InlineKeyboardButton(text=f' ', callback_data='nnpp'), InlineKeyboardButton(text=f'Страница №1', callback_data='nnpp'), InlineKeyboardButton(text=f'>>>', callback_data='sled_str_stud_2')]))
				else:
					stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
		stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
		await bot.send_message(chat_id=message.from_user.id, text=f'(если вам нужно выбрать какого-то ученика, запомните его номер и нажмите соответствующую кнопку на клавиатуре 🔹)\n\nВсе ваши зарегестрированные ученики:', reply_markup=stud_users)
	else:
		await bot.send_message(chat_id=message.from_user.id, text=f'У вас недостаточно прав.')

async def clon_my_students(call):
	res = sqlite_db.sql_my_students(call.from_user.id)
	stud_list = []
	count = 0
	for i in res[1]:
		count += 1
		stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
		if len(res[1]) == count:
			if res[2] == 1:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f' ', callback_data='nnpp'), InlineKeyboardButton(text=f'Страница №1', callback_data='nnpp'), InlineKeyboardButton(text=f'>>>', callback_data='sled_str_stud_2')]))
			else:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
	stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
	await call.message.edit_reply_markup(stud_users)


async def sled_str_stud_2(call):
	res = sqlite_db.sql_my_students_nomer_2(call.from_user.id)
	stud_list = []
	count = 10
	for i in res[1]:
		count += 1
		stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
		if int(len(res[1]))+10 == count:
			if res[2] == 1:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='clon_my_students'), InlineKeyboardButton(text=f'Страница №2', callback_data='nnpp'), InlineKeyboardButton(text=f'>>>', callback_data='sled_str_stud_3')]))
			else:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='clon_my_students'), InlineKeyboardButton(text=f'Страница №2', callback_data='nnpp'), InlineKeyboardButton(text=f' ', callback_data='nnpp')]))
	stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
	await call.message.edit_reply_markup(stud_users)


async def sled_str_stud_3(call):
	res = sqlite_db.sql_my_students_nomer_3(call.from_user.id)
	stud_list = []
	count = 20
	for i in res[1]:
		count += 1
		stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
		if int(len(res[1]))+20 == count:
			if res[2] == 1:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='sled_str_stud_2'), InlineKeyboardButton(text=f'Страница №3', callback_data='nnpp'), InlineKeyboardButton(text=f'>>>', callback_data='sled_str_stud_4')]))
			else:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='sled_str_stud_2'), InlineKeyboardButton(text=f'Страница №3', callback_data='nnpp'), InlineKeyboardButton(text=f' ', callback_data='nnpp')]))
	stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
	await call.message.edit_reply_markup(stud_users)


async def sled_str_stud_4(call):
	res = sqlite_db.sql_my_students_nomer_4(call.from_user.id)
	stud_list = []
	count = 30
	for i in res[1]:
		count += 1
		stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
		if int(len(res[1]))+30 == count:
			if res[2] == 1:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='sled_str_stud_3'), InlineKeyboardButton(text=f'Страница №4', callback_data='nnpp'), InlineKeyboardButton(text=f'>>>', callback_data='sled_str_stud_5')]))
			else:
				stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
				stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='sled_str_stud_3'), InlineKeyboardButton(text=f'Страница №4', callback_data='nnpp'), InlineKeyboardButton(text=f' ', callback_data='nnpp')]))
	stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
	await call.message.edit_reply_markup(stud_users)


async def sled_str_stud_5(call):
	res = sqlite_db.sql_my_students_nomer_5(call.from_user.id)
	stud_list = []
	count = 40
	for i in res[1]:
		count += 1
		stud_list.append([InlineKeyboardButton(text=f'{count}. {str(i)[2:-3]}', callback_data=str(i)[2:-3])])
		if int(len(res[1]))+40 == count:
			stud_list.append([InlineKeyboardButton(text=f'Выбор ученика 🔹', callback_data='sled_stud'), InlineKeyboardButton(text=f'Должники 😡', callback_data='dolg')])
			stud_list.append(([InlineKeyboardButton(text=f'<<<', callback_data='sled_str_stud_4'), InlineKeyboardButton(text=f'Страница №5', callback_data='nnpp'), InlineKeyboardButton(text=f' ', callback_data='nnpp')]))
	stud_users = InlineKeyboardMarkup(inline_keyboard=stud_list)
	await call.message.edit_reply_markup(stud_users)


#обработка каждого ученика
async def sled_stud(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data='nnpp')))
	await bot.send_message(chat_id=call.from_user.id, text='Напишите номер ученика:', reply_markup=ReplyKeyboardRemove())
	await FSMAdmChoiceYch.user.set()

async def AdmChoiceYch(message : types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		user_list = sqlite_db.user_list_for_admin(message.from_user.id)
		if int(message.text) <= len(user_list) and int(message.text) > 0:
			my_user = user_list[int(message.text)-1]
			async with state.proxy() as data:
				data['user_id'] = message.from_user.id
				data['name'] = my_user[0]
				data['clock'] = my_user[1]
				data['callendar'] = '-'
				data['status_sum'] = 'admin_redact'
			await sqlite_db.new_redact_for_admin(message.from_user.id, state)
			await state.finish()
			await bot.send_message(chat_id=message.from_user.id, text=f'✅', reply_markup=kb_admin)
			await bot.send_message(chat_id=message.from_user.id, text=f'Вы зашли в профиль ученика - {my_user[1]}, \nBыберите дальнейшие действия c ним:', reply_markup=choise_user_keyboard)
		else:
			await bot.send_message(chat_id=message.from_user.id, text='Вы написали номер, которого не существует, впишите номер еще раз:')
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Напишите номер ученика корректно, без каких-либо дополнительных знаков (пример "5"):')



async def mess_user_check_adm_panel(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data='nnpp')))
	await bot.send_message(chat_id=call.from_user.id, text='Напишите сообщение ученику:\n(если передумали, напишите слово "отмена")', reply_markup=ReplyKeyboardRemove())
	await FSMAdmMesYch.user.set()

async def AdmMesYch(message : types.Message, state: FSMContext):
	usr = sqlite_db.admin_redact_user(message.from_user.id)
	if message.text == 'отмена':
		await bot.send_message(chat_id=message.from_user.id, text='Вы отменили отправку сообщения.', reply_markup=kb_admin)
		await state.finish()
		await bot.send_message(chat_id=message.from_user.id, text=f'Вы выбрали ученика - {usr[1]}, \nBыберите дальнейшие действия c ним:', reply_markup=choise_user_keyboard)
	else:
		await bot.send_message(chat_id=message.from_user.id, text=f'✅', reply_markup=kb_admin)
		await bot.send_message(chat_id=message.from_user.id, text=f'Cообщение успешно отправлено ученику\n{usr[1]}!\nBыберите дальнейшие действия c ним:', reply_markup=choise_user_keyboard)
		await bot.send_message(chat_id=usr[0], text=f'Вам пришло новое сообщение от учителя:\n"{str(message.text)}"', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Ответить', callback_data='mess_to_admin')))
		await state.finish()


#ответить админу
async def mess_to_admin(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data='nnpp')))
	await bot.send_message(chat_id=call.from_user.id, text='Чтобы ответить учителю, напишите текст в следующем сообщени:', reply_markup=ReplyKeyboardRemove())
	await FSMAnswerAdminMessage.user.set()

async def AnswerAdminMessage(message : types.Message, state: FSMContext):
	adm = sqlite_db.sql_admin_name()
	name = sqlite_db.get_name(message.from_user.id)
	await bot.send_message(chat_id=int(str(adm)[2:-3]), text=f'Вам пришло сообщение от {str(name)[2:-3]}:\n"{str(message.text)}"')
	await bot.send_message(chat_id=message.from_user.id, text='Вы успешно отправили сообщение учителю!', reply_markup=kb_client)
	await state.finish()



async def rasp_users_check(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data='nnpp')))
	



#user panel lessons - (3)

async def my_lessons_command(message : types.Message):
	#await sqlite_db.sql_got_les(message.from_user.id)
	k = 0
	count_dpl = int(str(sqlite_db.sql_sum_dnt_pay_les(message.from_user.id))[1:-2])

	if count_dpl > 0:
		all_payment = sqlite_db.sql_auto_pay(message.from_user.id)
		ind_c = int(str(all_payment[0])[2:-3])
		gr_c = int(str(all_payment[1])[2:-3])
		ost = int(str(all_payment[2])[1:-2])
		while ost >= (ind_c or gr_c):
			if ind_c <= ost:
				sqlite_db.sql_solopay_ind(message.from_user.id)
				ost -= ind_c
			else:
				ost = 0
	user_lessons_list2 = sqlite_db.sql_lesson_list(message.from_user.id)
	user_lessons_button_list2 = []
	for item in list(reversed(user_lessons_list2)):
		user_lessons_button_list2.append([InlineKeyboardButton(text="["+str(item)[2:12]+"] - ("+str(item)[16:21]+") "+str(item)[-3:-2], callback_data=str(item))])
		k += 1
		if len(user_lessons_list2) == k:
			user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
			user_lessons_button_list2.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_func')])
	if not user_lessons_list2:
		user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
	lessons_user2 = InlineKeyboardMarkup(inline_keyboard=user_lessons_button_list2, row_width=1)
	await message.answer(text='♻️', reply_markup=kb_client)
	await message.answer(text='Здесь видны ваши активные занятия с учителем\n(которые вы уже загрузили):', reply_markup=lessons_user2)


#доп функции
async def dop_func_lesson(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='Мои транзакции 💳', callback_data="trans")).add(InlineKeyboardButton(text='Редактировать расписание ⚙️', callback_data="redactor_rasp")).add(InlineKeyboardButton(text='<<< Назад', callback_data="back_to_lesson")))


#оплаты хуй
async def transaction(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	prov = sqlite_db.idprov_user(call.from_user.id)
	if prov[0] == 1:
		les_list = sqlite_db.sql_transaction_list(call.from_user.id)
	else:
		les_list = sqlite_db.sql_transaction_list((prov[1])[0])
	ind_cost = str(sqlite_db.ind_cost())[2:-3]
	pay_str = ""
	status_payment = ""
	pay_info = ""
	kk = 1
	for i in les_list:
		if i[3] == '🟢':
			status_payment = 'оплачено ✅'
			pay_info = f'Дата платежа: {str(str(i[2]).split()[1])[:-1]}\n'
		else:
			status_payment = 'не оплачено ☑'
			pay_info = ''
		pay_str += f'🔘 Урок №: {str(kk)}\nДата и время: [{str(i[0])}] - ({str(i[1])})\nСтатус оплаты: {status_payment}\n{pay_info}\n'
		kk += 1
	if prov[0] == 1:
		await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны все ваши оплаты, \
			\nстоимость одного индивидуального\n занятия - {ind_cost} ₽.\nЧтобы посмотреть чек об оплате, \
			\nнажмите на кнопку снизу и \nвпишите номер занятия:\n______________________________________\n\
			\n{pay_str}', reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text='<<< Назад', callback_data='s_dop_func_double'), InlineKeyboardButton(text='Посмотреть чек', callback_data='check_payment_look')))
	else:
		await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны все оплаты ученика - \
			\n{(prov[1])[1]}\nстоимость одного индивидуального\n занятия - {ind_cost} ₽.\nЧтобы посмотреть чек об оплате, \
			\nнажмите на кнопку снизу и \nвпишите номер занятия:\n______________________________________\n\
			\n{pay_str}', reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text='<<< Назад', callback_data='s_dop_func_double'), InlineKeyboardButton(text='Посмотреть чек', callback_data='check_payment_look')))
	


async def look_at_chek(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	pro = sqlite_db.idprov_user(call.from_user.id)
	if pro[0] == 1:
		les_list = sqlite_db.sql_transaction_list_check(call.from_user.id)
	else:
		les_list = sqlite_db.sql_transaction_list_check((pro[1])[0])
	if len(les_list) > 0:
		ind_cost = str(sqlite_db.ind_cost())[2:-3]
		pay_str = ""
		status_payment = ""
		pay_info = ""
		kk = 1
		for i in les_list:
			if i[3] == '🟢':
				status_payment = 'оплачено ✅'
				pay_info = f'Дата платежа: {str(str(i[2]).split()[1])[:-1]}\n'
			pay_str += f'🔘 Урок №: {str(kk)}\nДата и время: [{str(i[0])}] - ({str(i[1])})\nСтатус оплаты: {status_payment}\n{pay_info}\n'
			kk += 1
		await bot.send_message(chat_id=call.from_user.id, text=f'Введите номер урока (только одной цифрой),\nкоторый можно увидеть ниже:\n______________________________________\n\n{pay_str}', reply_markup=ReplyKeyboardRemove())
		await FSMCheckList.num.set()
	else:
		await bot.send_message(chat_id=call.from_user.id, text=f'У вас нет оплаченых уроков.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='trans')).add(InlineKeyboardButton(text='Вернуться к списку уроков 🎓', callback_data='back_to_lesson')))

async def check_check_kek(message: types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		pro = sqlite_db.idprov_user(message.from_user.id)
		if pro[0] == 1:
			les_list = sqlite_db.sql_transaction_list_check(message.from_user.id)
		else:
			les_list = sqlite_db.sql_transaction_list_check((pro[1])[0])
		if len(les_list) < int(message.text):
			await bot.send_message(chat_id=message.from_user.id, text='Вы ввели число, которого нет в списке, попробуйте еще раз')
		else:
			k = 1
			for i in les_list:
				if int(message.text) == k:
					await bot.send_document(chat_id=message.from_user.id, document=str(str(i[2]).split()[2])[:-1], caption=f'Чек об оплате за {str(str(i[2]).split()[1])[:-1]}', reply_markup=kb_client)
					await state.finish()
					await bot.send_message(chat_id=message.from_user.id, text='Выберите дальнейшее действие:', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться к списку уроков 🎓', callback_data='back_to_lesson')).add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='trans')).add(InlineKeyboardButton(text='Вернуться к чекам 📄', callback_data='check_payment_look')))
				k += 1
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите число корректно')



async def redactor_lesson(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	idu = sqlite_db.idprov_user(call.from_user.id)
	if idu[0] == 1:
		les_list = sqlite_db.sql_transaction_list(call.from_user.id)
	else:
		les_list = sqlite_db.sql_transaction_list((idu[1])[0])
	if len(les_list) > 0:
		pay_str = ""
		kk = 1
		for i in les_list:
			pay_str += f'🔘 Урок №: {str(kk)}\nДата и время: [{str(i[0])}] - ({str(i[1])})\n\n'
			kk += 1
		await bot.send_message(chat_id=call.from_user.id, text=f'Введите номер урока для \nредактирования, который можно \nвидеть ниже:\n\n|только одной цифрой|\n|все оплаты сохранятся|\n|введите ["Нет"/"нет"/"No"/"no"] для отмены редактирования|\n______________________________________\n\n{pay_str}', reply_markup=ReplyKeyboardRemove())
		await FSMRedactorLes.num.set()
	else:
		bot.send_message(chat_id=call.from_user.id, text=f'У вас нет оплаченых уроков.')


async def redactor_lesson_num(message : types.Message, state: FSMContext):
	idu = sqlite_db.idprov_user(message.from_user.id)
	if str(message.text).isdigit() == True:
		if idu[0] == 1:
			les_list = sqlite_db.sql_transaction_list(message.from_user.id)
		else: 
			les_list = sqlite_db.sql_transaction_list((idu[1])[0])
		if len(les_list) < int(message.text):
			await bot.send_message(chat_id=message.from_user.id, text='Вы ввели число, которого нет в списке, попробуйте еще раз')
		else:
			k = 1
			for i in les_list:
				if int(message.text) == k:
					await state.finish()
					sqlite_db.sql_poof(message.from_user.id, i)
					await bot.send_message(chat_id=message.from_user.id, text=f'Выберите, что хотите отредактировать в выбраном уроке:\n.\nДата и время: *[{str(i[0])}] - ({str(i[1])})* \n.\n', reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text='Редактировать дату', callback_data='redact_data_solo_lesson'), InlineKeyboardButton(text='Редактировать время', callback_data='time_red')).add(InlineKeyboardButton(text='<<< Назад', callback_data='redactor_rasp')), parse_mode="Markdown")
				k += 1
	else:
		if idu[0] == 1: 
			if str(message.text) == 'нет' or str(message.text) == 'Нет' or str(message.text) == 'No' or str(message.text) == 'no':
				await state.finish()
				await bot.send_message(chat_id=message.from_user.id, text='♻️', reply_markup=kb_client)
				await bot.send_message(chat_id=message.from_user.id, text='Здесь расположена дополнительная информация по вашим индивидуальным занятиям:', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Мои транзакции 💳', callback_data="trans")).add(InlineKeyboardButton(text='Редактировать расписание ⚙️', callback_data="redactor_rasp")).add(InlineKeyboardButton(text='<<< Назад', callback_data="back_to_lesson")))
			else:
				await bot.send_message(chat_id=message.from_user.id, text='Введите число корректно')
		else:
			if str(message.text) == 'нет' or str(message.text) == 'Нет' or str(message.text) == 'No' or str(message.text) == 'no':
				await state.finish()
				await bot.send_message(chat_id=message.from_user.id, text='♻️', reply_markup=kb_admin)
				await bot.send_message(chat_id=message.from_user.id, text=f'Здесь расположена дополнительная информация по индивидуальным занятиям ученика {(idu[1])[1]}:', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Транзакции 💳', callback_data="trans")).add(InlineKeyboardButton(text='Редактировать расписание ⚙️', callback_data="redactor_rasp")).add(InlineKeyboardButton(text='<<< Назад', callback_data="back_to_lesson")))
			else:
				await bot.send_message(chat_id=message.from_user.id, text='Введите число корректно')



async def red_les_cal(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет редактирование занятия...', callback_data="nnls")))
	await bot.send_message(chat_id=call.from_user.id, text='Выберите новое число:', reply_markup=await DialogCalendar().start_calendar())


async def red_les_cal_an(callback_query: CallbackQuery, callback_data: dict):
	selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
	idu = sqlite_db.idprov_user(callback_query.from_user.id)
	red = sqlite_db.send_admin_change_time(callback_query.from_user.id)
	if selected:
		await callback_query.message.answer(f'Вы изменили дату - {date.strftime("%d/%m/%Y")}\n\nВыберите дальнейшее действие:', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Редактировать время ⏱', callback_data="time_red")).add(InlineKeyboardButton(text='Назад к редактору ⚙️', callback_data="redactor_rasp")).add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='trans')).add(InlineKeyboardButton(text='Вернуться к списку уроков 🎓', callback_data='back_to_lesson')))
		if idu[0] == 1:
		    await bot.send_message(chat_id=callback_query.from_user.id, text='♻️', reply_markup=kb_client)
		    calend = date.strftime("%d/%m/%Y")
		    await bot.send_message(chat_id=f'{int(str(red[2])[2:-3])}', text=f'Пользователь - {str(red[1])[2:-3]} \nизменил дату индивидуального урока \nс [{str(str(red[0])[2:].split()[1])[1:-2]}] на [{calend}] - ({str(str(red[0])[2:-3].split()[0])[:-2]})')
		    await sqlite_db.chenge_calendar(callback_query.from_user.id, calend)
		else:
		    await bot.send_message(chat_id=callback_query.from_user.id, text='♻️', reply_markup=kb_admin)
		    calend = date.strftime("%d/%m/%Y")
		    await sqlite_db.adm_chenge_calendar(callback_query.from_user.id, calend, (idu[1])[0])
		    await bot.send_message(chat_id=f'{(idu[1])[0]}', text=f'Учитель изменил дату индивидуального урока \nс [{str(str(red[0])[2:].split()[1])[1:-2]}] на [{calend}] - ({str(str(red[0])[2:-3].split()[0])[:-2]})')



async def red_les_time(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет редактирование занятия...', callback_data="nnls")))
	await bot.send_message(chat_id=call.from_user.id, text='Впишите самостоятельно новое время (только час):', reply_markup=ReplyKeyboardRemove())
	await FSMRedTimer.num.set()

async def red1_les_time_FSM(message : types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		if int(message.text) >= 0 and int(message.text) <= 23:
			async with state.proxy() as data:
				data['user_id'] = message.from_user.id
				if len(message.text) < 2:
					data['name'] = '0'+f'{str(message.text)}'
				else:
					data['name'] = message.text
			await FSMRedTimer.next()
			await bot.send_message(chat_id=message.from_user.id, text='Теперь впишите только минуты:')
		else:
			await bot.send_message(chat_id=message.from_user.id, text='Часовой формат от 0 часов до 23, впишите еще раз')
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите час заново (пример: "12")')



async def red2_timer_last(message : types.Message, state: FSMContext):
	idu = sqlite_db.idprov_user(message.from_user.id)
	if str(message.text).isdigit() == True:
		if int(message.text) >= 0 and int(message.text) <= 59:
			async with state.proxy() as data:
				if len(message.text) < 2:
					data['clock'] = '0'+f'{str(message.text)}'
				else:
					data['clock'] = message.text
				data['callendar'] = 'no'
				data['status_sum'] = 'poof'
			red = sqlite_db.send_admin_change_time(message.from_user.id)
			if idu == 1:
				await sqlite_db.finish_clock_chenger(state, message.from_user.id)
				tm = sqlite_db.changed_tim(message.from_user.id)
				await bot.send_message(chat_id=int(str(red[2])[2:-3]), text=f'Пользователь - {str(red[1])[2:-3]} \nизменил время индивидуального урока \nс (\
					{str(str(red[0]).split()[0])[2:-2]}) на ({str(tm)[-6:-1]}),\nДата занятия - [{str(str(red[0]).split()[1])[1:-2]}]')
				await state.finish()
				await bot.send_message(chat_id=message.from_user.id, text=f'Вы успешно изменили время на {tm} !', reply_markup=InlineKeyboardMarkup()\
					.add(InlineKeyboardButton(text='Редактировать дату', callback_data='redact_data_solo_lesson'))\
					.add(InlineKeyboardButton(text='Назад к редактору ⚙️', callback_data="redactor_rasp"))\
					.add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='trans'))\
					.add(InlineKeyboardButton(text='Вернуться к списку уроков 🎓', callback_data='back_to_lesson')))
			else:
				await sqlite_db.finish_clock_chenger(state, message.from_user.id, (idu[1])[0])
				tm = sqlite_db.changed_tim(message.from_user.id, (idu[1])[0])
				await bot.send_message(chat_id=(idu[1])[0], text=f'Учитель изменил время индивидуального урока \nс (\
					{str(str(red[0]).split()[0])[2:-2]}) на ({str(tm)[-6:-1]}),\nДата занятия - [{str(str(red[0]).split()[1])[1:-2]}]')
				await state.finish()
				await bot.send_message(chat_id=message.from_user.id, text=f'Вы успешно изменили время на {tm}!', reply_markup=InlineKeyboardMarkup()\
					.add(InlineKeyboardButton(text='Редактировать дату', callback_data='redact_data_solo_lesson'))\
					.add(InlineKeyboardButton(text='Назад к редактору ⚙️', callback_data="redactor_rasp"))\
					.add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='trans'))\
					.add(InlineKeyboardButton(text='Вернуться к списку уроков 🎓', callback_data='back_to_lesson')))
		else:
			await bot.send_message(chat_id=message.from_user.id, text='Часовой формат от 0 минут до 59, впишите еще раз')
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите минуты заново (пример: "35")')




async def clon_lesson1(call):
	if sqlite_db.prov_user(call.from_user.id) == 1:
		k = 0
		user_lessons_list2 = sqlite_db.sql_lesson_list(call.from_user.id)
		user_lessons_button_list2 = []
		for item in list(reversed(user_lessons_list2)):
			user_lessons_button_list2.append([InlineKeyboardButton(text="["+str(item)[2:12]+"] - ("+str(item)[16:21]+") "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_lessons_list2) == k:
				user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
				user_lessons_button_list2.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_func')])
		if not user_lessons_list2:
			user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
		lessons_user2 = InlineKeyboardMarkup(inline_keyboard=user_lessons_button_list2, row_width=1)
		await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data='//waiting//')))
		await bot.send_message(chat_id=call.from_user.id, text='Здесь видны ваши активные занятия с учителем\n(которые вы уже загрузили):', reply_markup=lessons_user2)
	else:
		id_y = sqlite_db.idusers(call.from_user.id)
		k = 0
		user_lessons_list2 = sqlite_db.sql_lesson_list(id_y[0])
		user_lessons_button_list2 = []
		for item in list(reversed(user_lessons_list2)):
			user_lessons_button_list2.append([InlineKeyboardButton(text="["+str(item)[2:12]+"] - ("+str(item)[16:21]+") "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_lessons_list2) == k:
				user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
				user_lessons_button_list2.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_func')])
				user_lessons_button_list2.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		if not user_lessons_list2:
			user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
			user_lessons_button_list2.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		lessons_user2 = InlineKeyboardMarkup(inline_keyboard=user_lessons_button_list2, row_width=1)
		await call.message.edit_reply_markup(lessons_user2)
		#await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data='//waiting//')))
		#await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны активные занятия с {id_y[1]}\n(которые вы уже загрузили):', reply_markup=lessons_user2)
#хуй!


async def new_lesson_user(call):
	await sqlite_db.bezop_dob_les(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет добавление нового урока...', callback_data="nnls")))
	await bot.send_message(chat_id=call.from_user.id, text="♻️", reply_markup=ReplyKeyboardRemove())
	await bot.send_message(chat_id=call.from_user.id, text="Чтобы добавить новую запись, сначала выберите дату занятия: ", reply_markup=await SimpleCalendar().start_calendar())



async def new_lesson_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Вы выбрали дату - {date.strftime("%d/%m/%Y")}', reply_markup=kb_time)
        await sqlite_db.sql_timer(callback_query.from_user.id, date.strftime("%d/%m/%Y"))


#ответы на часы


async def change_callendar(call):
	await call.message.edit_reply_markup(await SimpleCalendar().start_calendar())

async def cancel_hours(call):
	await call.message.edit_reply_markup(kb_time)

async def next_time_01(call):
	await call.message.edit_reply_markup(time_min)
	await sqlite_db.sql_hour_timer(call.from_user.id, '01')

async def next_time_02(call):
	await call.message.edit_reply_markup(time_min2)
	await sqlite_db.sql_hour_timer(call.from_user.id, '02')

async def next_time_03(call):
	await call.message.edit_reply_markup(time_min3)
	await sqlite_db.sql_hour_timer(call.from_user.id, '03')

async def next_time_04(call):
	await call.message.edit_reply_markup(time_min4)
	await sqlite_db.sql_hour_timer(call.from_user.id, '04')

async def next_time_05(call):
	await call.message.edit_reply_markup(time_min5)
	await sqlite_db.sql_hour_timer(call.from_user.id, '05')

async def next_time_06(call):
	await call.message.edit_reply_markup(time_min6)
	await sqlite_db.sql_hour_timer(call.from_user.id, '06')

async def next_time_07(call):
	await call.message.edit_reply_markup(time_min7)
	await sqlite_db.sql_hour_timer(call.from_user.id, '07')

async def next_time_08(call):
	await call.message.edit_reply_markup(time_min8)
	await sqlite_db.sql_hour_timer(call.from_user.id, '08')

async def next_time_09(call):
	await call.message.edit_reply_markup(time_min9)
	await sqlite_db.sql_hour_timer(call.from_user.id, '09')

async def Rnext_time_10(call):
	await call.message.edit_reply_markup(Rtime_min10)
	await sqlite_db.sql_hour_timer(call.from_user.id, '10')

async def Rnext_time_11(call):
	await call.message.edit_reply_markup(Rtime_min11)
	await sqlite_db.sql_hour_timer(call.from_user.id, '11')

async def Rnext_time_12(call):
	await call.message.edit_reply_markup(Rtime_min12)
	await sqlite_db.sql_hour_timer(call.from_user.id, '12')

async def Rnext_time_13(call):
	await call.message.edit_reply_markup(Rtime_min13)
	await sqlite_db.sql_hour_timer(call.from_user.id, '13')

async def Rnext_time_14(call):
	await call.message.edit_reply_markup(Rtime_min14)
	await sqlite_db.sql_hour_timer(call.from_user.id, '14')

async def Rnext_time_15(call):
	await call.message.edit_reply_markup(Rtime_min15)
	await sqlite_db.sql_hour_timer(call.from_user.id, '15')

async def Rnext_time_16(call):
	await call.message.edit_reply_markup(Rtime_min16)
	await sqlite_db.sql_hour_timer(call.from_user.id, '16')

async def Rnext_time_17(call):
	await call.message.edit_reply_markup(Rtime_min17)
	await sqlite_db.sql_hour_timer(call.from_user.id, '17')

async def Rnext_time_18(call):
	await call.message.edit_reply_markup(Rtime_min18)
	await sqlite_db.sql_hour_timer(call.from_user.id, '18')

async def Rnext_time_19(call):
	await call.message.edit_reply_markup(Rtime_min19)
	await sqlite_db.sql_hour_timer(call.from_user.id, '19')

async def next_time_20(call):
	await call.message.edit_reply_markup(time_min20)
	await sqlite_db.sql_hour_timer(call.from_user.id, '20')

async def next_time_21(call):
	await call.message.edit_reply_markup(time_min21)
	await sqlite_db.sql_hour_timer(call.from_user.id, '21')

async def next_time_22(call):
	await call.message.edit_reply_markup(time_min22)
	await sqlite_db.sql_hour_timer(call.from_user.id, '22')

async def next_time_23(call):
	await call.message.edit_reply_markup(time_min23)
	await sqlite_db.sql_hour_timer(call.from_user.id, '23')

async def next_time_00(call):
	await call.message.edit_reply_markup(time_min00)
	await sqlite_db.sql_hour_timer(call.from_user.id, '00')

#ответы на минуты

async def change_all_time(call):
	await call.message.edit_reply_markup(kb_time)

async def next_min(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':00')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min2(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':05')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min3(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':10')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min4(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':15')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min5(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':20')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min6(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':25')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min7(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':30')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min8(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':35')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min9(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':40')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min10(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':45')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min11(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':50')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))

async def next_min12(call):
	await sqlite_db.sql_min_timer(call.from_user.id, ':55')
	r = sqlite_db.sql_timer_insert(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Вы выбрали время - {str(r)[2:-3]}', callback_data="ttmm")).row(InlineKeyboardButton(text='Готово', callback_data="sum_status"), InlineKeyboardButton(text='Изменить время', callback_data="change_all_time")))


async def callback_gotovo_lesson(call):
	r = sqlite_db.sql_zanyato_time(call.from_user.id)
	if r == 'no':
		adm = sqlite_db.prov_user(call.from_user.id)
		if adm == 1:
			await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='✅', callback_data="got")))
			await sqlite_db.sql_got_les(call.from_user.id)
			k = 0
			count_dpl = int(str(sqlite_db.sql_sum_dnt_pay_les(call.from_user.id))[1:-2])
			if count_dpl > 0:
				all_payment = sqlite_db.sql_auto_pay(call.from_user.id)
				ind_c = int(str(all_payment[0])[2:-3])
				gr_c = int(str(all_payment[1])[2:-3])
				ost = int(str(all_payment[2])[1:-2])
				while ost >= (ind_c or gr_c):
					if ind_c <= ost:
						sqlite_db.sql_solopay_ind(call.from_user.id)
						ost -= ind_c
					else:
						ost = 0
			user_lessons_list2 = sqlite_db.sql_lesson_list(call.from_user.id)
			user_lessons_button_list2 = []
			for item in list(reversed(user_lessons_list2)):
				user_lessons_button_list2.append([InlineKeyboardButton(text="["+str(item)[2:12]+"] - ("+str(item)[16:21]+") "+str(item)[-3:-2], callback_data=str(item))])
				k += 1
				if len(user_lessons_list2) == k:
					user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
					user_lessons_button_list2.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_func')])
			if not user_lessons_list2:
				user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
			lessons_user2 = InlineKeyboardMarkup(inline_keyboard=user_lessons_button_list2, row_width=1)
			await call.message.answer(text='♻️', reply_markup=kb_client)
			await call.message.answer(text='Здесь видны ваши активные занятия с учителем\n(которые вы уже загрузили):', reply_markup=lessons_user2)
		else:
			await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='✅', callback_data="got")))
			await sqlite_db.sql_got_les_admin(call.from_user.id)
			id_y = sqlite_db.idusers(call.from_user.id)
			k = 0
			user_lessons_list2 = sqlite_db.sql_lesson_list(id_y[0])
			user_lessons_button_list2 = []
			for item in list(reversed(user_lessons_list2)):
				user_lessons_button_list2.append([InlineKeyboardButton(text="["+str(item)[2:12]+"] - ("+str(item)[16:21]+") "+str(item)[-3:-2], callback_data=str(item))])
				k += 1
				if len(user_lessons_list2) == k:
					user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
					user_lessons_button_list2.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_func')])
					user_lessons_button_list2.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
			if not user_lessons_list2:
				user_lessons_button_list2.append([InlineKeyboardButton(text='Добавить запись >>>', callback_data='Добавить запись >>>')])
				user_lessons_button_list2.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
			lessons_user2 = InlineKeyboardMarkup(inline_keyboard=user_lessons_button_list2, row_width=1)
			await call.message.answer(text='♻️', reply_markup=kb_admin)
			await bot.send_message(chat_id=call.from_user.id, text=f'Вы добавили урок ученику {id_y[1]}!', reply_markup=(lessons_user2))
			await bot.send_message(chat_id=id_y[0], text=f'Учитель добавил вам новый урок!\nЕго можно посмотреть в разделе "Моё расписание".')
	else:
		await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🚫', callback_data="nononono")))
		await call.message.answer(text='Такая дата и время уже заняты, выбери заново!', reply_markup=await SimpleCalendar().start_calendar())
#!хуй


# user panel payment (4)

#проверочная команда
async def command_test(message : types.Message):
	idu = sqlite_db.idprov_user(message.from_user.id)
	await bot.send_message(chat_id=message.from_user.id, text=f'{idu[0]}')




async def command_payment(message : types.Message):
	k = 0
	user_payment_list = sqlite_db.sql_payment_list(message.from_user.id)
	user_payment_button_list = []
	for item in list(reversed(user_payment_list)):						
		user_payment_button_list.append([InlineKeyboardButton(text="{"+str((str(item)[2:-2].split())[1])[1:-1]+" ₽} - ["+str((str(item)[2:-2].split())[2])[:-2]+"] "+str(item)[-3:-2], callback_data=str(item))])
		k += 1
		if len(user_payment_list) == k:
			user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
			user_payment_button_list.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_pay_function')])
	if not user_payment_list:
		user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
	payment_user = InlineKeyboardMarkup(inline_keyboard=user_payment_button_list, row_width=1)
	await message.answer(text='💵', reply_markup=kb_client)
	await message.answer(text='Здесь видны ваши активные оплаты\n(уже внесённые):', reply_markup=payment_user)



#доп функции по оплате
async def dop_pay_function(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='Транзакции 💳', callback_data='oplata_detalno')).add(InlineKeyboardButton(text='Редактировать оплаты ⚙️', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='<<< Назад', callback_data='red_payment_list')))


async def everyone_my_trans_pay(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	idu = sqlite_db.idprov_user(call.from_user.id)
	if idu == 1:
		les_list = sqlite_db.sql_payment_transaction_list(call.from_user.id)
	else:
		les_list = sqlite_db.sql_payment_transaction_list((idu[1])[0])
	if len(les_list) == 0:
		await bot.send_message(chat_id=call.from_user.id, text='У вас нет действующих оплат.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться к моим оплатам 💸', callback_data='red_payment_list')))
	else:
		pay_list = sqlite_db.sql_pay_lists(call.from_user.id)
		ind_cost = str(sqlite_db.ind_cost())[2:-3]
		group_cost = str(sqlite_db.group_cost())[2:-3]
		pay_str = ""
		status_payment = ""
		pay_info = ""
		kk = 1
		count = 0
		for i in les_list:
			if i[3] == 's🟢':
				count = 0
				pay_info = f'Проплачено за: '
				status_payment = 'без остатка ✅'
				prov_tich = 'Проверено учителем ✅'
				for c in pay_list:
						if i[2] == str(c[0])[:-1].split()[2]:
							count += 1
							if count == 1:
								pay_info += f'{str(c[1])}'
							else:
								pay_info += f', {str(c[1])}'
			elif i[3] == 's🟡':
				count = 0
				pay_info = f'Проплачено за: '
				status_payment = f'остаток - {i[1]} ₽'
				prov_tich = 'Проверено учителем ✅'
				if bool(pay_list) is True:
					for c in pay_list:
						if i[2] == str(c[0])[:-1].split()[2]:
							count += 1
							if count == 1:
								pay_info += f'{str(c[1])}'
							else:
								pay_info += f', {str(c[1])}'
				else:			
					pay_info = 'Нет проплаченых уроков'
			else:
				status_payment = 'не оплачено ☑'
				prov_tich = 'Не проверено учителем ☑'
				pay_info = ''
			pay_str += f'\n🔘 Оплата №: {str(kk)}\nДата и взнос: [{str(i[0]).split()[1]}] - ({str(str(i[0]).split()[0])[:-1]} ₽)\nСтатус оплаты: {status_payment}\n{prov_tich}\n{pay_info}\n'
			kk += 1
		await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны все ваши оплаты, \
			\nстоимость одного индивидуального\n занятия - {ind_cost} ₽.\n\
			стоимость одного группового\n занятия - {group_cost} ₽.\nЧтобы посмотреть чек об оплате, \
			\nнажмите на кнопку снизу и \nвпишите номер занятия:\n______________________________________\
			\n{pay_str}', reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text='<<< Назад', callback_data='dop_pay_function'), InlineKeyboardButton(text='Посмотреть чек', callback_data='send_check_payment')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='red_payment_list')))



async def send_check_payment(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	await bot.send_message(chat_id=call.from_user.id, text=f'Чтобы посмотреть чек, который вы загрузили, введите номер урока из прошлого сообщения:', reply_markup=ReplyKeyboardRemove())
	await FSMCheck_pay.sym.set()



async def h_c_send_pay(message: types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		idu = sqlite_db.idprov_user(message.from_user.id)
		if idu[0] == 1:
			les_list = sqlite_db.send_check(message.from_user.id)
		else:
			les_list = sqlite_db.send_check((idu[1])[0])
		if len(les_list) < int(message.text):
			await bot.send_message(chat_id=message.from_user.id, text='Вы ввели число, которого нет в списке, попробуйте еще раз')
		else:
			k = 1
			for i in les_list:
				if int(message.text) == k:
					if idu[0] == 1:
						await bot.send_document(chat_id=message.from_user.id, document=i[0], caption=f'Чек об оплате за {str(i[1]).split()[1]}', reply_markup=kb_client)
					else:
						await bot.send_document(chat_id=message.from_user.id, document=i[0], caption=f'Чек об оплате за {str(i[1]).split()[1]}', reply_markup=kb_admin)
					await state.finish()
					await bot.send_message(chat_id=message.from_user.id, text='Выберите дальнейшее действие:', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться к оплатам 💸', callback_data='red_payment_list')).add(InlineKeyboardButton(text='Вернуться к транзакциям 🧩', callback_data='oplata_detalno')).add(InlineKeyboardButton(text='Вернуться к чекам 📄', callback_data='send_check_payment')))
				k += 1
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите число корректно')


#Редактор оплат
async def payment_list_changer(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='🌀', callback_data="//waiting//")))
	idu = sqlite_db.idprov_user(call.from_user.id)
	if idu[0] == 1:
		les_list = sqlite_db.sql_payment_transaction_list(call.from_user.id)
	else:
		les_list = sqlite_db.sql_payment_transaction_list((idu[1])[0])
	if len(les_list) == 0:
		await bot.send_message(chat_id=call.from_user.id, text='У вас нет действующих оплат.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться к моим оплатам 💸', callback_data='red_payment_list')))
	else:
		pay_list = sqlite_db.sql_pay_lists(call.from_user.id)
		ind_cost = str(sqlite_db.ind_cost())[2:-3]
		group_cost = str(sqlite_db.group_cost())[2:-3]
		pay_str = ""
		status_payment = ""
		pay_info = ""
		kk = 1
		count = 0
		for i in les_list:
			if i[3] == 's🟢':
				count = 0
				pay_info = f'Проплачено за: '
				status_payment = 'без остатка ✅'
				prov_tich = 'Проверено учителем ✅'
				for c in pay_list:
						if i[2] == str(c[0])[:-1].split()[2]:
							count += 1
							if count == 1:
								pay_info += f'{str(c[1])}'
							else:
								pay_info += f', {str(c[1])}'
			elif i[3] == 's🟡':
				count = 0
				pay_info = f'Проплачено за: '
				status_payment = f'остаток - {i[1]} ₽'
				prov_tich = 'Проверено учителем ✅'
				if bool(pay_list) is True:
					for c in pay_list:
						if i[2] == str(c[0])[:-1].split()[2]:
							count += 1
							if count == 1:
								pay_info += f'{str(c[1])}'
							else:
								pay_info += f', {str(c[1])}'
				else:			
					pay_info = 'Нет проплаченых уроков'
			else:
				status_payment = 'не оплачено ☑'
				prov_tich = 'Не проверено учителем ☑'
				pay_info = ''
			pay_str += f'\n🔘 Оплата №: {str(kk)}\nДата и взнос: [{str(i[0]).split()[1]}] - ({str(str(i[0]).split()[0])[:-1]} ₽)\nСтатус оплаты: {status_payment}\n{prov_tich}\n{pay_info}\n'
			kk += 1
		if idu[0] == 1:
			await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны все ваши оплаты, \
				\nчтобы отредактировать взнос или загрузить другой чек, впишите номер занятия:\n______________________________________\
				\n{pay_str}', reply_markup=ReplyKeyboardRemove())
		else:
			await bot.send_message(chat_id=call.from_user.id, text=f'Здесь видны все оплаты ученика {(idu[1])[1]}, \
				\nчтобы отредактировать взнос или загрузить другой чек, впишите номер занятия:\n______________________________________\
				\n{pay_str}', reply_markup=ReplyKeyboardRemove())
		await FSMChangePayw.first.set()
#хуй с оплатами
async def what_is_chenge_payment(message : types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		idu = sqlite_db.idprov_user(message.from_user.id)
		if idu[0] == 1:
			les_list = sqlite_db.sql_payment_transaction_list(message.from_user.id)
			if len(les_list) < int(message.text):
				await bot.send_message(chat_id=message.from_user.id, text='Вы ввели число, которого нет в списке, попробуйте еще раз')
			else:
				k = 1
				for i in les_list:
					if int(message.text) == k:
						await bot.send_message(chat_id=message.from_user.id, text='💴', reply_markup=kb_client)
						if i[3] != 's🔴':
							await bot.send_document(chat_id=message.from_user.id, document=i[2], caption=f'Чек об оплате за {str(i[0]).split()[1]}, взнос - {str(str(i[0]).split()[0])[:-1]} ₽', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Запрос на изменение', callback_data='zapros_red_pay')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))
						else:
							await bot.send_document(chat_id=message.from_user.id, document=i[2], caption=f'Чек об оплате за {str(i[0]).split()[1]}, взнос - {str(str(i[0]).split()[0])[:-1]} ₽', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Изменить поле "взнос"', callback_data='ch_p_vz')).add(InlineKeyboardButton(text='Изменить прикрепленный чек', callback_data='ch_pr_check')).add(InlineKeyboardButton(text='Удалить запись', callback_data='delete_payment')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))
						await sqlite_db.sql_pooper_poo(message.from_user.id, i)
						await state.finish()
					k += 1
		else:
			les_list = sqlite_db.sql_payment_transaction_list((idu[1])[0])
			if len(les_list) < int(message.text):
				await bot.send_message(chat_id=message.from_user.id, text='Вы ввели число, которого нет в списке, попробуйте еще раз')
			else:
				k = 1
				for i in les_list:
					if int(message.text) == k:
						await bot.send_message(chat_id=message.from_user.id, text='💴', reply_markup=kb_admin)
						await bot.send_document(chat_id=message.from_user.id, document=i[2], caption=f'Чек об оплате за {str(i[0]).split()[1]}, взнос - {str(str(i[0]).split()[0])[:-1]} ₽', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Изменить поле "взнос"', callback_data='ch_p_vz')).add(InlineKeyboardButton(text='Изменить прикрепленный чек', callback_data='ch_pr_check')).add(InlineKeyboardButton(text='Удалить запись', callback_data='delete_payment')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))
						await sqlite_db.sql_pooper_poo(message.from_user.id, i)
						await state.finish()
					k += 1
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите число корректно')

#запрос на редактирование оплаты

async def zapros_red_pay(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='отправка запроса на изменение...', callback_data='npp')))
	time.sleep(1)
	await bot.send_message(chat_id=call.from_user.id, text='Так как ваша оплата прошла проверку учителя, и скорее всего, уже привязанна к какому-то уроку - редактировать эту оплату может только учитель. Напишите какой-то краткий коментарий или обговорите с учителем лично, какая у вас проблема:', reply_markup=ReplyKeyboardRemove())
	await FSMzapros_red_pay.zapros.set()

async def FSMzapros(message: types.Message, state: FSMContext):
	red = sqlite_db.info_red_payp(message.from_user.id)
	await bot.send_message(chat_id=int(str(red[0])[2:-3]), text=f'Вам пришел новый запрос на редактирование оплаты от пользователя = {str(red[2])[2:-3]}\n.\nИнформация об оплате (взнос и дата): {str(red[1])[2:-3]}\n.\nКоментарий ученика: "{message.text}"', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Все запросы', callback_data='zaprosymoi')))
	await state.finish()
	await bot.send_message(chat_id=message.from_user.id, text='Вы успешно отправили запрос!', reply_markup=kb_client)


#удалить запись если она не проверена учителем
async def delete_payment(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идёт редактирование оплаты...', callback_data='npp')))
	await bot.send_message(chat_id=call.from_user.id, text='Вы действительно хотите удалить запись об оплате?', reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text='Да, уверен', callback_data='yes_i_did_it_delete_payment'), InlineKeyboardButton(text='Отмена', callback_data='everyone_lesson_red_payments')))


async def yes_i_did_it_delete_payment(call):
	red = sqlite_db.sql_delete_payment_xianzai(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Оплата за {str(red)[-10:]} успешно удалена!', callback_data='npp')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))


#изменить поле взнос
async def ch_p_vz(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет редактирование оплаты...', callback_data='npp')))
	await bot.send_message(chat_id=call.from_user.id, text='Чтобы обновить поле взнос - впишите сюда новое значение (только цифрами):', reply_markup=ReplyKeyboardRemove())
	await FSMch_p_vz.vznos.set()

async def vznos_new(message: types.Message, state: FSMContext):
	red = sqlite_db.send_admin_change_time(message.from_user.id) 
	if str(message.text).isdigit() == True:
		await bot.send_message(chat_id=f'{int(str(red[2])[2:-3])}', text=f'Пользователь - {str(red[1])[2:-3]} \nизменил сумму оплаченную за урок \nс ({str(str(red[0])[2:-3].split()[0])[:-2]}) на ({message.text})\nДата оплаты - ({str(str(red[0])[2:].split()[1])[1:-2]})') 
		await sqlite_db.vznos_new(message.from_user.id, message.text)
		await bot.send_message(chat_id=message.from_user.id, text=f'Вы успешно обновили сумму оплаченную за урок!\nТеперь ваш взнос = {message.text} ₽', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Изменить поле "взнос"', callback_data='ch_p_vz')).add(InlineKeyboardButton(text='Изменить прикрепленный чек', callback_data='ch_pr_check')).add(InlineKeyboardButton(text='Удалить запись', callback_data='delete_payment')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))
		await state.finish()
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Введите сумму корректно (пример - "1500"):')


#изменить прикрепленный чек
async def ch_pr_check(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет редактирование оплаты...', callback_data='npp')))
	await bot.send_message(chat_id=call.from_user.id, text='Чтобы обновить прикрепленный к этой оплате чек - пришлите новый в ответ на это сообщение:', reply_markup=ReplyKeyboardRemove())
	await FSMch_pr_check.check.set()

async def check_new(message: types.Message, state: FSMContext):
	await bot.send_message(chat_id=message.from_user.id, text='Ваша оплата теперь выглядит вот так:')
	doc = message.document.file_id
	time.sleep(1)
	await bot.send_document(chat_id=message.from_user.id, document=doc, caption=f'Взнос и дата: {str(sqlite_db.obnov_check(message.from_user.id, message.document.file_id))[2:-3]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Изменить поле "взнос"', callback_data='ch_p_vz')).add(InlineKeyboardButton(text='Изменить прикрепленный чек', callback_data='ch_pr_check')).add(InlineKeyboardButton(text='Удалить запись', callback_data='delete_payment')).add(InlineKeyboardButton(text='<<< Назад', callback_data='everyone_lesson_red_payments')).add(InlineKeyboardButton(text='Вернуться в "Дополнительно 🧩"', callback_data='dop_pay_function')).add(InlineKeyboardButton(text='Вернуться в "Мои оплаты 💸"', callback_data='exelent_payment')))
	await state.finish()




#Добавление оплаты
async def callback_payment_user(call):
	await sqlite_db.bezop_dob_les(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='идет добавление оплаты...', callback_data='npp')))
	await bot.send_message(chat_id=call.from_user.id, text='Перешлите сюда чек из онлайн банка\n(согласно инструкции):', reply_markup=ReplyKeyboardRemove())
	await FSMPayment_new.symma.set()

async def payment_sum_sbor_and_next(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
		data['name'] = message.document.file_id
	await FSMPayment_new.next()
	await bot.send_message(chat_id=message.from_user.id, text='Теперь введите сумму которую перевели учителю:')

async def check_payment_user(message : types.Message, state: FSMContext):
	if str(message.text).isdigit() == True:
		async with state.proxy() as data:
			data['clock'] = message.text
			data['callendar'] = f'{message.text}, {now.strftime("%d/%m/%Y")}'
			data['status_sum'] = 's🔴'
		await sqlite_db.new_payment_red(state)
		await state.finish()
		await bot.send_message(chat_id=message.from_user.id, text='Вы успешно внесли оплату!', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Завершить', callback_data="exelent_payment")))
	else: 
		await message.answer(text='Введите данные корректно - |только цифры|:')



#дабл список оплат
async def double_payment_list(call):
	if sqlite_db.prov_user(call.from_user.id) == 1:
		await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='✅', callback_data='comlete_payment')))
		k = 0
		count_dpl = int(str(sqlite_db.sql_sum_dnt_pay_les(call.from_user.id))[1:-2])
		if count_dpl > 0:
			all_payment = sqlite_db.sql_auto_pay(call.from_user.id)
			ind_c = int(str(all_payment[0])[2:-3])
			gr_c = int(str(all_payment[1])[2:-3])
			ost = int(str(all_payment[2])[1:-2])
			while ost >= (ind_c or gr_c):
				if ind_c <= ost:
					sqlite_db.sql_solopay_ind(call.from_user.id)
					ost -= ind_c
				else:
					ost = 0
		user_payment_list = sqlite_db.sql_payment_list(call.from_user.id)
		user_payment_button_list = []
		for item in list(reversed(user_payment_list)):
			user_payment_button_list.append([InlineKeyboardButton(text="{"+str((str(item)[2:-2].split())[1])[1:-1]+" ₽} - ["+str((str(item)[2:-2].split())[2])[:-2]+"] "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_payment_list) == k:
				user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
				user_payment_button_list.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_pay_function')])
		if not user_payment_list:
			user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
		payment_user = InlineKeyboardMarkup(inline_keyboard=user_payment_button_list, row_width=1)
		await call.message.answer(text='Здесь видны ваши активные оплаты\n(уже внесённые):', reply_markup=payment_user)
	else:
		#await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='💸', callback_data='nnpp')))
		id_y = sqlite_db.idusers(call.from_user.id)
		k = 0
		user_payment_list = sqlite_db.sql_payment_list(id_y[0])
		user_payment_button_list = []
		for item in list(reversed(user_payment_list)):
			user_payment_button_list.append([InlineKeyboardButton(text="{"+str((str(item)[2:-2].split())[1])[1:-1]+" ₽} - ["+str((str(item)[2:-2].split())[2])[:-2]+"] "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_payment_list) == k:
				user_payment_button_list.append([InlineKeyboardButton(text='Проверить оплаты >>>', callback_data='Проверить оплаты >>>')])
				user_payment_button_list.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_pay_function')])
				user_payment_button_list.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		if not user_payment_list:
			user_payment_button_list.append([InlineKeyboardButton(text='У этого ученика пока нет активных оплат', callback_data='nnpp')])
			user_payment_button_list.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		payment_user = InlineKeyboardMarkup(inline_keyboard=user_payment_button_list, row_width=1)
		#await call.message.answer(text=f'Здесь видны активные оплаты (уже внесённые):\nученика - {id_y[1]}', reply_markup=payment_user)
		await call.message.edit_reply_markup(payment_user)



async def nazadadminlists(call):
	id_y = sqlite_db.idusers(call.from_user.id)
	await call.message.edit_reply_markup(choise_user_keyboard)
	#await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data='nnpp')))
	#await bot.send_message(chat_id=call.from_user.id, text=f'Вы выбрали ученика - {id_y[1]}, \nBыберите дальнейшие действия c ним:', reply_markup=choise_user_keyboard)
#хуй!


#для редактора список оплат
async def red_payment_list(call):
	idu = sqlite_db.idprov_user(call.from_user.id)
	if idu[0] == 1:
		k = 0
		count_dpl = int(str(sqlite_db.sql_sum_dnt_pay_les(call.from_user.id))[1:-2])
		if count_dpl > 0:
			all_payment = sqlite_db.sql_auto_pay(call.from_user.id)
			ind_c = int(str(all_payment[0])[2:-3])
			gr_c = int(str(all_payment[1])[2:-3])
			ost = int(str(all_payment[2])[1:-2])
			while ost >= (ind_c or gr_c):
				if ind_c <= ost:
					sqlite_db.sql_solopay_ind(call.from_user.id)
					ost -= ind_c
				else:
					ost = 0
		user_payment_list = sqlite_db.sql_payment_list(call.from_user.id)
		user_payment_button_list = []
		for item in list(reversed(user_payment_list)):
			user_payment_button_list.append([InlineKeyboardButton(text="{"+str((str(item)[2:-2].split())[1])[1:-1]+" ₽} - ["+str((str(item)[2:-2].split())[2])[:-2]+"] "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_payment_list) == k:
				user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
				user_payment_button_list.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_pay_function')])
		if not user_payment_list:
			user_payment_button_list.append([InlineKeyboardButton(text='Добавить оплату >>>', callback_data='Добавить оплату >>>')])
		payment_user = InlineKeyboardMarkup(inline_keyboard=user_payment_button_list, row_width=1)
		await call.message.edit_reply_markup(payment_user)
	else:
		k = 0
		user_payment_list = sqlite_db.sql_payment_list((idu[1])[0])
		user_payment_button_list = []
		for item in list(reversed(user_payment_list)):
			user_payment_button_list.append([InlineKeyboardButton(text="{"+str((str(item)[2:-2].split())[1])[1:-1]+" ₽} - ["+str((str(item)[2:-2].split())[2])[:-2]+"] "+str(item)[-3:-2], callback_data=str(item))])
			k += 1
			if len(user_payment_list) == k:
				user_payment_button_list.append([InlineKeyboardButton(text='Проверить оплаты >>>', callback_data='Проверить оплаты >>>')])
				user_payment_button_list.append([InlineKeyboardButton(text='Дополнительно 🧩', callback_data='dop_pay_function')])
				user_payment_button_list.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		if not user_payment_list:
			user_payment_button_list.append([InlineKeyboardButton(text='У этого ученика пока нет активных оплат', callback_data='nnpp')])
			user_payment_button_list.append([InlineKeyboardButton(text='<<< Назад', callback_data='nazadadminlists')])
		payment_user = InlineKeyboardMarkup(inline_keyboard=user_payment_button_list, row_width=1)
		await call.message.edit_reply_markup(payment_user)


#helpers

#добавление картинок
async def command_pic(message : types.Message):
	if sqlite_db.sql_adm_check(message.from_user.id) == 1:
		await message.reply(text=f'загрузите картинку:'#, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='загрузить картинку', callback_data="download_1_pic")))
			)
		await FSMPic1.status_sum.set()
	else:
		await message.reply(text='у вас недостаточно прав для вызова этой команды...')

async def load_photo(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = '0'
		data['name'] = '0'
		data['clock'] = '01A'
		data['callendar'] = '0'
		data['status_sum'] = message.photo[0].file_id
	await sqlite_db.sql_add_pic(state)
	await state.finish()
	await message.reply('картинка загружена!')


#статус админа
async def admin_status(message : types.Message):
	if sqlite_db.sql_prov_reg(message.from_user.id) == '':
		await bot.send_message(message.from_user.id, text='К сожалению, вы не зарегистрированы :(', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Регистрация', callback_data="registration")))
	else:
		await message.reply(text='Чтобы изменить статус администратора - введите пароль:')
		await FSMAdmstat.status_sum.set()


async def try_admin_status(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
	await state.finish()
	if message.text == 'admin password12':
		await bot.send_message(chat_id=message.from_user.id, text='Вы успешно вошли в админ панель, выберите режим, в котором хотите находиться.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Войти в режим администратора', callback_data="join_admin")).add(InlineKeyboardButton(text='Войти в режим пользователя', callback_data="join_user")))
	else:
		await bot.send_message(chat_id=message.from_user.id, text='Пароль неправильный, попробуйте ввести его заново нажав сюда - /set_admin_status')


async def callback_admin_status_join(call):
	await sqlite_db.sql_chenge_stat_adm(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='Войти со статусом администратора', callback_data="join")))


async def callback_user_status_join(call):
	await sqlite_db.sql_chenge_stat_user(call.from_user.id)
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='Войти со статусом пользователя', callback_data="join")))

#добавить стоимость занятия
async def add_pay_command(message : types.Message):
	if sqlite_db.sql_adm_check(message.from_user.id) == 1:
		await message.answer(text='Укажите стоимость одного занятия:')
		await FSMPay_cost.cost.set()
	else:
		await message.answer(text='У вас недостаточно прав для использования этой функции')

async def add_pay_answer(message : types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = 'individual cost'
		data['name'] = '0'
		data['clock'] = message.text
		data['callendar'] = '0'
		data['status_sum'] = '💎'
	await sqlite_db.sql_add_ind_cost(state)
	await state.finish()
	await message.answer(text=f'Теперь стоимость одного индивидуального урока - {str(sqlite_db.ind_cost())[2:-3]} ₽')


#добавить стоимость занятия групповое
async def add_pay_group_command(message : types.Message):
	if sqlite_db.sql_adm_check(message.from_user.id) == 1:
		await message.answer(text='Укажите стоимость одного группового занятия:')
		await FSMPay_cost_group.cost.set()
	else:
		await message.answer(text='У вас недостаточно прав для использования этой функции')

async def add_pay_group_answer(message : types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['user_id'] = 'group cost'
		data['name'] = '0'
		data['clock'] = message.text
		data['callendar'] = '0'
		data['status_sum'] = '💰'
	await sqlite_db.sql_add_group_cost(state)
	await state.finish()
	await message.answer(text=f'Теперь стоимость одного группового урока - {str(sqlite_db.group_cost())[2:-3]} ₽')


#reg handlers

def register_handlers_client(dp : Dispatcher):

#test
	dp.register_message_handler(command_test, commands='test')

#(1)

	dp.register_message_handler(commands_start, commands=['start', 'help'])
	dp.register_callback_query_handler(callback_registr, lambda c: c.data == 'registration')
	dp.register_message_handler(load_name, state=FSMReg.name)
	dp.register_callback_query_handler(callback_join, lambda c: c.data == 'join')
	dp.register_callback_query_handler(callback_change_name, lambda c: c.data == 'change_name')
	dp.register_callback_query_handler(callback_yver_change_name, lambda c: c.data == 'yes_change')
#(2)#admin
	dp.register_message_handler(my_students, lambda message: message.text == "Мои ученики 🎓")
	dp.register_callback_query_handler(clon_my_students, lambda c: c.data == 'clon_my_students')
	dp.register_callback_query_handler(sled_str_stud_2, lambda c: c.data == 'sled_str_stud_2')
	dp.register_callback_query_handler(sled_str_stud_3, lambda c: c.data == 'sled_str_stud_3')
	dp.register_callback_query_handler(sled_str_stud_4, lambda c: c.data == 'sled_str_stud_4')
	dp.register_callback_query_handler(sled_str_stud_5, lambda c: c.data == 'sled_str_stud_5')

	dp.register_callback_query_handler(sled_stud, lambda c: c.data == 'sled_stud')
	dp.register_message_handler(AdmChoiceYch, state=FSMAdmChoiceYch.user)
	dp.register_callback_query_handler(mess_user_check_adm_panel, lambda c: c.data == 'mess_user_check_adm_panel')
	dp.register_message_handler(AdmMesYch, state=FSMAdmMesYch.user)

	dp.register_callback_query_handler(mess_to_admin, lambda c: c.data == 'mess_to_admin')
	dp.register_message_handler(AnswerAdminMessage, state=FSMAnswerAdminMessage.user)

	dp.register_callback_query_handler(nazadadminlists, lambda c: c.data == 'nazadadminlists')


#(3)
	dp.register_callback_query_handler(change_callendar, lambda call: 'calendar_back' in call.data)

	dp.register_callback_query_handler(dop_func_lesson, lambda call: 'dop_func' in call.data)
	dp.register_callback_query_handler(transaction, lambda call: 'trans' in call.data)

	dp.register_message_handler(my_lessons_command, lambda message: message.text == "Моё расписание 🎓")
	dp.register_callback_query_handler(clon_lesson1, lambda call: 'back_to_lesson' in call.data)
	dp.register_callback_query_handler(new_lesson_user, lambda c: c.data == 'Добавить запись >>>')
	dp.register_callback_query_handler(new_lesson_calendar, simple_cal_callback.filter())
	dp.register_callback_query_handler(look_at_chek, lambda call: 'check_payment_look' in call.data)
	dp.register_message_handler(check_check_kek, state=FSMCheckList.num)
	dp.register_callback_query_handler(redactor_lesson, lambda call: 'redactor_rasp' in call.data)
	dp.register_message_handler(redactor_lesson_num, state=FSMRedactorLes.num)
	#dp.register_callback_query_handler(back_to_dop_into_red, lambda call: 'back_to_dop_into_red' in call.data, state=FSMRedactorLes.num)

	dp.register_callback_query_handler(red_les_cal, lambda c: c.data == 'redact_data_solo_lesson')
	dp.register_callback_query_handler(red_les_cal_an, dialog_cal_callback.filter())
	dp.register_callback_query_handler(red_les_time, lambda c: c.data == 'time_red')
	dp.register_message_handler(red1_les_time_FSM, state=FSMRedTimer.num)
	dp.register_message_handler(red2_timer_last, state=FSMRedTimer.com)


	dp.register_callback_query_handler(cancel_hours, lambda call: 'back_timer' in call.data)

	dp.register_callback_query_handler(next_time_01, lambda call: 'tib1' in call.data)
	dp.register_callback_query_handler(next_time_02, lambda call: 'tib2' in call.data)
	dp.register_callback_query_handler(next_time_03, lambda call: 'tib3' in call.data)
	dp.register_callback_query_handler(next_time_04, lambda call: 'tib4' in call.data)
	dp.register_callback_query_handler(next_time_05, lambda call: 'tib5' in call.data)
	dp.register_callback_query_handler(next_time_06, lambda call: 'tib6' in call.data)
	dp.register_callback_query_handler(next_time_07, lambda call: 'tib7' in call.data)
	dp.register_callback_query_handler(next_time_08, lambda call: 'tib8' in call.data)
	dp.register_callback_query_handler(next_time_09, lambda call: 'tib9' in call.data)
	dp.register_callback_query_handler(Rnext_time_10, lambda call: 'decade_time10' in call.data)
	dp.register_callback_query_handler(Rnext_time_11, lambda call: 'decade_time11' in call.data)
	dp.register_callback_query_handler(Rnext_time_12, lambda call: 'decade_time12' in call.data)
	dp.register_callback_query_handler(Rnext_time_13, lambda call: 'decade_time13' in call.data)
	dp.register_callback_query_handler(Rnext_time_14, lambda call: 'decade_time14' in call.data)
	dp.register_callback_query_handler(Rnext_time_15, lambda call: 'decade_time15' in call.data)
	dp.register_callback_query_handler(Rnext_time_16, lambda call: 'decade_time16' in call.data)
	dp.register_callback_query_handler(Rnext_time_17, lambda call: 'decade_time17' in call.data)
	dp.register_callback_query_handler(Rnext_time_18, lambda call: 'decade_time18' in call.data)
	dp.register_callback_query_handler(Rnext_time_19, lambda call: 'decade_time19' in call.data)
	dp.register_callback_query_handler(next_time_20, lambda call: 'twenty_tis20' in call.data)
	dp.register_callback_query_handler(next_time_21, lambda call: 'twenty_tis21' in call.data)
	dp.register_callback_query_handler(next_time_22, lambda call: 'twenty_tis22' in call.data)
	dp.register_callback_query_handler(next_time_23, lambda call: 'twenty_tis23' in call.data)
	dp.register_callback_query_handler(next_time_00, lambda call: 'twenty_tis24' in call.data)

	dp.register_callback_query_handler(change_all_time, lambda call: 'change_all_time' in call.data)

	dp.register_callback_query_handler(next_min, lambda call: 'time_m00' in call.data)
	dp.register_callback_query_handler(next_min2, lambda call: 'time_m05' in call.data)
	dp.register_callback_query_handler(next_min3, lambda call: 'time_m10' in call.data)
	dp.register_callback_query_handler(next_min4, lambda call: 'time_m15' in call.data)
	dp.register_callback_query_handler(next_min5, lambda call: 'time_m20' in call.data)
	dp.register_callback_query_handler(next_min6, lambda call: 'time_m25' in call.data)
	dp.register_callback_query_handler(next_min7, lambda call: 'time_m30' in call.data)
	dp.register_callback_query_handler(next_min8, lambda call: 'time_m35' in call.data)
	dp.register_callback_query_handler(next_min9, lambda call: 'time_m40' in call.data)
	dp.register_callback_query_handler(next_min10, lambda call: 'time_m45' in call.data)
	dp.register_callback_query_handler(next_min11, lambda call: 'time_m50' in call.data)
	dp.register_callback_query_handler(next_min12, lambda call: 'time_m55' in call.data)

	dp.register_callback_query_handler(callback_gotovo_lesson, lambda call: 'sum_status' in call.data)

#(4)
	dp.register_message_handler(command_payment, lambda message: message.text == "Мои оплаты 💸")
	dp.register_callback_query_handler(callback_payment_user, lambda c: c.data == 'Добавить оплату >>>')
	dp.register_message_handler(payment_sum_sbor_and_next, content_types=['document'], state=FSMPayment_new.symma)
	dp.register_message_handler(check_payment_user, state=FSMPayment_new.file)
	dp.register_callback_query_handler(double_payment_list, lambda c: c.data == 'exelent_payment')
	dp.register_callback_query_handler(dop_pay_function, lambda c: c.data == 'dop_pay_function')
	dp.register_callback_query_handler(red_payment_list, lambda c: c.data == 'red_payment_list')
	dp.register_callback_query_handler(everyone_my_trans_pay, lambda c: c.data == 'oplata_detalno')
	dp.register_callback_query_handler(send_check_payment, lambda c: c.data == 'send_check_payment')
	dp.register_message_handler(h_c_send_pay, state=FSMCheck_pay.sym)
	dp.register_callback_query_handler(payment_list_changer, lambda c: c.data == 'everyone_lesson_red_payments')
	dp.register_message_handler(what_is_chenge_payment, state=FSMChangePayw.first)
	dp.register_callback_query_handler(ch_p_vz, lambda c: c.data == 'ch_p_vz')
	dp.register_message_handler(vznos_new, state=FSMch_p_vz.vznos)
	dp.register_callback_query_handler(ch_pr_check, lambda c: c.data == 'ch_pr_check')
	dp.register_message_handler(check_new, content_types=['document'], state=FSMch_pr_check.check)
	dp.register_callback_query_handler(zapros_red_pay, lambda c: c.data == 'zapros_red_pay')
	dp.register_message_handler(FSMzapros, state=FSMzapros_red_pay.zapros)
	dp.register_callback_query_handler(delete_payment, lambda c: c.data == 'delete_payment')
	dp.register_callback_query_handler(yes_i_did_it_delete_payment, lambda c: c.data == 'yes_i_did_it_delete_payment')

#helpers

#добавление картинок
	dp.register_message_handler(command_pic, commands='add_pic1')
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMPic1.status_sum)
#статус админа
	dp.register_message_handler(admin_status, commands='set_admin_status')
	dp.register_message_handler(try_admin_status, state=FSMAdmstat.status_sum)
	dp.register_callback_query_handler(callback_admin_status_join, lambda c: c.data == 'join_admin')
	dp.register_callback_query_handler(callback_user_status_join, lambda c: c.data == 'join_user')
#добавить стоимость занятий
	dp.register_message_handler(add_pay_command, commands='set_cost')
	dp.register_message_handler(add_pay_answer, state=FSMPay_cost.cost)

	dp.register_message_handler(add_pay_group_command, commands='set_group_cost')
	dp.register_message_handler(add_pay_group_answer, state=FSMPay_cost_group.cost)
