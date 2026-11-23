# Worked examples: good and bad tests

Python with `pytest`-style asserts, for illustration only. The same shapes hold in any language;
write the real tests in the target repository's framework.

## Behaviour, not implementation

The behaviour under test: an invoice can be paid in full.

Coupled to the implementation:

```python
def test_pay_calls_ledger_record(mocker):
    ledger = mocker.patch("billing.invoice._ledger")
    pay(invoice, amount=120)
    ledger.record.assert_called_once_with(invoice.id, 120)
```

It mocks a module the project owns, and asserts how `pay` does its work. Rename `_ledger`, batch
the writes, or move the record call, and the test goes red while every invoice still pays
correctly.

Through the interface:

```python
def test_paying_the_full_amount_settles_the_invoice():
    invoice = new_invoice(total=120)
    pay(invoice, amount=120)
    assert balance_of(invoice) == 0
    assert status_of(invoice) == "settled"
```

It names *what* the caller gets, uses only public functions, and survives any refactor that keeps
that promise.

## Verify through the interface, not a side channel

```python
# Side channel: reads the table the code happens to write today.
def test_register_inserts_row(db):
    register(email="ada@example.com")
    assert db.execute("select count(*) from users").fetchone()[0] == 1

# Interface: reads back the way a caller would.
def test_registered_user_can_be_found():
    user = register(email="ada@example.com")
    assert find_user(user.id).email == "ada@example.com"
```

## A literal, not a tautology

```python
# Tautology: the expected value is computed the way the code computes it.
def test_shipping_cost():
    weight = 3.5
    assert shipping_cost(weight) == BASE_FEE + weight * RATE_PER_KG

# Literal: the expected value was worked out by hand from the published rate card.
def test_shipping_cost_for_three_and_a_half_kilos():
    assert shipping_cost(3.5) == Decimal("11.75")
```

If `RATE_PER_KG` is wrong, the first test is wrong in the same way and still passes. The second
fails, because its number came from somewhere else.

## Mock a boundary, not a collaborator

Boundaries worth substituting: an external service, the clock, a random source, and sometimes the
filesystem or a database (prefer a real test database when one is cheap). Everything the project
owns runs for real.

```python
# Internal mock: replaces the project's own pricing rules, so the test checks nothing.
def test_quote(mocker):
    mocker.patch("shop.pricing.apply_discounts", return_value=90)
    assert quote(cart) == 90

# Boundary mock: only the clock is fixed; the pricing rules run for real.
def test_weekend_discount_applies_on_saturday():
    saturday = FixedClock(datetime(2026, 11, 21, 10, 0))
    assert quote(cart_of(total=100), clock=saturday) == 90
```

## Inject the boundary

A dependency built inside the function can only be replaced by patching. Passed in, it can be
replaced by an ordinary argument.

```python
# Hard to substitute: the client is constructed inside.
def send_receipt(order):
    client = MailClient(os.environ["MAIL_KEY"])
    client.send(order.email, render_receipt(order))

# Easy to substitute: the boundary is a parameter.
def send_receipt(order, mailer):
    mailer.send(order.email, render_receipt(order))

def test_receipt_goes_to_the_buyer():
    outbox = RecordingMailer()
    send_receipt(order_for("ada@example.com"), mailer=outbox)
    assert outbox.sent == [("ada@example.com", "Receipt for order 42: 120.00")]
```

Give each boundary operation its own narrow method (`mailer.send`, `payments.charge`) rather than
one generic `request(path, options)`. Each fake then returns one shape, the test setup carries no
branching, and a reader can see which operations the test touches.
