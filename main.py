import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3
from ain import otchet

conn = sqlite3.connect('manicur.sql')
cursor = conn.cursor()


def open_uslugi_window():
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)
    def update_usluga_table():
        # Очищаем текущие данные в таблице
        for row in tree.get_children():
            tree.delete(row)

        # Выполняем SQL-запрос для извлечения данных из таблицы Услуги
        cursor.execute("SELECT Название, Цена FROM Услуги")
        services = cursor.fetchall()

        # Добавляем данные в таблицу
        for service in services:
            tree.insert("", "end", values=service)

    def add_service():
        new_usluga = usluga_list.get()
        new_price = price_list.get()

        if new_usluga and new_price:
            cursor.execute("INSERT INTO Услуги (Название, Цена) VALUES (?, ?)", (new_usluga, new_price))
            # Применяем изменения
            conn.commit()
            update_usluga_table()
            usluga_list.delete(0, tk.END)
            price_list.delete(0, tk.END)

    def delete_usluga():
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)

            # Удаление данных из базы данных
            delete_query = '''
                    DELETE FROM Услуги
                    WHERE Название = ? AND Цена = ?
                '''

            cursor.execute(delete_query, (selected_data[0],selected_data[1]))
            update_usluga_table()
            conn.commit()

    root = tk.Tk()
    root.geometry("470x450")
    root.resizable(False, False)
    frame_left = ttk.Frame(root, style="Gray.TFrame")
    frame_left.pack(side="left", pady=5)

    schedule_button = tk.Button(frame_left, text="Расписание",command=lambda :[okno_zakaza(), root.destroy()],bg="#FFB6C1", width=15, pady=8)
    schedule_button.pack(side="top", pady=5)
    master_button = tk.Button(frame_left, text="Мастера",command=lambda : [open_master_window(),root.destroy()],bg="#FFB6C1", width=15, pady=8)
    master_button.pack(side="top", pady=5)

    services_button = tk.Button(frame_left, text="Услуги", bg="#FFB6C1", width=15, pady=8)
    services_button.pack(side="top", pady=5)

    otchetnost_button = tk.Button(frame_left, text="Отчетность",command = otchet, bg="#FFB6C1", width=15, pady=8)
    otchetnost_button.pack(side="top", pady=5)

    frame_left.configure(style="Gray.TFrame")

    frame_right = ttk.Frame(root, style="Gray.TFrame")
    frame_right.pack(side="right", padx=5, pady=5, fill="both", expand=True)

    nazvanie_okna = ttk.Label(frame_right, text="Услуги", font=("Arial", 16))
    nazvanie_okna.grid(row=0, column=2)

    tree = ttk.Treeview(frame_right, columns=("Service", "Price"), show="headings")
    tree.heading("Service", text="Услуга")
    tree.heading("Price", text="Цена")
    tree.column("Service", width=150)
    tree.column("Price", width=50)
    update_usluga_table()
    tree.grid(row=1, column=0)
    tree.bind('<ButtonRelease-1>', on_tree_select)

    usluga_label = ttk.Label(frame_right, text="Услуга:")
    usluga_label.grid(row=2, column= 0)
    usluga_list = ttk.Entry(frame_right)
    usluga_list.grid(row=3, column= 0)

    price_label = ttk.Label(frame_right, text="Цена:")
    price_label.grid(row=4, column=0)
    price_list = ttk.Entry(frame_right)
    price_list.grid(row=5, column=0, pady=5)

    add_button = ttk.Button(frame_right, text="Добавить", command=add_service)
    add_button.grid(row=6, column=1, pady=5)
    delete_button = ttk.Button(frame_right, text="Удалить", command=delete_usluga)
    delete_button.grid(row=7, column=1, pady=5)

