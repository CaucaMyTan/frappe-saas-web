import frappe


def get_active_statuses():
	return frappe.get_all("CRM Lead Status", {"type": "Open"}, pluck="name")


def get_assignable_users():
	"""Return unique CRM User emails, excluding system accounts."""
	rows = frappe.get_all(
		"Has Role",
		filters={"role": "CRM User", "parenttype": "User"},
		pluck="parent",
	)
	system_users = {"Administrator", "Guest"}
	return list({u for u in rows if u not in system_users})


def auto_assign_lead_owner(doc):
	"""
	Set doc.lead_owner to the sales user with the fewest active CRM Leads.
	Ties are broken by who was assigned a lead least recently (longest wait).
	Does nothing if lead_owner is already set or no assignable users exist.
	"""
	if doc.lead_owner:
		return

	users = get_assignable_users()
	if not users:
		return

	active_statuses = get_active_statuses()

	counts = {}
	last_assigned = {}

	for user in users:
		counts[user] = frappe.db.count(
			"CRM Lead",
			filters={"lead_owner": user, "status": ["in", active_statuses]} if active_statuses else {"lead_owner": user},
		)
		last = frappe.db.get_value(
			"CRM Lead",
			{"lead_owner": user},
			"creation",
			order_by="creation desc",
		)
		# Users with no leads at all get "oldest possible" date — they go first
		last_assigned[user] = last or "2000-01-01 00:00:00"

	# Primary sort: fewest active leads; tiebreaker: waited longest
	winner = min(users, key=lambda u: (counts[u], last_assigned[u]))
	doc.lead_owner = winner
