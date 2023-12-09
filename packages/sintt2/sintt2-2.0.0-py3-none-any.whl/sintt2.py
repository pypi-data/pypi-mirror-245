import os

class true_code:
    def __init__(self):
        self.words = {
            "Demka": self.create_file,
            # Добавьте сюда другие слова и код
        }

    def get_code(self, word):
        func = self.words.get(word, None)
        if func:
            func()

    def create_file(self):
        code = """
import sys
import pyodbc
import os.path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, showerror

# Подключение к БД сервер----------------------------
# server = '192.168.1.231'
# db = 'DatabaseDany'
# user = 'admin'
# pw = '123456'

# try:
#    conn = pyodbc.connect(f'DRIVER={{ODBC driver 17 for SQL Server}}; \
#                      SERVER={server};DATABASE={db}; \
#                      UID={user};PWD={pw}')
#-----------------------------------------


#подлючение через ядро-----------------------------------------
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SINTT\SQLEXPRESS;DATABASE=DemoPy;Trusted_Connection=yes;')

except Exception:
    showerror(title='Ошибка1', message='Нет соединения с базой данных. Работа приложения будет завершена.')
    sys.exit(1)
#-----------------------------------------


# Глобальные переменные
status = ['Найдено товаров', '', 'из', '']
sorting = ''  # ORDER BY Products DESC
filtr = ''  # WHERE Discount>=5 and Discount<15
query = 'SELECT *, price*(100-discount)/100 AS NewPrice FROM Product \
         INNER JOIN Unit ON Product.unit=Unit.unit_id \
         INNER JOIN Prod ON Product.prod=Prod.prod_id \
         INNER JOIN Provider ON Product.provider=Provider.provider_id \
         INNER JOIN Category ON Product.category=Category.category_id'
new_query = f'{query} {filtr} {sorting}'
out = []

# Функции
def data():
    global out, new_query
    try:
        cursor = conn.cursor()
        cursor.execute(new_query)
        out = []
        for row in cursor.fetchall():
            image = row.image if row.image else 'picture.png'
            if not os.path.exists(row.image):
                image='picture.png'
            img1=Image.open(image).resize((45, 45))
            img=ImageTk.PhotoImage(img1)
            tag = 'sale' if row.discount>0 else 'blank'
            if row.discount !=0:
                row.price=''.join([u'обратный слеш u0335{}'.format(c) for c in str(row.price)])
            line = [img, (row.art,row.name,row.unit,row.price,
                            row.NewPrice,row.discount,row.max_discount,
                                row.prod,row.provider_name,row.category_name,
                                    row.amount,row.description), tag]
            out.append(line)
        return out
    except Exception as e:
        showerror(title='Ошибка2', message=f'Произошла ошибка при работе с базой данных: {str(e)}')
        print(f"Подробности ошибки: {str(e)}")
        return out

def update_tree():
    datatree.delete(*datatree.get_children())
    for row in data():
        datatree.insert('', END, open=True, text='',
                        image=row[0], values=row[1], tag=row[2])

def update_status():
    global filtr, status
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM Product {filtr}')
        status[1] = str(cursor.fetchone()[0])
        if status[1] == '0':
            showinfo(title='Информация', message='Товаров не найдено')
        cursor.execute('SELECT COUNT(*) FROM Product ')
        status[3] = str(cursor.fetchone()[0])
        lbl_status.config(text=' '.join(status))
    except Exception:
        showerror(title='Ошибка3', message='Нет соединения с базой данных')

def apply_sort(event):
    global sorting, new_query
    select = cb_sort.get()
    sorting = 'ORDER BY name DESC' if select == 'В обратном порядке' else 'ORDER BY name' if select == 'По алфавиту' else ''
    new_query = f'{query} {filtr} {sorting}'
    update_tree()

def apply_filter(event):
    global filtr, new_query
    select = cb_filtr.get()
    filtr = 'WHERE discount<5' if select == 'Скидка менее 5%' else 'WHERE discount>=5 and discount<15' if select == 'От 5 до 15%' else 'WHERE discount>=15' if select == 'Более 15%' else ''
    new_query = f'{query} {filtr} {sorting}'
    update_tree()
    update_status()

app = Tk()
app.title('Демоэкзамен')
app.geometry('1200x600')
app.minsize(600, 300)

# Фреймы
frame_fs = Frame(app)
frame_status = Frame(app)
frame_data = Frame(app)

# Комбобоксы
lbl_cb_sort = Label(frame_fs, text='Сортировка товаров: ')
cb_sort = ttk.Combobox(frame_fs, values=['Без сортировки', 'По алфавиту', 'В обратном порядке'], state='readonly')
cb_sort.current(0)
lbl_cb_filtr = Label(frame_fs, text=' ' * 20 + 'Фильтрация товаров по скидке: ')
cb_filtr = ttk.Combobox(frame_fs, values=['Без фильтра', 'Скидка менее 5%', 'От 5 до 15%', 'Более 15%'], state='readonly')
cb_filtr.current(0)

lbl_cb_sort.grid(column=0, row=0)
cb_sort.grid(column=1, row=0)
lbl_cb_filtr.grid(column=2, row=0)
cb_filtr.grid(column=3, row=0)

cb_sort.bind("<<ComboboxSelected>>", apply_sort)
cb_filtr.bind("<<ComboboxSelected>>", apply_filter)

lbl_status = Label(frame_status, text='')
lbl_status.pack(fill=BOTH)
update_status()

style = ttk.Style()
style.configure('data.Treeview', rowheight=50)
columns = ['#' + str(i) for i in range(11)]
datatree = ttk.Treeview(frame_data, columns=columns, style='data.Treeview')
datatree.tag_configure('sale', background='#7fff00')
datatree.tag_configure('blank', background='white')
tree = [['#0', 'Изображение', 'center', 50],
        ['#1', 'Артикул', 'e', 50],
        ['#2', 'Название', 'w', 150],
        ['#3', 'Ед.изм.', 'w', 40],
        ['#4', 'Цена', 'e', 40],
        ['#5', 'Новая цена', 'e', 40],
        ['#6', 'Скидка', 'e', 40],
        ['#7', 'Макс.скидка', 'e', 40],
        ['#8', 'Производитель', 'w', 100],
        ['#9', 'Поставщик', 'w', 100],
        ['#10', 'Категория', 'w', 150],
        ['#11', 'Остатки', 'e', 40]]

for c in tree:
    datatree.column(c[0], anchor=c[2], width=c[3])
    datatree.heading(c[0], text=c[1])

update_tree()

datatree.pack(fill=BOTH)
frame_fs.pack(anchor=E, padx=20, pady=10)
frame_status.pack(anchor=W, padx=20)
frame_data.pack(fill=BOTH)

app.mainloop()
"""
        with open(os.path.join(os.getcwd(), 'true_code.txt'), 'w') as f:
            f.write(code)
