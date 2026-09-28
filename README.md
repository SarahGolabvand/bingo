# Dingo

A runnable Django frontend for a bilingual café menu and ordering platform. Dark mode is the default; English and Persian share semantic templates, logical spacing, local fonts, and complete translation catalogs.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
npm run build
python manage.py compilemessages
python manage.py runserver
```

`compilemessages` requires GNU gettext (`brew install gettext` on macOS). No database migration is required for this frontend demo, which uses signed cookie sessions. Frontend scripts and fonts are served locally after the build; no runtime CDN is required.

## Pages

| Route | Page |
| --- | --- |
| `/` | Marketing landing page |
| `/pricing/` | Monthly and annual pricing preview |
| `/login/` | OTP input and cooldown preview |
| `/demo/?table=4` | Interactive customer menu |
| `/demo/invoice/` | Printable demo checkout snapshot |
| `/preview/vendor/` | Merchant dashboard preview |
| `/preview/vendor/menu/` | Availability and price controls preview |
| `/preview/vendor/qr/` | Downloadable table QR codes and printable package |

The menu supports category filtering, focus-trapped modifier dialogs, integer-cent prices, quantity controls, a slide-over cart, and HTMX subtotal updates. Django recalculates prices from its catalog and rejects invalid payloads. Checkout produces a demo invoice; it does not charge or submit a real order. Table QR codes point to this deployment's demo route and retain table context.

The language switch uses Django's CSRF-protected `set_language` form, retaining the path and query string. The demo cart persists in sessionStorage across the resulting navigation. Theme choice persists in localStorage. Currency is explicitly USD in both languages; translation never implies currency conversion. Browser carts must not be treated as price authority.

## Structure and customization

- `templates/base.html` provides language direction, theme state, accessibility skip link, and local script loading.
- `templates/includes/` contains shared header, language form, messages, and footer.
- `templates/public/`, `templates/tenant/`, and `templates/vendor/` separate each audience.
- `static/css/main.css` contains Tailwind directives, design tokens, font declarations, glow effects, and print rules. `app.css` is its generated output.
- `static/js/theme.js`, `cart.js`, and `otp-timer.js` contain their respective Alpine interactions.
- `static/js/qr.js` is bundled into `qr.bundle.js` during the build.
- `locale/{en,fa}/LC_MESSAGES/django.po` contains the UI translations. Compile after editing.
- `apps/frontend/views.py` is a deliberately small demo adapter that can be replaced with the application's authenticated, tenant-aware services.

Run `npm run watch` when changing Tailwind classes. Run `npm run build` after dependencies or QR code source change. Product art and café branding are presentation samples; replace them with merchant-owned photography and identity. Replace the example contact address before publishing.

## Production integration boundary

This is a production-oriented frontend foundation, not a completed multi-tenant commerce backend. The public `/preview/vendor/` pages show sample data and do not grant merchant access. Price and availability changes there are temporary. No SMS is sent, no authentication is granted, and no real subscription is created. The OTP component exposes `start()` for calling only after a successful SMS response in the integrated application; the preview button demonstrates its 60-second timer explicitly.

Before exposing real merchant data:

1. Resolve tenant identity from a trusted hostname/schema mapping and scope every catalog, cart, order, and subscription query to it. Namespace browser storage with that tenant's stable identifier instead of the demo key.
2. Replace preview views with authenticated merchant views and object-level tenant authorization. Persist price/availability updates through CSRF-protected endpoints with server validation. Connect order summary refresh to the real order service.
3. Connect phone login to an SMS service with server-enforced expiry, resend cooldown, verification attempt limits, and session issuance. Client timers are presentation only.
4. Replace signed-cookie demo carts and invoice snapshots with server-side cart/order records, atomic checkout, authoritative tax and modifier rules, payment idempotency, and webhook verification. QR table IDs are display context, not authorization.
5. Supply real plan prices, contact details, item media, and business information. Enable checkout only when its backend is ready.
6. Set `DJANGO_DEBUG=0`, a strong `DJANGO_SECRET_KEY`, and explicit `DJANGO_ALLOWED_HOSTS`; run Django's deployment checks, configure HTTPS and static asset hosting, and use a production WSGI server with `config.wsgi:application`. The development server is not a production server.

## Verification

```sh
python manage.py check
python manage.py test
npm run build
npx playwright install chromium
# In another terminal: python manage.py runserver
npx playwright test
```

Django tests cover both locales, server-side cart pricing, input rejection, invoice snapshots, CSRF, and language context. Browser tests cover persistent themes, modifiers, HTMX totals, checkout, RTL cart restoration, mobile overflow, dialog focus, OTP input, and QR generation.
