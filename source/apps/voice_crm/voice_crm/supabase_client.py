import frappe
import requests


def get_config():
    doc = frappe.get_doc("Voice CRM Client")
    service_key = ""
    if hasattr(doc, "supabase_service_key"):
        service_key = doc.get_password("supabase_service_key") or doc.supabase_service_key
    return frappe._dict({
        "url": getattr(doc, "supabase_url", ""),
        "key": service_key,
        "tenant_id": getattr(doc, "tenant_id", ""),
        "n8n_url": getattr(doc, "n8n_base_url", ""),
        "retell_api_key": doc.get_password("retell_api_key") if hasattr(doc, "retell_api_key") else "",
    })


def _headers(config):
    return {
        "apikey": config.key,
        "Authorization": f"Bearer {config.key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def sb_get(table, filters=None, fields="*", order=None, limit=100, offset=0):
    config = get_config()
    params = {"select": fields, "limit": limit, "offset": offset}
    params[f"tenant_id"] = f"eq.{config.tenant_id}"
    if filters:
        params.update(filters)
    if order:
        params["order"] = order
    r = requests.get(
        f"{config.url}/rest/v1/{table}",
        headers=_headers(config),
        params=params,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def sb_get_one(table, record_id):
    config = get_config()
    params = {"id": f"eq.{record_id}", "tenant_id": f"eq.{config.tenant_id}", "limit": 1}
    r = requests.get(
        f"{config.url}/rest/v1/{table}",
        headers=_headers(config),
        params=params,
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def sb_post(table, data):
    config = get_config()
    data["tenant_id"] = config.tenant_id
    r = requests.post(
        f"{config.url}/rest/v1/{table}",
        headers=_headers(config),
        json=data,
        timeout=10,
    )
    r.raise_for_status()
    result = r.json()
    return result[0] if isinstance(result, list) and result else result


def sb_patch(table, record_id, data):
    config = get_config()
    r = requests.patch(
        f"{config.url}/rest/v1/{table}",
        headers=_headers(config),
        params={"id": f"eq.{record_id}", "tenant_id": f"eq.{config.tenant_id}"},
        json=data,
        timeout=10,
    )
    r.raise_for_status()
    result = r.json()
    return result[0] if isinstance(result, list) and result else result


def sb_delete(table, record_id):
    config = get_config()
    r = requests.delete(
        f"{config.url}/rest/v1/{table}",
        headers=_headers(config),
        params={"id": f"eq.{record_id}", "tenant_id": f"eq.{config.tenant_id}"},
        timeout=10,
    )
    r.raise_for_status()
    return {"ok": True}


def n8n_trigger(path, payload):
    config = get_config()
    r = requests.post(
        f"{config.n8n_url}/webhook/{path}",
        json=payload,
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def retell_call(from_number, to_number, agent_id, customer_name=""):
    config = get_config()
    api_key = config.retell_api_key
    if not api_key:
        frappe.throw("Retell API Key chưa được cấu hình trong Voice CRM Client")
    phone = to_number if to_number.startswith("+") else "+84" + to_number.lstrip("0")
    r = requests.post(
        "https://api.retellai.com/v2/create-phone-call",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "from_number": from_number,
            "to_number": phone,
            "override_agent_id": agent_id,
            "retell_llm_dynamic_variables": {"customer_name": customer_name},
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()
