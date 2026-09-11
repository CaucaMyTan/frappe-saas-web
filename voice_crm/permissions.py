import frappe


def get_permission_query_conditions_for_lead(user=None):
	if not user:
		user = frappe.session.user

	roles = frappe.get_roles(user)

	if "Administrator" in roles or "System Manager" in roles or "Sales Manager" in roles:
		return ""

	# Sales User chỉ thấy lead được assign cho mình
	return f"`tabCRM Lead`.`lead_owner` = {frappe.db.escape(user)}"


def auto_assign_lead(doc, method=None):
	"""Round-robin assign lead mới cho Sales User có ít lead nhất."""
	if doc.lead_owner:
		return

	# Lấy danh sách user có role Sales User
	staff_names = frappe.get_all(
		"Has Role",
		filters={"role": "Sales User", "parenttype": "User"},
		pluck="parent",
	)

	if not staff_names:
		return

	# Lọc user đang active
	active_staff = frappe.get_all(
		"User",
		filters={"name": ["in", staff_names], "enabled": 1},
		pluck="name",
	)

	if not active_staff:
		return

	# Đếm số lead đang mở của từng nhân viên
	counts = {}
	for u in active_staff:
		counts[u] = frappe.db.count("CRM Lead", {"lead_owner": u, "converted": 0})

	# Assign cho người có ít nhất
	assigned_to = min(counts, key=counts.get)
	doc.db_set("lead_owner", assigned_to, notify=True)
