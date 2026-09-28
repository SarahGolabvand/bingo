import json
from decimal import Decimal
from django.test import SimpleTestCase, Client
from django.utils import translation


class FrontendTests(SimpleTestCase):
    def test_pages_in_both_locales(self):
        for language, direction in [("en", "ltr"), ("fa", "rtl")]:
            self.client.cookies["django_language"] = language
            for path in [
                "/",
                "/pricing/",
                "/login/",
                "/demo/",
                "/demo/invoice/",
                "/preview/vendor/",
                "/preview/vendor/menu/",
                "/preview/vendor/qr/",
            ]:
                with self.subTest(language=language, path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(
                        response, f'lang="{language}" dir="{direction}"'
                    )
        with translation.override("fa"):
            self.assertEqual(translation.gettext("Add to Cart"), "افزودن به سبد")

    def row(self, **kwargs):
        return dict(
            id=1, quantity=2, milk="oat", shot=True, sweetness="normal", **kwargs
        )

    def test_cart_uses_catalog_prices_and_invoice_snapshot(self):
        response = self.client.post(
            "/demo/cart/", {"cart": json.dumps([self.row(price=1)])}
        )
        self.assertEqual(response.context["subtotal"], Decimal("12.60"))
        self.client.get("/demo/?table=7")
        self.assertRedirects(self.client.post("/demo/checkout/"), "/demo/invoice/")
        self.client.post("/demo/cart/", {"cart": "[]"})
        response = self.client.get("/demo/invoice/")
        self.assertEqual(response.context["subtotal"], Decimal("12.60"))
        self.assertEqual(response.context["table"], 7)

    def test_malformed_cart_is_rejected(self):
        for cart in [
            None,
            {},
            [None],
            [{"id": 999}],
            [{"id": True}],
            [dict(self.row(), quantity=0)],
            [dict(self.row(), quantity=1.5)],
            [dict(self.row(), milk="invalid")],
            [dict(self.row(), shot="true")],
            [self.row()] * 51,
        ]:
            with self.subTest(cart=cart):
                self.assertEqual(
                    self.client.post(
                        "/demo/cart/", {"cart": json.dumps(cart)}
                    ).status_code,
                    400,
                )
        self.assertEqual(self.client.get("/demo/cart/").status_code, 405)
        self.assertRedirects(self.client.post("/demo/checkout/"), "/demo/")

    def test_csrf_and_language_context(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/demo/cart/", {"cart": "[]"}).status_code, 403)
        client.get("/demo/?table=7")
        token = client.cookies["csrftoken"].value
        response = client.post(
            "/i18n/setlang/",
            {"csrfmiddlewaretoken": token, "language": "fa", "next": "/demo/?table=7"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/demo/?table=7")
        self.assertContains(client.get(response.url), 'dir="rtl"')
