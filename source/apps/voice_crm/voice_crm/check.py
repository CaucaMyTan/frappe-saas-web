import frappe

def fix_permissions():
    doctypes = ["AI Agent", "AI Campaign", "AI Campaign Target"]
    
    for dt in doctypes:
        doc = frappe.get_doc("DocType", dt)
        if not doc.permissions:
            doc.append("permissions", {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 0,
                "cancel": 0,
                "amend": 0
            })
            doc.save(ignore_permissions=True)
            print(f"Added permissions for {dt}")

def check():
    fix_permissions()
    frappe.db.commit()
    print("Permissions fixed")

