# A member can borrow a book multiple times. However, if the member's most recent interaction with a book is a reservation, the displayed number of borrowed days will be 'R' regardless of any previous borrowings. For example, if member M01 borrowed book B01 for 7 days and then made a reservation, it will display 'R'. If, after the reservation, M01 borrows B01 for an additional 4 days, the total displayed borrowed days will be 11.
# If records.txt have a book id that not in books.txt exception raised

import sys

class Book:
    def __init__(self, book_id, name, n_copies, late_charge, n_free_days):
        self.__book_id = book_id
        self.__name = name
        self.__n_copies = n_copies
        self.__late_charge = late_charge
        self.__n_free_days = n_free_days
        self.__borrowed_records = {}

    @property
    def book_id(self):
        return self.__book_id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def n_copies(self):
        return self.__n_copies
    
    @n_copies.setter
    def n_copies(self, n_copies):
        self.__n_copies = n_copies

    @property
    def late_charge(self):
        return self.__late_charge
    
    @late_charge.setter
    def late_charge(self, late_charge):
        self.__late_charge = late_charge

    @property
    def n_free_days(self):
        return self.__n_free_days
    
    @n_free_days.setter
    def n_free_days(self, n_free_days):
        self.__n_free_days = n_free_days
    
    @property
    def borrowed_records(self):
        return self.__borrowed_records

    def add_borrow_record(self, member_id, days):
        if (member_id not in self.__borrowed_records):
            self.__borrowed_records[member_id] = []
        self.__borrowed_records[member_id].append(days)

    def calculate_num_of_borrowing_members(self):
        return len([days for days in self.__borrowed_records.values() if any(char.isdigit() for char in days)])
    
    def calculate_num_of_reservers(self):
        return len([days for days in self.__borrowed_records.values() if days[-1] == 'R'])
    
    def calculate_borrowing_date_ranges(self):
        borrowing_dates = [int(day) for days in self.__borrowed_records.values() for day in days if day.isdigit()]
        return f'{min(borrowing_dates)}-{max(borrowing_dates)}'
    
    def calculate_statistics(self):
        n_borrowing_mem = self.calculate_num_of_borrowing_members()
        n_reserves = self.calculate_num_of_reservers()
        n_borrowing_dates = self.calculate_borrowing_date_ranges()
        
        return {
            'n_borrowing_mem': n_borrowing_mem, 
            'n_reserves': n_reserves, 
            'n_borrowing_dates': n_borrowing_dates
        }

    def display_info(self):
        return f"Book ID: {self.__book_id}, Name: {self.__name}, Number of copies: {self.__n_copies}, Free borrow days: {self.__n_free_days}, Late charge: {self.__late_charge}"

class TextBook(Book):
    __default_n_free_days = 14

    def __init__(self, book_id, name, n_copies, late_charge, n_free_days=None):
        n_free_days = TextBook.__default_n_free_days if n_free_days == None else n_free_days
        super().__init__(book_id, name, n_copies, late_charge, n_free_days)

class FictionBook(Book):
    __default_min_n_free_days = 15

    def __init__(self, book_id, name, n_copies, late_charge, n_free_days):
        if(n_free_days < FictionBook.__default_min_n_free_days):
            raise InvalidFreeDaysForFictionException(f"Fiction book {book_id} {name} must have maximum borrowing days greater than 14")
        super().__init__(book_id, name, n_copies, late_charge, n_free_days)

class Member:
    def __init__(self, member_id, first_name, last_name, dob):
        self.__member_id = member_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__dob = dob

    def display_info(self):
        return f"Member ID: {self.__member_id}, First name: {self.__first_name}, Last name: {self.__last_name}, DOB: {self.__dob}"

