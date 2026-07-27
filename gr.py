from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from fastapi import FastAPI
from database import db, cursor
import pandas as pd
import os
import time
import requests




AUTH_FILE = r"C:\Users\Admin\OneDrive\Desktop\AI_ANAZ\my_project\auth.json"
BACKEND_URL = "http://127.0.0.1:8000/api/update"

PAGES = [
    ("Dashboard",
     "https://staging.guardrail.in/dashboard/home"),

    ("Cloud Server",
     "https://staging.guardrail.in/dashboard/server/server-list"),

    ("Elastic Load Balancer",
     "https://staging.guardrail.in/dashboard/elastic-lb/elastic-lb-list"),

    ("Server IP",
     "https://staging.guardrail.in/dashboard/server/server-details?tabindex=monitoring&id=99516"),

    ("VPC Network",
     "https://staging.guardrail.in/dashboard/vpc/create-vpc"),

     ("Load Balancer",
      "https://staging.guardrail.in/dashboard/elb/lb-details?tabindex=monitoring&id=20930&provider=nginx_plus"),

      ("VPC Dashboard",
       "https://staging.guardrail.in/dashboard/vpc/vpc-network"),

       ("K8s cluster",
        "https://staging.guardrail.in/dashboard/k8s-cluster/k8s-cluster-list"),

        ("DB Cluster",
         "https://staging.guardrail.in/dashboard/cluster/cluster-list"),

         ("Autoscale ",
          "https://staging.guardrail.in/dashboard/autoscale/autoscale-list"),

          ("Volume",
           "https://staging.guardrail.in/dashboard/volume/volume-list"),

           ("Object Storage",
            "https://staging.guardrail.in/dashboard/bucket/bucket-list"),

            ("Snapshot",
             "https://staging.guardrail.in/dashboard/snapshot/snapshot-list"),

             ("Email Services",
              "https://staging.guardrail.in/dashboard/email-services/email-details"),

              ("Domains",
               "https://staging.guardrail.in/dashboard/domains/domains-list"),

               ("CDN Config",
                "https://staging.guardrail.in/dashboard/cdn-config/cdn-list"),

                ("Alert Dashboard",
                 "https://staging.guardrail.in/dashboard/alerts/list-view"),

                 ("Alert History",
                  "https://staging.guardrail.in/dashboard/alerts/list-view"),

                  ("Access",
                   "https://staging.guardrail.in/dashboard/admin/admin-details"),

                   ("Capacity",
                    "https://staging.guardrail.in/dashboard/capacity-management/capacity-management-details"),

                    ("Billing",
                     "https://staging.guardrail.in/dashboard/capacity-management/capacity-management-details"),

                     ("SSL Certificate",
                      "https://staging.guardrail.in/dashboard/ssl-certificate/ssl-certificate-list"),

                      ("Risk Action",
                       "https://staging.guardrail.in/dashboard/risk-action/risk-action-list"),

                       ("Unallocated Devices",
                        "https://staging.guardrail.in/dashboard/device-inventory/device-inventory-list"),

                        ("Ngnix Cluster",
                         "https://staging.guardrail.in/dashboard/device-cluster/clusters-list"),

                         ("Devices",
                          "https://staging.guardrail.in/dashboard/device/device-list"),

                          ("Zone Cluster",
                           "https://staging.guardrail.in/dashboard/zone-cluster/zone-cluster-list"),

                           ("All Networks",
                            "https://staging.guardrail.in/dashboard/all-networks/all-vpc"),
                            
                            ("Network Link",
                             "https://staging.guardrail.in/dashboard/network-link/network-list"),

                             ("Create Cloud Server",
                              "https://staging.guardrail.in/dashboard/server/create-server"),

                              ("Create Bare Metal",
                               "https://staging.guardrail.in/dashboard/bare-metal/create-bare-metal"),

                               ("Create Elastic Load Balancer",
                                "https://staging.guardrail.in/dashboard/elastic-lb/create-elb"),

                                ("Create Load Balancer",
                                 "https://staging.guardrail.in/dashboard/elb/create-lb"),

                                 ("Create Kubernetes Cluster",
                                  "https://staging.guardrail.in/dashboard/k8s-cluster/create"),

                                  ("Create Database Cluster",
                                   "https://staging.guardrail.in/dashboard/cluster/create-cluster"),

                                   ("Create Autoscale Configuration",
                                    "https://staging.guardrail.in/dashboard/autoscale/create-autoscale"),

                                    ("Create Volume",
                                     "https://staging.guardrail.in/dashboard/volume/create-volume"),

                                     ("Create Object Storage",
                                      "https://staging.guardrail.in/dashboard/bucket/create-bucket"),

                                      ("Create Domain",
                                       "https://staging.guardrail.in/dashboard/domains/domains-list"),

                                       ("Create CDN Config",
                                        "https://staging.guardrail.in/dashboard/cdn-config/create-cdn"),

                                        ("Create Alert Dashboard",
                                         "https://staging.guardrail.in/dashboard/alerts/create-dashboard"),

                                         ("Create Project",
                                          "https://staging.guardrail.in/dashboard/admin/admin-details"),

                                          ("Create Group",
                                           "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=groups"),

                                           ("Zones",
                                            "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=zones"),

                                            ("Access policy",
                                             "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=access_policy"),

                                             ("Create access policy",
                                              "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=access_policy"),

                                              ("Users",
                                               "https://staging.guardrail.in/dashboard/admin/admin-details?activeTabName=users"),

                                               ("Create Ngnix Cluster",
                                                "https://staging.guardrail.in/dashboard/device-cluster/create-cluster"),

                                                ("Support Center",
                                                 "https://staging.guardrail.in/dashboard/server/create-server"),

                                                 ("Profile",
                                                  "https://staging.guardrail.in/dashboard/profile/my-profile"),

                                                  ("User Access",
                                                   "https://staging.guardrail.in/dashboard/profile/my-profile"),

                                                   ("Group",
                                                    "https://staging.guardrail.in/dashboard/profile/my-profile")
                                                   

]

