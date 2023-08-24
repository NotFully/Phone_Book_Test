import os
import json
from typing import List, Dict, Any


class Phonebook:
    """
    Класс для работы с телефонным справочником.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализация объекта Phonebook.

        :param filename: Имя файла для хранения записей.
        """
        self.filename = filename
        self.records = []
        self.load_records()

    def load_records(self) -> None:
        """
        Загрузка записей из файла.
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                try:
                    self.records = json.load(file)
                except json.JSONDecodeError:
                    self.records = []

    def save_records(self) -> None:
        """
        Сохранение записей в файл.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4, ensure_ascii=False)

    def display_records(self, page_num: int, records_per_page: int) -> None:
        """
        Вывод записей на экран постранично.

        :param page_num: Номер страницы для вывода.
        :param records_per_page: Количество записей на странице.
        """
        start_idx = (page_num - 1) * records_per_page
        end_idx = start_idx + records_per_page

        if not self.records:
            print("Справочник пуст!")
            return

        for idx, record in enumerate(self.records[start_idx:end_idx], start=start_idx + 1):
            print(f"{idx}. {record}")

    def add_record(self, record: Dict[str, Any]) -> None:
        """
        Добавление новой записи в справочник.

        :param record: Словарь с данными записи.
        """
        self.records.append(record)
        self.save_records()

    def edit_record(self, record_idx: int, new_record: Dict[str, Any]) -> None:
        """
        Редактирование существующей записи в справочнике.

        :param record_idx: Индекс записи для редактирования.
        :param new_record: Новые данные записи.
        """
        self.records[record_idx] = new_record
        self.save_records()

    def search_records(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Поиск записей по заданному поисковому запросу.

        :param search_term: Поисковый запрос.
        :return: Список найденных записей.
        """
        found_records = []
        for record in self.records:
            if search_term in json.dumps(record, ensure_ascii=False).lower():
                found_records.append(record)
        return found_records


class PhonebookApp:
    """
    Класс для управления приложением телефонного справочника.
    """

    def __init__(self, phonebook: Phonebook) -> None:
        """
        Инициализация объекта PhonebookApp.

        :param phonebook: Объект Phonebook для работы с записями.
        """
        self.phonebook = phonebook

    def run(self) -> None:
        """
        Запуск основного цикла приложения.
        """
        while True:
            print("\nМеню:")
            print("1. Вывод записей")
            print("2. Добавление записи")
            print("3. Редактирование записи")
            print("4. Поиск записей")
            print("5. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                page_num = int(input("Введите номер страницы: "))
                records_per_page = 5
                self.phonebook.display_records(page_num, records_per_page)
            elif choice == "2":
                new_record = self.input_record_data()
                self.phonebook.add_record(new_record)
                print("Запись добавлена!")
            elif choice == "3":
                record_idx = int(input("Введите номер записи для редактирования: ")) - 1
                if 0 <= record_idx < len(self.phonebook.records):
                    new_record = self.input_record_data()
                    self.phonebook.edit_record(record_idx, new_record)
                    print("Запись обновлена!")
                else:
                    print("Неверный номер записи!")
            elif choice == "4":
                search_term = input("Введите поисковый запрос: ").lower()
                found_records = self.phonebook.search_records(search_term)
                if found_records:
                    print("Результаты поиска:")
                    for idx, record in enumerate(found_records, start=1):
                        print(f"{idx}. {record}")
                else:
                    print("Записи не найдены.")
            elif choice == "5":
                self.phonebook.save_records()
                print("Данные сохранены. До скорых встреч.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def input_record_data(self) -> Dict[str, Any]:
        """
        Ввод данных для новой записи.

        :return: Словарь с данными записи.
        """
        last_name = input("Введите фамилию: ")
        first_name = input("Введите имя: ")
        middle_name = input("Введите отчество: ")
        organization = input("Введите название организации: ")
        work_phone = input("Введите рабочий телефон: ")
        personal_phone = input("Введите личный телефон: ")
        return {
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "organization": organization,
            "work_phone": work_phone,
            "personal_phone": personal_phone
        }


def main() -> None:
    phonebook = Phonebook("phonebook.json")
    app = PhonebookApp(phonebook)
    app.run()


if __name__ == "__main__":
    main()