def open_master_window():
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)
    def update_master_table():
        # Очищаем текущие данные в таблице
        for row in tree.get_children():
            tree.delete(row)

        # Выполняем SQL-запрос для извлечения данных из таблицы Master
        cursor.execute("SELECT Full_name FROM Master")
        masters = cursor.fetchall()

        # Добавляем данные в таблицу
        for master in masters:
            tree.insert("", "end", values=master)

    def add_master():
        new_master_name = entry_full_name.get()
        # Выполняем SQL-запрос для добавления нового мастера в таблицу Master
        cursor.execute("INSERT INTO Master (Full_name) VALUES (?)", (new_master_name,))
        # Применяем изменения
        conn.commit()

        # Обновляем данные в таблице
        update_master_table()

        entry_full_name.delete(0, tk.END)

    def delete_master():
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)

            # Удаление данных из базы данных
            delete_query = '''
                    DELETE FROM Master
                    WHERE Full_Name = ? 
                '''

            cursor.execute(delete_query, (selected_data[0],))
            update_master_table()
            conn.commit()

    root = tk.Tk()
    root.geometry("450x450")
    root.resizable(False, False)

    frame_left = ttk.Frame(root, style="Gray.TFrame")
    frame_left.pack(side="left", pady=5)

    # Увеличиваем размер кнопок и уменьшаем расстояние между ними
    schedule_button = tk.Button(frame_left, text="Расписание",command=lambda : [okno_zakaza(), root.destroy()],bg="#FFB6C1", width=15, pady=8)
    schedule_button.pack(side="top", pady=5)

    master_button = tk.Button(frame_left, text="Мастера", bg="#FFB6C1", width=15, pady=8)
    master_button.pack(side="top", pady=5)

    services_button = tk.Button(frame_left, text="Услуги", command=lambda: [open_uslugi_window(), root.destroy()],bg="#FFB6C1", width=15, pady=8)
    services_button.pack(side="top", pady=5)

    otchetnost_button = tk.Button(frame_left, text="Отчетность",command=otchet, bg="#FFB6C1", width=15,pady=8)
    otchetnost_button.pack(side="top", pady=5)

    # Устанавливаем фон фрейма
    frame_left.configure(style="Gray.TFrame")

    frame_right = ttk.Frame(root, style="Gray.TFrame")
    frame_right.pack(side="right", padx=5, pady=5, fill="both", expand=True)

    nazvanie_okna = ttk.Label(frame_right, text="Мастера", font=("Arial", 16))
    nazvanie_okna.grid(row=0, column=2)

    # Создаем таблицу для отображения мастеров
    tree = ttk.Treeview(frame_right, columns=("Full Name",), show="headings")
    tree.heading("Full Name", text="ФИО Мастера" )
    tree.column("Full Name",width=200)
    # Обновляем данные в таблице при запуске программы
    update_master_table()

    tree.grid(row=1, column=1, pady=10)
    tree.bind('<ButtonRelease-1>', on_tree_select)

    label_full_name = ttk.Label(frame_right, text="ФИО Мастера:", style="Pink.TLabel")
    label_full_name.grid(row=2, column=1, pady=5)

    entry_full_name = ttk.Entry(frame_right)
    entry_full_name.grid(row=3, column=1, pady=5)

    add_button = ttk.Button(frame_right, text="Добавить", command=add_master)
    add_button.grid(row=4, column=2, pady=5)

    delete_button = ttk.Button(frame_right, text="Удалить", command=delete_master)
    delete_button.grid(row=5, column=2, pady=5)

