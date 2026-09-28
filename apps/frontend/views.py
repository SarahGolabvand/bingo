from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _


def products():
    return [
        dict(
            id=1,
            name=_("Velvet latte"),
            description=_("Double espresso, silky steamed milk."),
            price=450,
            category="coffee",
            symbol="☕",
        ),
        dict(
            id=2,
            name=_("Cloud matcha"),
            description=_("Ceremonial matcha, a softer kind of energy."),
            price=520,
            category="matcha",
            symbol="🍵",
        ),
        dict(
            id=3,
            name=_("Midnight cold brew"),
            description=_("Slow-steeped for a smooth chocolate finish."),
            price=400,
            category="coffee",
            symbol="🧊",
        ),
        dict(
            id=4,
            name=_("Butter croissant"),
            description=_("Golden layers, baked fresh every morning."),
            price=320,
            category="bakery",
            symbol="🥐",
        ),
    ]


def landing(request):
    return render(request, "public/landing.html")


def pricing(request):
    return render(request, "public/pricing.html")


def login(request):
    return render(request, "public/auth/login_otp.html")


def menu(request):
    try:
        table = int(request.GET.get("table", request.session.get("demo_table", 4)))
        if not 1 <= table <= 50:
            raise ValueError
    except (ValueError, TypeError):
        table = 4
    request.session["demo_table"] = table
    return render(request, "tenant/menu.html", {"products": products(), "table": table})


def lines(request, key="demo_cart"):
    catalog = {p["id"]: p for p in products()}
    result = []
    for row in request.session.get(key, []):
        p = catalog.get(row["id"])
        if p:
            cents = (
                p["price"]
                + (80 if row["milk"] == "oat" else 0)
                + (100 if row["shot"] else 0)
            )
            result.append(
                {
                    **row,
                    "name": p["name"],
                    "unit": Decimal(cents) / 100,
                    "total": Decimal(cents * row["quantity"]) / 100,
                }
            )
    return result


@require_POST
def cart(request):
    import json

    try:
        raw = json.loads(request.POST.get("cart", "[]"))
        if not isinstance(raw, list) or len(raw) > 50:
            raise ValueError
        clean = []
        for row in raw:
            if type(row.get("id")) is not int or row["id"] not in {
                p["id"] for p in products()
            }:
                raise ValueError
            if type(row.get("quantity")) is not int or not 1 <= row["quantity"] <= 20:
                raise ValueError
            if (
                row.get("milk") not in ["regular", "oat"]
                or type(row.get("shot")) is not bool
                or row.get("sweetness") not in ["none", "normal", "extra"]
            ):
                raise ValueError
            clean.append(
                {k: row[k] for k in ["id", "quantity", "milk", "shot", "sweetness"]}
            )
        request.session["demo_cart"] = clean
    except (ValueError, TypeError, KeyError, AttributeError):
        return HttpResponseBadRequest(_("Invalid cart."))
    rows = lines(request)
    return render(
        request,
        "tenant/cart/_cart_summary.html",
        {"lines": rows, "subtotal": sum((r["total"] for r in rows), Decimal(0))},
    )


@require_POST
def checkout(request):
    if not lines(request):
        return redirect("menu")
    request.session["demo_invoice"] = request.session.get("demo_cart", [])
    request.session["demo_invoice_table"] = request.session.get("demo_table", 4)
    return redirect("invoice")


def invoice(request):
    rows = lines(request, "demo_invoice")
    return render(
        request,
        "tenant/orders/invoice.html",
        {
            "table": request.session.get("demo_invoice_table", 4),
            "lines": rows,
            "subtotal": sum((r["total"] for r in rows), Decimal(0)),
        },
    )


def dashboard(request):
    return render(request, "vendor/dashboard.html")


def manage(request):
    return render(request, "vendor/menu_manage.html", {"products": products()})


def qr(request):
    return render(request, "vendor/qr_codes.html")