results = {}

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(storage_state=AUTH_FILE)

    page = context.new_page()

    current_page = ""

    def capture_response(response):
        global current_page

        if "/api/" not in response.url:
            return

        status = response.status

        if status >= 500:
            priority = "P2"
            action = "Critical Server Error"
            severity = 3

        elif status >= 400:
            priority = "P1"
            action = "Immediate Action Required"
            severity = 2

        else:
            priority = "P5"
            action = "No Action Needed"
            severity = 1

        try:
            response_time = round(float(response.timing["responseEnd"]), 2)
        except Exception:
            response_time = 0.0

        key = (current_page, response.url)

        if key not in results or severity > results[key]["Severity"]:
            results[key] = {
                "Page": current_page,
                "api_url": response.url,
                "status_code": status,
                "priority": priority,
                "action": action,
                "response_time": response_time,
                "Severity": severity,
            }

        # -------------------------
        # Save to MySQL
        # -------------------------

        query = """
        INSERT INTO api_status
        (page_name, api_url, status_code, priority, action, response_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            current_page,
            response.url,
            status,
            priority,
            action,
            response_time,
        )

        try:
            cursor.execute(query, values)
            db.commit()

        except Exception as e:
            print(f"Database Error: {e}")

        # -------------------------
        # Send to FastAPI Backend
        # -------------------------

        payload = {
            "page": current_page,
            "api_url": response.url,
            "status": status,
            "priority": priority,
            "response_time": response_time,
            "action": action,
        }

        try:
            r = requests.post(
                BACKEND_URL,
                json=payload,
                timeout=2,
            )

            if r.status_code == 200:
                print(f"✔ Sent -> {response.url}")
            else:
                print(f"Backend returned {r.status_code}")

        except Exception as e:
            print(f"Backend Error: {e}")

    page.on("response", capture_response)

    print("Starting Live API Monitor...\nPress Ctrl+C to stop.")

    try:

        while True:

            results.clear()

            for page_name, url in PAGES:

                current_page = page_name

                try:

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )

                except Exception as e:

                    print(f"{page_name}: {e}")
                    continue

                if page_name == "Server IP":
                    page.wait_for_timeout(10000)
                else:
                    page.wait_for_timeout(5000)

            os.system("cls" if os.name == "nt" else "clear")

            print("=" * 140)
            print("GUARDRAIL LIVE API STATUS DASHBOARD (Refresh: 10 Seconds)")
            print("=" * 140)

            if results:

                df = pd.DataFrame(results.values())

                df.drop(columns=["Severity"], inplace=True)

                df = df.sort_values(
                    by=["Page", "status_code"],
                    ascending=[True, False],
                )

                print(df.to_string(index=False))

            else:
                print("No API responses captured.")

            print("\nRefreshing in 10 seconds...")

            time.sleep(10)

    except KeyboardInterrupt:

        print("\nMonitoring stopped.")

    finally:

        browser.close()