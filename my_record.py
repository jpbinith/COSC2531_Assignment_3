# A member can borrow a book multiple times. However, if the member's most recent interaction with a book is a reservation, the displayed number of borrowed days will be 'R' regardless of any previous borrowings. For example, if member M01 borrowed book B01 for 7 days and then made a reservation, it will display 'R'. If, after the reservation, M01 borrows B01 for an additional 4 days, the total displayed borrowed days will be 11.

import sys

class Book:
    def __init__(self, book_id):
        self.__book_id = book_id
        self.__borrowed_records = {}

    @property
    def book_id(self):
        return self.__book_id
    
    @property
    def borrowed_records(self):
        return self.__borrowed_records

    def add_borrow_record(self, member_id, days):
        if (member_id not in self.__borrowed_records):
            self.__borrowed_records[member_id] = []
        self.__borrowed_records[member_id].append(days)

    def display_info(self):
        return f"Book ID: {self.__book_id}, Borrowed Days: {self.__borrowed_days}"

class Member:
    def __init__(self, member_id):
        self.__member_id = member_id

    def display_info(self):
        return f"Member ID: {self.__member_id}"

class Records:
    def __init__(self):
        self.__books = {}
        self.__members = {}
    
    def read_records(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                book_id = parts[0].strip()
                if book_id not in self.__books:
                    self.__books[book_id] = Book(book_id)
                for part in parts[1:]:
                    member_id, days = part.split(':')
                    if member_id not in self.__members:
                        self.__members[member_id] = Member(member_id.strip())
                    self.__books[book_id].add_borrow_record(member_id, days.strip())

    def display_records(self):
        member_ids = sorted(self.__members.keys())
        print("RECORDS")
        print('| ', end='')
        print(f"{'Member IDs':<10}", end='')
        for book_id in sorted(self.__books.keys()):
            print(f" {book_id:>8}", end='')
        print('  |')

        print('-' * (15 + 9 * len(self.__books)))

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

        average_days = total_days / total_books if total_books > 0 else 0

        print("\nRECORDS SUMMARY")
        print(f"There are {total_members} members and {total_books} books.")
        print(f"The average number of borrow days is {average_days:.2f} (days).")

def main():
    if len(sys.argv) != 2:
        print("Usage: python my_record.py <record_file_name>")
        return

    # record_file_name = 'records.txt'
    record_file_name = sys.argv[1]
    records = Records()
    records.read_records(record_file_name)
    records.display_records()

if __name__ == "__main__":
    main()