class Records:
    def __init__(self):
        self.__books = {}
        self.__members = {}
    
    def read_records(self, record_file_name, book_file_name):

        with open(book_file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                book_id = parts[0].strip()
                name = parts[1].strip()
                book_type = parts[2].strip()
                n_copies = int(parts[3].strip())
                n_free_days = int(parts[4].strip())
                late_charge = float(parts[5].strip())
                
                if book_type == "T":
                    self.__books[book_id] = TextBook(book_id, name, n_copies, late_charge, n_free_days)
                elif book_type == "F":
                    self.__books[book_id] = FictionBook(book_id, name, n_copies, late_charge, n_free_days)

        with open(record_file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                book_id = parts[0].strip()
                if book_id not in self.__books:
                    raise InvalidBookIdException(f'No book with book id {book_id}')
                for part in parts[1:]:
                    member_id, days = part.split(':')
                    if member_id not in self.__members:
                        self.__members[member_id] = Member(member_id.strip())
                    self.__books[book_id].add_borrow_record(member_id, days.strip())

    def display_records(self):
        member_ids = sorted(self.__members.keys())
        print("RECORDS")
        print('-' * 60)
        print('| ', end='')
        print(f"{'Member IDs':<10}", end='')
        for book_id in sorted(self.__books.keys()):
            print(f" {book_id:>8}", end='')
        print('  |')
        print('-' * 60)

        total_books = len(self.__books)
        total_members = len(self.__members)
        total_days = 0

        for member_id in member_ids:
            print(f"| {member_id:<10}", end='')
            for book_id in sorted(self.__books.keys()):
                days = self.__books[book_id].borrowed_records.get(member_id, 'xx')
                if days[-1] == 'R':
                    print(f" {'--':>8}", end='')
                elif days == 'xx':
                    print(f" {days:>8}", end='')
                else:
                    n_days = sum(int(day) for day in days if day.isdigit())
                    total_days += n_days
                    print(f" {n_days:>8}", end='')
            print('  |')
        print('-' * 60)

        average_days = total_days / total_books if total_books > 0 else 0

        print("\nRECORDS SUMMARY")
        print(f"There are {total_members} members and {total_books} books.")
        print(f"The average number of borrow days is {average_days:.2f} (days).\n")

    def display_book_info(self):
        book_information = ''
        book_information += "BOOK INFORMATION\n"
        book_information += ('-' * 103 + '\n')
        book_information += '| '
        book_information += f"{'Book ID':<8} {'Name':<20} {'Type':<10} {'Ncopy':>8} {'Maxday':>8} {'Lcharge':>8} {'Nborrow':>10} {'Nreserve':>10}     {'Range':<6}|\n"
        book_information += ('-' * 103 + '\n')

        most_popular_book = None
        max_borrow_reserve_count = 0
        longest_days_book = None
        longest_days = 0

        for book_id, book in sorted(self.__books.items()):
            stats = book.calculate_statistics()
            book_type = 'Textbook'  if type(book).__name__ == 'TextBook' else 'Fiction'
            book_information += f"| {book.book_id:<8} {book.name:<20} {book_type:<10} {book.n_copies:>8} {book.n_free_days:>8} {book.late_charge:>8.2f} {stats['n_borrowing_mem']:>10} {stats['n_reserves']:>10}     {stats['n_borrowing_dates']:<6}|\n"
            
            borrow_reserve_count = stats['n_borrowing_mem'] + stats['n_reserves']
            if borrow_reserve_count > max_borrow_reserve_count:
                most_popular_book = book
                max_borrow_reserve_count = borrow_reserve_count

            if stats['n_borrowing_dates'] and int(stats['n_borrowing_dates'].split('-')[1]) > longest_days:
                longest_days_book = book
                longest_days = int(stats['n_borrowing_dates'].split('-')[1])
        book_information += ('-' * 103)
        book_information += ('\nBOOK SUMMARY')

        if most_popular_book:
            book_information += f"\nThe most popular book is {most_popular_book.name}.\n"
        if longest_days_book:
            book_information += f"The book {longest_days_book.name} has the longest borrow days ({longest_days} days).\n"
        print(book_information)
        self.write_book_information('reports.txt', book_information)

    # # Write order details to the file
    def write_book_information(self, orders_filename, book_information):
        f = open(orders_filename, "w")
        f.write(book_information)
        f.close()

class InvalidFreeDaysForFictionException(Exception):
    pass

class InvalidBookIdException(Exception):
    pass

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: python my_record.py <record_file_name> <book_file_name>")
    #     return

    record_file_name = 'records.txt'
    # record_file_name = sys.argv[1]
    book_file_name = 'books.txt'
    # book_file_name = sys.argv[2]
    records = Records()
    records.read_records(record_file_name, book_file_name)
    records.display_records()
    records.display_book_info()

if __name__ == "__main__":
    main()