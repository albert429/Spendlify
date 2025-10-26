import datetime
from data_handler import load_transactions

def _parse_date(d):
    if not d:
        return None
    try:
        return datetime.datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        return None

def search_by_date_range(transactions=None, start_date=None, end_date=None):

    if transactions is None:
        transactions = load_transactions()

    s = _parse_date(start_date) if start_date else None
    e = _parse_date(end_date) if end_date else None

    out = []
    for t in transactions:
        td = _parse_date(t.get("date", ""))
        if td is None:
            continue
        if s and td < s:
            continue
        if e and td > e:
            continue
        out.append(t)
    return out

def filter_by_category(transactions=None, category=None):

    if transactions is None:
        transactions = load_transactions()

    if not category:
        return list(transactions)

    cat_lower = category.strip().lower()
    return [t for t in transactions if str(t.get("category", "")).strip().lower() == cat_lower]

def filter_by_amount_range(transactions=None, min_amount=None, max_amount=None):

    if transactions is None:
        transactions = load_transactions()

    out = []
    for t in transactions:
        try:
            amt = float(t.get("amount", 0.0))
        except Exception:
            continue
        if min_amount is not None and amt < min_amount:
            continue
        if max_amount is not None and amt > max_amount:
            continue
        out.append(t)
    return out

def sort_transactions(transactions, sort_by="date", reverse=False):
    def key_fn(t):
        if sort_by == "amount":
            try:
                return float(t.get("amount", 0.0))
            except Exception:
                return 0.0
        if sort_by == "category":
            return str(t.get("category", "")).lower()
        # default: date
        d = _parse_date(t.get("date", ""))
        return d or datetime.date.min

    return sorted(list(transactions), key=key_fn, reverse=reverse)

def search_transactions(username=None, start_date=None, end_date=None,
                        category=None, min_amount=None, max_amount=None,
                        sort_by="date", reverse=False):

    txs = load_transactions()
    if username:
        txs = [t for t in txs if t.get("username") == username]

    if start_date or end_date:
        txs = search_by_date_range(txs, start_date, end_date)

    if category:
        txs = filter_by_category(txs, category)

    if min_amount is not None or max_amount is not None:
        txs = filter_by_amount_range(txs, min_amount, max_amount)

    if sort_by:
        txs = sort_transactions(txs, sort_by=sort_by, reverse=reverse)

    return txs

def run_search(username=None):
    print("🔍 Search & Filter Transactions:")
    start = input("Start date (YYYY-MM-DD, leave empty for none): ").strip() or None
    end = input("End date (YYYY-MM-DD, leave empty for none): ").strip() or None
    category = input("Category (leave empty for none): ").strip() or None
    min_a = input("Min amount (leave empty for none): ").strip() or None
    max_a = input("Max amount (leave empty for none): ").strip() or None
    sort_by = input("Sort by (date/amount/category) [date]: ").strip() or "date"
    reverse = input("Reverse sort? (y/N): ").strip().lower() == 'y'

    min_amount = float(min_a) if min_a else None
    max_amount = float(max_a) if max_a else None

    results = search_transactions(username=username, start_date=start, end_date=end,
                                  category=category, min_amount=min_amount, max_amount=max_amount,
                                  sort_by=sort_by, reverse=reverse)

    print(f"\nFound {len(results)} transactions:\n")
    for t in results:
        print(f"{t.get('id')} | {t.get('date')} | {t.get('amount')} {t.get('currency')} | {t.get('category')} | {t.get('type')}")

def __main__():
    run_search("albert429")