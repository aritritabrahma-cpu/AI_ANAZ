from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import os
import time
import mysql.connector

# ==============================
# MYSQL CONNECTION
# ==============================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",      # <-- Change this
    database="guardrail_monitor"
)

cursor = db.cursor()

# Create table automatically if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS api_status (

    id INT AUTO_INCREMENT PRIMARY KEY,

    page_name VARCHAR(100),

    api_url TEXT,

    status_code INT,

    priority VARCHAR(10),

    action VARCHAR(100),

    response_time FLOAT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_api(api_url(255))

)
""")

db.commit()

AUTH_FILE = r"C:\Users\Admin\OneDrive\Desktop\AI_ANAZ\my_project\auth.json"

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
            response_time = round(response.timing["responseEnd"], 2)
        except:
            response_time = ""

        key = (current_page, response.url)

        # Keep only highest severity
        if key not in results or severity > results[key]["Severity"]:

            results[key] = {

                "Page": current_page,

                "API URL": response.url,

                "Status Code": status,

                "Priority": priority,

                "Action": action,

                "Response Time (ms)": response_time,

                "Severity": severity

            }

    page.on("response", capture_response)

    print("Starting Live API Monitor...\nPress Ctrl+C to stop.")

    try:

        while True:
                        # Clear previous results
            results.clear()

            # Visit each page
            for page_name, url in PAGES:

                current_page = page_name

                try:
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                except PlaywrightTimeoutError:
                    print(f"Timeout while opening {page_name}")

                # Give APIs time to load
                if page_name == "Server IP":
                    page.wait_for_timeout(10000)
                else:
                    page.wait_for_timeout(5000)

            # Clear terminal
            os.system("cls" if os.name == "nt" else "clear")

            print("=" * 150)
            print("GUARDRAIL LIVE API STATUS DASHBOARD (Refresh: 10 Seconds)")
            print("=" * 150)

            if results:

                df = pd.DataFrame(results.values())

                # Remove helper column
                if "Severity" in df.columns:
                    df.drop(columns=["Severity"], inplace=True)

                # Sort output
                df = df.sort_values(
                    by=["Page", "Status Code"],
                    ascending=[True, False]
                )

                # =====================================
                # SAVE DATA TO MYSQL
                # =====================================

                sql = """
                INSERT INTO api_status
                (
                    page_name,
                    api_url,
                    status_code,
                    priority,
                    action,
                    response_time
                )

                VALUES (%s,%s,%s,%s,%s,%s)

                ON DUPLICATE KEY UPDATE

                    status_code=VALUES(status_code),
                    priority=VALUES(priority),
                    action=VALUES(action),
                    response_time=VALUES(response_time),
                    updated_at=CURRENT_TIMESTAMP
                """

                for _, row in df.iterrows():

                    values = (

                        row["Page"],
                        row["API URL"],
                        int(row["Status Code"]),
                        row["Priority"],
                        row["Action"],
                        row["Response Time (ms)"]

                    )

                    cursor.execute(sql, values)

                db.commit()

                print(df.to_string(index=False))

                print("\n")
                print(f"Total APIs Monitored : {len(df)}")
                print(f"P1 Errors            : {(df['Priority'] == 'P1').sum()}")
                print(f"P2 Errors            : {(df['Priority'] == 'P2').sum()}")

            else:
                print("No API responses captured.")

            print("\nRefreshing in 10 seconds...")
            time.sleep(10)

    except KeyboardInterrupt:

        print("\nMonitoring stopped.")

    finally:

        cursor.close()
        db.close()
        browser.close()