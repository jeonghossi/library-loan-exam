# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # True/False는 int의 하위 타입이므로 type으로 정확히 확인
    return type(day) is int and day >= 1


class LibraryLoan:
    def __init__(self):
        self.loans = {}            # book_id -> (name, 빌린 날, 반납 기한)
        self.suspensions = {}      # name -> [(정지 시작일, 다시 대출 가능한 날), ...]

    def borrow(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in BOOKS:
            return False
        if not _valid_day(day):
            return False
        if book_id in self.loans:
            return False
        try:
            held = [due for (who, _, due) in self.loans.values() if who == name]
            if len(held) >= MAX_LOANS:
                return False
            if any(day > due for due in held):
                return False
            # 날짜 순서는 검사하지 않음: 정지 기간 안의 날만 막음
            if any(start <= day < end for start, end in self.suspensions.get(name, [])):
                return False
        except TypeError:
            return False
        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in self.loans:
            return -1
        if not _valid_day(day):
            return -1
        who, borrowed_day, due = self.loans[book_id]
        if who != name or day < borrowed_day:
            return -1
        overdue = max(0, day - due)
        del self.loans[book_id]
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 정지. 겹치면 합쳐져서 더 늦게 끝나는 쪽까지 막힘 (기간을 더하지 않음)
            self.suspensions.setdefault(name, []).append((day, day + overdue))
        return overdue

    def get_loans(self, name):
        result = [(book_id, due) for book_id, (who, _, due) in self.loans.items() if who == name]
        result.sort(key=lambda x: (x[1], x[0]))
        return result
