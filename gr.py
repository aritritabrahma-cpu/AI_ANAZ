from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from database import db, cursor
import pandas as pd
import os
import time
import requests


AUTH_FILE = r"C:\Users\Admin\OneDrive\Desktop\AI_ANAZ\my_project\auth.json"
BACKEND_URL = "http://127.0.0.1:8000/api/update"
FRONTEND_BACKEND_URL = "http://127.0.0.1:8000/api/frontend"

PAGES = [
    ("Dashboard", "https://staging.guardrail.in/dashboard/home"),
    ("Cloud Server", "https://staging.guardrail.in/dashboard/server/server-list"),
    ("Elastic Load Balancer", "https://staging.guardrail.in/dashboard/elastic-lb/elastic-lb-list"),
    ("Server IP", "https://staging.guardrail.in/dashboard/server/server-details?tabindex=monitoring&id=99516"),
    ("VPC Network", "https://staging.guardrail.in/dashboard/vpc/create-vpc"),
    ("Load Balancer", "https://staging.guardrail.in/dashboard/elb/lb-details?tabindex=monitoring&id=20930&provider=nginx_plus"),
    ("VPC Dashboard", "https://staging.guardrail.in/dashboard/vpc/vpc-network"),
    ("K8s cluster", "https://staging.guardrail.in/dashboard/k8s-cluster/k8s-cluster-list"),
    ("DB Cluster", "https://staging.guardrail.in/dashboard/cluster/cluster-list"),
    ("Autoscale", "https://staging.guardrail.in/dashboard/autoscale/autoscale-list"),
    ("Volume", "https://staging.guardrail.in/dashboard/volume/volume-list"),
    ("Object Storage", "https://staging.guardrail.in/dashboard/bucket/bucket-list"),
    ("Snapshot", "https://staging.guardrail.in/dashboard/snapshot/snapshot-list"),
    ("Email Services", "https://staging.guardrail.in/dashboard/email-services/email-details"),
    ("Domains", "https://staging.guardrail.in/dashboard/domains/domains-list"),
    ("CDN Config", "https://staging.guardrail.in/dashboard/cdn-config/cdn-list"),
    ("Alert Dashboard", "https://staging.guardrail.in/dashboard/alerts/list-view"),
    ("Alert History", "https://staging.guardrail.in/dashboard/alerts/list-view"),
    ("Access", "https://staging.guardrail.in/dashboard/admin/admin-details"),
    ("Capacity", "https://staging.guardrail.in/dashboard/capacity-management/capacity-management-details"),
    ("Billing", "https://staging.guardrail.in/dashboard/capacity-management/capacity-management-details"),
    ("SSL Certificate", "https://staging.guardrail.in/dashboard/ssl-certificate/ssl-certificate-list"),
    ("Risk Action", "https://staging.guardrail.in/dashboard/risk-action/risk-action-list"),
    ("Unallocated Devices", "https://staging.guardrail.in/dashboard/device-inventory/device-inventory-list"),
    ("Ngnix Cluster", "https://staging.guardrail.in/dashboard/device-cluster/clusters-list"),
    ("Devices", "https://staging.guardrail.in/dashboard/device/device-list"),
    ("Zone Cluster", "https://staging.guardrail.in/dashboard/zone-cluster/zone-cluster-list"),
    ("All Networks", "https://staging.guardrail.in/dashboard/all-networks/all-vpc"),
    ("Network Link", "https://staging.guardrail.in/dashboard/network-link/network-list"),
    ("Create Cloud Server", "https://staging.guardrail.in/dashboard/server/create-server"),
    ("Create Bare Metal", "https://staging.guardrail.in/dashboard/bare-metal/create-bare-metal"),
    ("Create Elastic Load Balancer", "https://staging.guardrail.in/dashboard/elastic-lb/create-elb"),
    ("Create Load Balancer", "https://staging.guardrail.in/dashboard/elb/create-lb"),
    ("Create Kubernetes Cluster", "https://staging.guardrail.in/dashboard/k8s-cluster/create"),
    ("Create Database Cluster", "https://staging.guardrail.in/dashboard/cluster/create-cluster"),
    ("Create Autoscale Configuration", "https://staging.guardrail.in/dashboard/autoscale/create-autoscale"),
    ("Create Volume", "https://staging.guardrail.in/dashboard/volume/create-volume"),
    ("Create Object Storage", "https://staging.guardrail.in/dashboard/bucket/create-bucket"),
    ("Create Domain", "https://staging.guardrail.in/dashboard/domains/domains-list"),
    ("Create CDN Config", "https://staging.guardrail.in/dashboard/cdn-config/create-cdn"),
    ("Create Alert Dashboard", "https://staging.guardrail.in/dashboard/alerts/create-dashboard"),
    ("Create Project", "https://staging.guardrail.in/dashboard/admin/admin-details"),
    ("Create Group", "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=groups"),
    ("Zones", "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=zones"),
    ("Access policy", "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=access_policy"),
    ("Create access policy", "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=access_policy"),
    ("Users", "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=users"),
    ("Create Ngnix Cluster", "https://staging.guardrail.in/dashboard/device-cluster/create-cluster"),
    ("Support Center", "https://staging.guardrail.in/dashboard/server/create-server"),
    ("Profile", "https://staging.guardrail.in/dashboard/profile/my-profile"),
    ("User Access", "https://staging.guardrail.in/dashboard/profile/my-profile"),
    ("Group", "https://staging.guardrail.in/dashboard/profile/my-profile"),
]

