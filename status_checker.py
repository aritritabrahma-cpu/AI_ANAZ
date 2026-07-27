from playwright.sync_api import sync_playwright

URL = input("Enter URL: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="auth.json",
        extra_http_headers={
            "X-Email": "aritrita.brahma@timesinternet.in",
            "X-Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55IjoiVElNRVMgSU5URVJORVQgTFREIiwiZGVwYXJ0bWVudCI6IlN5c3RlbSAmIE5ldHdvcmsgQWRtaW4iLCJkaXNwbGF5TmFtZSI6IkFyaXRyaXRhIEJyYWhtYSIsImRpdmlzaW9uIjpudWxsLCJmdWxsbmFtZSI6IkFyaXRyaXRhIEJyYWhtYSIsIm1vYmlsZSI6IjkzNTQzOTcyMzUiLCJ0aXRsZSI6IkludGVybiIsInVzZXIiOiJhcml0cml0YS5icmFobWEiLCJ1c2VybG9jYXRpb24iOiJUSUwgLSBOT0lEQSIsInVzZXJwcmluY2lwYWxuYW1lIjoiYXJpdHJpdGEuYnJhaG1hQHRpbWVzaW50ZXJuZXQuaW4iLCJlbWFpbCI6ImFyaXRyaXRhLmJyYWhtYUB0aW1lc2ludGVybmV0LmluIiwidXNlcl9pZCI6MTEyNzcsImF2YXRhciI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xJM3dhbFQxNzFXV1R5RWpERGdTenpJTURVNGhNc2JQN0F0ZWw2eWFnTXRnSDZOcW55PXMxMDAiLCJncl9sb2dpbiI6dHJ1ZSwiZXhwIjoxNzg0OTc4ODY3fQ.b6BRzPCicOBiKsf7aJ5zmkbkz4PUKmWyyXJpKoMcroazmCTrUyAQQq86hiXxbxRiCTobtxO9UvN4I-pZ9jYBnWCTPhMNXUayuirKMkxsZi0p-YxOugdULwlyacpYadEWNQpSHXZqszmnpnFwETrHXVCspsZirD26zy_Q9d8_Mhw1wq2jI9IMHuTZu5LoCRzSO5RFVY-KkctXH7wJN2c1LXONM3gHJud4I7EDouaEDmuMCumkV4NtH_lqeiFf_CPmcT8wgiua5DdU_sJaoyI-HxteipjHpSiTGbtyEBzx2EjjenRBKN0g58DmiW_iOtKRNqaT0JioN9V-t4V2zD4kKA"
        }
    )
    page = context.new_page()

    response = page.goto(URL)

    print(response.status)

    browser.close()