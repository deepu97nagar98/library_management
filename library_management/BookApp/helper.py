from datetime import datetime

def rent_on_book_return(transaction):
	book = transaction.book
	book_fees = book.fee
	current_date = datetime.now().date()

	diff_days = (current_date - transaction.issue_date).days
	amount  = book_fees*diff_days
	return amount