# ==========================================================
# GLOBAL STATE
# ==========================================================

results = {}
current_page = ""
console_logs = []
failed_requests = []


def handle_console(msg):
    console_logs.append({"type": msg.type, "text": msg.text})


def handle_request_failed(request):
    failed_requests.append(
        {"url": request.url, "method": request.method, "failure": request.failure}
    )


def capture_response(response):
    if "/api/" not in response.url:
        return

    status = response.status

    if status >= 500:
        priority, action, severity = "P2", "Critical Server Error", 3
    elif status >= 400:
        priority, action, severity = "P1", "Immediate Action Required", 2
    else:
        priority, action, severity = "P5", "No Action Needed", 1

    try:
        response_time = round(float(response.timing["responseEnd"]), 2)
    except Exception:
        response_time = 0.0

    key = (current_page, response.url)

    if key not in results or severity > results.get(key, {}).get("Severity", 0):
        results[key] = {
            "Page": current_page,
            "api_url": response.url,
            "status_code": status,
            "priority": priority,
            "action": action,
            "response_time": response_time,
            "Severity": severity,
        }

    # MYSQL INSERT
    try:
        cursor.execute(
            """
            INSERT INTO api_status
            (page_name, api_url, status_code, priority, action, response_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (current_page, response.url, status, priority, action, response_time),
        )
        db.commit()
    except Exception as e:
        print("Database Error :", e)

    # FASTAPI UPDATE
    payload = {
        "page": current_page,
        "api_url": response.url,
        "status": status,
        "priority": priority,
        "response_time": response_time,
        "action": action,
    }

    try:
        requests.post(BACKEND_URL, json=payload, timeout=2)
    except Exception as e:
        print("Backend Error :", e)


def get_active_page(context, current_page_obj, timeout_s=10):
    """
    Some SSO/OTP login flows open the login UI in a NEW browser tab
    instead of navigating the original tab. If that happens, the
    original `page` object never changes URL and login checks fail
    forever, even though you ARE logged in (just in another tab).

    This checks context.pages and returns whichever page is currently
    on a 'dashboard' URL, if any, otherwise falls back to the most
    recently opened page.
    """
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        for p in context.pages:
            try:
                if "dashboard" in p.url.lower():
                    return p
            except Exception:
                continue
        time.sleep(0.5)
    # No dashboard tab found within timeout -> return the last opened tab
    return context.pages[-1] if context.pages else current_page_obj


def wait_for_login(context, page, timeout_s=25, poll_interval=1.0):
    """
    Polls page URL (and any newly opened tabs) for up to `timeout_s`
    seconds looking for 'dashboard' in the URL, instead of checking
    ONCE right when ENTER is pressed. This fixes the false
    'Login not completed' when the SPA redirect is still in flight,
    or when login happened in a separate popup/tab.
    Returns the active Page object if login succeeded, else None.
    """
    deadline = time.time() + timeout_s
    last_seen_url = ""

    while time.time() < deadline:
        # Check every open tab/page in the context, not just the original one
        for p in context.pages:
            try:
                url = p.url.lower()
            except Exception:
                continue
            last_seen_url = url
            if "dashboard" in url:
                return p
        time.sleep(poll_interval)

    print(f"\n[DEBUG] Last URL seen while waiting: {last_seen_url}")
    return None


# ==========================================================
# MAIN
# ==========================================================

with sync_playwright() as p:

    print("=" * 80)
    print("Launching Guardrail Monitoring Engine...")
    print("=" * 80)

    context = p.chromium.launch_persistent_context(
        user_data_dir="playwright_profile",
        headless=False,
        channel="chrome",
        viewport=None,
        args=["--start-maximized"],
    )

    page = context.new_page()
    print("Browser Started Successfully")

    # -------------------- MANUAL LOGIN --------------------
    print("\nPlease login manually.\n")
    page.goto("https://staging.guardrail.in", wait_until="domcontentloaded")

    print("=" * 80)
    print("LOGIN STEPS")
    print("=" * 80)
    print("1. Enter Email")
    print("2. Enter Password")
    print("3. Complete OTP")
    print("4. Wait until Dashboard loads")
    print("5. Press ENTER here")

    input("\nPress ENTER after login...")

    # Instead of a single instant check, poll for up to 25s and also
    # scan every tab in the browser context (handles popup/new-tab logins).
    active_page = wait_for_login(context, page, timeout_s=25, poll_interval=1.0)

    if active_page is None:
        print("\nLogin not completed.")
        print("If you WERE actually logged in, this usually means either:")
        print("  1) The dashboard redirect took longer than 25s, or")
        print("  2) Login opened in a separate tab this script isn't tracking.")
        print("Re-run and wait for the dashboard to fully render before pressing ENTER.")
        context.close()
        exit()

    page = active_page  # make sure we monitor the tab that's actually logged in

    print("\nLogin Successful")
    print("=" * 80)

    page.on("console", handle_console)
    page.on("requestfailed", handle_request_failed)
    page.on("response", capture_response)

    print("\nMonitoring Engine Ready\n")

    try:
        while True:
            results.clear()
            print("\nStarting New Monitoring Cycle...\n")

            for page_name, url in PAGES:
                current_page = page_name
                console_logs.clear()
                failed_requests.clear()

                print("=" * 100)
                print(f"Opening : {page_name}")
                print("=" * 100)

                try:
                    page.goto(url, wait_until="networkidle", timeout=60000)
                except PlaywrightTimeoutError:
                    print("Timeout while opening page.")
                    continue
                except Exception as e:
                    print("Navigation Error :", e)
                    continue

                page.wait_for_timeout(5000)

                # LOGIN CHECK (mid-run session expiry)
                if "login" in page.url.lower():
                    print("\nSession Expired!")
                    print("Please login again.")
                    input("\nAfter login press ENTER...")
                    reauth_page = wait_for_login(context, page, timeout_s=25, poll_interval=1.0)
                    if reauth_page is None:
                        print("\nRe-login not completed. Skipping this page.")
                        continue
                    page = reauth_page
                    page.wait_for_timeout(3000)

                # FRONTEND ELEMENTS
                try:
                    element_counts = page.evaluate(
                        """
                        () => ({
                            buttons: document.querySelectorAll("button").length,
                            tables: document.querySelectorAll("table").length,
                            forms: document.querySelectorAll("form").length,
                            dropdowns: document.querySelectorAll("select").length,
                            images: document.querySelectorAll("img").length,
                            links: document.querySelectorAll("a").length
                        })
                        """
                    )
                except Exception:
                    element_counts = {
                        "buttons": 0, "tables": 0, "forms": 0,
                        "dropdowns": 0, "images": 0, "links": 0,
                    }

                print("\nFrontend Elements")
                print("-------------------------------")
                for key, value in element_counts.items():
                    print(f"{key.capitalize():12}: {value}")

                try:
                    cursor.execute(
                        """
                        INSERT INTO frontend_health
                        (page_name, buttons, tables_found, forms_found, dropdowns, images, links)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            page_name,
                            element_counts["buttons"],
                            element_counts["tables"],
                            element_counts["forms"],
                            element_counts["dropdowns"],
                            element_counts["images"],
                            element_counts["links"],
                        ),
                    )
                    db.commit()
                except Exception as e:
                    print("Frontend DB Error :", e)

                # CONSOLE SUMMARY
                errors, warnings, logs = [], [], []
                for log in console_logs:
                    if log["type"] == "error":
                        errors.append(log)
                    elif log["type"] == "warning":
                        warnings.append(log)
                    else:
                        logs.append(log)

                print("\nConsole Summary")
                print("-------------------------------")
                print("Errors   :", len(errors))
                print("Warnings :", len(warnings))
                print("Logs     :", len(logs))

                if errors:
                    print("\nJavaScript Errors\n")
                    for err in errors:
                        print(err["text"])
                        try:
                            cursor.execute(
                                """
                                INSERT INTO console_logs (page_name, log_type, message)
                                VALUES (%s, %s, %s)
                                """,
                                (page_name, err["type"], err["text"]),
                            )
                        except Exception as e:
                            print(e)
                    try:
                        db.commit()
                    except Exception as e:
                        print("Console DB Commit Error :", e)

                # FAILED NETWORK REQUESTS
                print("\nFailed Network Requests")
                print("-------------------------------")

                if failed_requests:
                    for request in failed_requests:
                        print(f"[{request['method']}]")
                        print(request["url"])
                        print(request["failure"])
                        print("-" * 60)
                        try:
                            cursor.execute(
                                """
                                INSERT INTO failed_requests (page_name, method, url, failure)
                                VALUES (%s, %s, %s, %s)
                                """,
                                (
                                    page_name,
                                    request["method"],
                                    request["url"],
                                    str(request["failure"]),
                                ),
                            )
                        except Exception as e:
                            print(e)
                    try:
                        db.commit()
                    except Exception as e:
                        print("Failed Requests DB Commit Error :", e)
                else:
                    print("No Failed Network Requests")

                # FRONTEND HEALTH SCORE
                health = 100
                if element_counts["buttons"] == 0:
                    health -= 10
                if element_counts["tables"] == 0:
                    health -= 10
                if element_counts["forms"] == 0:
                    health -= 10
                if len(errors) > 0:
                    health -= 20
                if len(failed_requests) > 0:
                    health -= 20
                health = max(0, health)

                print("\nFrontend Health :", health, "/100")

                # SEND FRONTEND HEALTH TO BACKEND
                frontend_payload = {
                    "page": page_name,
                    "frontend_health": health,
                    "console_errors": len(errors),
                    "failed_requests": len(failed_requests),
                }
                try:
                    requests.post(FRONTEND_BACKEND_URL, json=frontend_payload, timeout=2)
                except Exception:
                    pass

                # SCREENSHOT
                try:
                    os.makedirs("screenshots/latest", exist_ok=True)
                    filename = page_name.replace(" ", "_").replace("/", "_").lower() + ".png"
                    page.screenshot(path=f"screenshots/latest/{filename}", full_page=True)
                    print("Screenshot Saved")
                except Exception as e:
                    print("Screenshot Error :", e)

                # PAGE LOAD TIME
                try:
                    metrics = page.evaluate(
                        """
                        () => {
                            const nav = performance.getEntriesByType("navigation")[0];
                            return { load: nav.loadEventEnd, dom: nav.domContentLoadedEventEnd };
                        }
                        """
                    )
                    print("\nLoad Time :", round(metrics["load"], 2), "ms")
                    print("DOM Ready :", round(metrics["dom"], 2), "ms")
                except Exception:
                    pass

                # CLEAR TEMP DATA
                console_logs.clear()
                failed_requests.clear()

                if page_name == "Server IP":
                    page.wait_for_timeout(10000)
                else:
                    page.wait_for_timeout(5000)

            # ---------------- TERMINAL DASHBOARD ----------------
            os.system("cls" if os.name == "nt" else "clear")

            print("=" * 150)
            print("GUARDRAIL LIVE API STATUS DASHBOARD")
            print("=" * 150)

            if results:
                df = pd.DataFrame(results.values())
                df.drop(columns=["Severity"], inplace=True)
                df = df.sort_values(by=["Page", "status_code"], ascending=[True, False])
                print(df.to_string(index=False))
                print()
                print("=" * 150)
                print("Healthy :", len(df[df.priority == "P5"]))
                print("P1 :", len(df[df.priority == "P1"]))
                print("P2 :", len(df[df.priority == "P2"]))
                print("Total :", len(df))
            else:
                print("No API Responses Captured")

            print("\nRefreshing in 10 Seconds...")
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n" + "=" * 80)
        print("Stopping Monitoring...")
        print("=" * 80)

    except Exception as e:
        print("\nUnexpected Error Encountered")
        print(str(e))
        try:
            page.screenshot(path="screenshots/crash.png", full_page=True)
            print("Crash Screenshot Saved")
        except Exception:
            pass

    finally:
        print("\nCleaning Resources...")
        try:
            context.close()
        except Exception:
            pass
        try:
            db.commit()
        except Exception:
            pass
        try:
            db.close()
        except Exception:
            pass
        print("Database Closed")
        print("Browser Closed")
        print("Monitoring Engine Stopped")

# ==========================================================
# END OF MONITOR
# ==========================================================