def okno_zakaza():
    # Создаем StringVar для отслеживания изменений в поле ввода даты

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)

    def delete_usluga():
        selected_item = tree.selection()
        if selected_item:
            # Получение данных из выбранной строки
            selected_data = tree.item(selected_item)['values']
            print("Выбранная строка:", selected_data)

            # Удаление данных из базы данных
            delete_query = '''
                    DELETE FROM Прием
                    WHERE Код_мастера = ? AND Код_услуги = ? AND Время = ?
                '''

            cursor.execute(delete_query, (selected_data[0], selected_data[1], selected_data[2]))
            update_table()
            conn.commit()

    def add_usluga():
        # Получаем значения из полей
        master_value = master_list.get()
        date_value = data_list.get()
        client_value = client_list.get()
        usluga_value = usluga_list.get()
        time_value = time_list.get()
        number_phone_value = number_phone_list.get()
        price_value = price_list.get()

        # Проверяем, что все поля заполнены
        if master_value and date_value and time_value:
            try:
                # Проверяем, существует ли запись с такими значениями Код_мастера, Дата и Время
                cursor.execute("SELECT COUNT(*) FROM Прием WHERE Код_мастера=? AND Дата=? AND Время=?",
                               (master_value, date_value, time_value))
                count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM Visitors WHERE Full_Name = ?", (client_value,))
                count_visitors = cursor.fetchone()[0]

                if count_visitors == 0:
                    # Запись о клиенте не существует, выполняем вставку
                    cursor.execute("INSERT INTO Visitors (Full_Name) VALUES (?)", (client_value,))
                    # Сохраняем изменения
                    conn.commit()
                    print("Данные о клиенте успешно добавлены в таблицу Visitors")
                else:
                    print("Запись о клиенте уже существует в таблице Visitors")

                if count == 0:
                    # Запись не существует, выполняем вставку
                    cursor.execute(
                        "INSERT INTO Прием (Код_мастера, Дата, ФИО_клиента, Код_услуги, Время, Номер_телефона, Цена) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (master_value, date_value, client_value, usluga_value, time_value, number_phone_value,
                         price_value))
                    # Сохраняем изменения
                    conn.commit()
                    # Обновляем таблицу
                    update_table()

                    # Очищаем поля после вставки данных
                    master_list.set('')
                    date_var.set('')
                    client_list.delete(0, tk.END)
                    usluga_list.set('')
                    data_list.delete(0, tk.END)
                    time_list.delete(0, tk.END)
                    number_phone_list.delete(0, tk.END)
                    price_list.delete(0, tk.END)
                else:
                    print("Запись с такими значениями уже существует")

            except Exception as e:
                print(f"Ошибка при вставке данных: {e}")
        else:
            print("Заполните Код_мастера, Дату и Время перед добавлением данных")




    def validate_date_input(new_value):
        # Функция для валидации и форматирования ввода даты
        try:
            # Пробуем преобразовать введенное значение в формат дд.мм.гг
            formatted_date = datetime.strptime(new_value, "%d.%m.%y").strftime("%d.%m.%y")
            data_list.delete(0, tk.END)  # Очищаем поле
            data_list.insert(0, formatted_date)  # Устанавливаем новое отформатированное значение
        except ValueError:
            # Если ввод не соответствует формату, оставляем текущее значение
            pass

    def update_date_label():
        today_date = datetime.today().strftime("%Y-%m-%d")
        date_label.config(text=f"Дата: {today_date}")

    def update_table():
        # Очищаем текущие данные в таблице
        for item in tree.get_children():
            tree.delete(item)

        # Получаем выбранную дату из виджета Entry
        selected_date = date_var.get()

        if not selected_date:
            # Если выбранная дата пуста, используем текущую дату
            selected_date = today_date

        # Выполняем запрос к базе данных для получения обновленных данных
        cursor.execute(
            "SELECT Код_мастера, Код_услуги, Время, ФИО_клиента, Номер_телефона, Цена FROM Прием WHERE Дата = ?",
            (selected_date,))
        updated_data = cursor.fetchall()

        # Заполняем таблицу обновленными данными
        for item in updated_data:
            tree.insert("", "end", values=item)

    def format_time(entry):
        # Получаем введенный текст
        entry_text = entry.get()

        # Удаляем все символы, кроме цифр
        cleaned_text = ''.join(filter(str.isdigit, entry_text))

        # Добавляем двоеточие между часами и минутами, если есть хотя бы два символа
        if len(cleaned_text) >= 2:
            if len(cleaned_text) == 2:
                cleaned_text += ':00'
            elif len(cleaned_text) == 3:
                cleaned_text = cleaned_text[:2] + ':' + cleaned_text[2] + '0'

        # Обновляем текст в поле ввода
        entry.delete(0, tk.END)
        entry.insert(0, cleaned_text)

    def obnov_price():
        selected_usluga = usluga_list.get().strip('{}')
        print("Выбранная услуга:", selected_usluga)

        for item in usluga_data:
            if item[0] == selected_usluga:
                price = item[1]
                print("Цена:", price)

                # Заполняем поле с ценой
                price_list.delete(0, tk.END)  # Очищаем поле
                price_list.insert(0, price)  # Устанавливаем новое значение
                break

    root = tk.Tk()
    root.geometry("850x500")  # Увеличиваем размер окна
    root.resizable(False, False)  # Запрещаем изменение размеров окна

    date_var = tk.StringVar()

    # Создаем фрейм для кнопок слева
    frame_left = ttk.Frame(root, style="Gray.TFrame")
    frame_left.pack(side="left", pady=1)

    # Добавляем рамку вокруг изображения
    logo_frame = ttk.Frame(frame_left, borderwidth=2, relief="solid")
    logo_frame.pack(side="top")

    logo = ttk.Label(frame_left, text="💅", font=("Arial", 55), background="white")
    logo.pack(side="top", pady = 5)
    # Увеличиваем размер кнопок и уменьшаем расстояние между ними
    schedule_button = tk.Button(frame_left, text="Расписание", bg="#FFB6C1", width=15, pady=8)
    schedule_button.pack(side="top", pady=5)

    master_button = tk.Button(frame_left, text="Мастера", command=lambda: [open_master_window(), root.destroy()],bg="#FFB6C1", width=15, pady=8)
    master_button.pack(side="top", pady=5)

    services_button = tk.Button(frame_left, text="Услуги", command=lambda: [open_uslugi_window(), root.destroy()],
                                bg="#FFB6C1", width=15, pady=8)
    services_button.pack(side="top", pady=5)

    otchetnost_button = tk.Button(frame_left, text="Отчетность", command=otchet, bg="#FFB6C1", width=15, pady=8)
    otchetnost_button.pack(side="top", pady=5)

    # Устанавливаем фон фрейма
    frame_left.configure(style="Gray.TFrame")

    frame_top = ttk.Frame(root, style="Gray.TFrame")
    frame_top.pack(side="top", padx=5, pady=5, fill="both", expand=True)

    # условия для полей снизу
    frame_right = ttk.Frame(root, style="Gray.TFrame")
    frame_right.pack(side="right", padx=5, pady=5, fill="both", expand=True)

    date_label = ttk.Label(frame_top, text="Дата: ", style="Pink.TLabel")
    date_label.grid(row=0, column=0, pady=5, sticky="w")

    # Используем StringVar для связывания значения Entry с переменной
    data_izmenenie = ttk.Entry(frame_top, width=20, state='normal', textvariable=date_var)
    data_izmenenie.grid(row=1, column=0, pady=5, sticky="w")

    # Создаем кнопку для обновления таблицы по введенной дате
    update_button = tk.Button(frame_top, text="Обновить", command=update_table, bg="#FFB6C1", width=7, pady=5)
    update_button.grid(row=1, column=0)

    nazvanie_okna = ttk.Label(frame_top, text="Расписание", font=("Arial", 16))
    nazvanie_okna.grid(row=0, column=0)

    today_date = datetime.now().strftime("%d.%m.%Y")

    query = '''
        SELECT Код_мастера, Код_услуги, Время, ФИО_клиента, Номер_телефона, Цена
        FROM Прием
        WHERE Дата = ?
    '''

    cursor.execute(query, (today_date,))
    data = cursor.fetchall()
    print(data)
    # Создание и настройка виджета Treeview (таблица)
    tree = ttk.Treeview(frame_top, columns=("Код_мастера", "Код_услуги", "Время", "ФИО_клиента", "Номер_телефона", "Цена"), show="headings")
    tree.heading("Код_мастера", text="Мастер")
    tree.heading("Код_услуги", text="Услуга")
    tree.heading("Время", text="Время")
    tree.heading("ФИО_клиента", text="ФИО клиента")
    tree.heading("Номер_телефона", text="Номер телефона")
    tree.heading("Цена", text="Цена")

    # Заполнение таблицы данными из столбцов Код_мастера, Код_услуги, Время
    for item in data:
        tree.insert("", "end", values=item)

    tree.column("Код_мастера", width=150)
    tree.column("Код_услуги", width=150)
    tree.column("Время", width=50)
    tree.column("ФИО_клиента", width=150)
    tree.column("Номер_телефона", width=150)
    tree.column("Цена", width=50)

    tree.grid(row = 3, column=0, pady=5, sticky="nsew")
    tree.bind('<ButtonRelease-1>', on_tree_select)

    master_label = ttk.Label(frame_right, text="Мастер", font=("Arial", 10), style="Pink.TLabel")
    master_label.grid(row=2, column=0, pady=2,padx= 5, sticky="w")

    master_list = ttk.Combobox(frame_right, width=20, state='readonly')
    master_list.grid(row=3, column=0, pady=2, padx=5, sticky="w")
    cursor.execute("SELECT Full_Name FROM Master")
    masters_data = cursor.fetchall()
    master_names = [item[0] for item in masters_data]
    master_list['values'] = master_names

    data_label = ttk.Label(frame_right, text="Дата", font=("Arial", 10), style="Pink.TLabel")
    data_label.grid(row=2, column=1, pady=2, padx= 5, sticky="w")
    data_list = ttk.Entry(frame_right, width=20, state='normal')
    data_list.grid(row=3, column=1, pady=2, padx=5, sticky="w")

    client_label = ttk.Label(frame_right, text="Клиент", font=("Arial", 10), style="Pink.TLabel")
    client_label.grid(row=2, column=2, pady=2, padx = 5, sticky="w")

    client_list = ttk.Entry(frame_right, width=20, state='normal')
    client_list.grid(row=3, column=2, pady=2, padx = 5, sticky="w")

    #второй уровень
    usluga_label = ttk.Label(frame_right,text="Услуга", font=("Arial", 10),style = "Pink.TLabel")
    usluga_label.grid(row = 4, column= 0, pady=2, padx=5, sticky="w")

    usluga_list = ttk.Combobox(frame_right, width=20, state='readonly')
    usluga_list.grid(row= 5, column=0, pady=2, sticky="w")
    cursor.execute("SELECT Название, Цена FROM Услуги")  # Добавляем Цену в запрос
    usluga_data = cursor.fetchall()
    usluga_names = [item[0] for item in usluga_data]
    usluga_list['values'] = usluga_names
    selected_usluga = str(usluga_list.get()).strip('{}')
    usluga_list.bind("<<ComboboxSelected>>", lambda event: obnov_price())

    
    time_label = ttk.Label(frame_right,text="Время", font=("Arial", 10),style = "Pink.TLabel")
    time_label.grid(row = 4, column= 1, pady=2, padx=5, sticky="w")

    time_list = ttk.Entry(frame_right, width=20, state='normal')
    time_list.grid(row= 5, column=1, pady=2, sticky="w")
    time_list.bind('<KeyRelease>', lambda event: format_time(time_list))

    number_phone_label = ttk.Label(frame_right,text="Номер телефона", font=("Arial", 10),style = "Pink.TLabel")
    number_phone_label.grid(row = 4, column = 2, pady=2, padx=5, sticky="w")

    number_phone_list = ttk.Entry(frame_right, width=20, state='normal')
    number_phone_list.grid(row= 5, column=2, pady=2, sticky="w")

    #3 уровень
    price_label = ttk.Label(frame_right,text="Цена", font=("Arial", 10),style = "Pink.TLabel")
    price_label.grid(row = 6, column= 0, pady=2, padx=5, sticky="w")
    price_list = ttk.Entry(frame_right, width=20, state='normal')
    price_list.grid(row=7, column=0, pady=2, sticky="w")

    add_button = ttk.Button(frame_right, text="Добавить", command=add_usluga)
    add_button.grid(row = 7, column= 3, padx=5,sticky="e")

    delete_button = ttk.Button(frame_right, text="Удалить", command=delete_usluga)
    delete_button.grid(row = 7, column= 4, sticky="e")

    update_date_label()
    return root

if __name__ == "__main__":
    root = okno_zakaza()
    root.mainloop()