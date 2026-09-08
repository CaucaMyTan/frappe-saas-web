import frappe
from frappe import _
import requests

@frappe.whitelist()
def trigger_outbound_call(lead_id, agent_id=None):
    """
    API Kích hoạt cuộc gọi: Nhận lệnh từ giao diện Frappe CRM
    Gửi dữ liệu sang n8n Webhook để n8n gọi Retell AI.
    """
    lead = frappe.get_doc("CRM Lead", lead_id)
    
    # Lấy số điện thoại
    phone_number = lead.mobile_no or lead.phone
    if not phone_number:
        frappe.throw(_("Khách hàng này chưa có số điện thoại."))

    # Lấy Agent mặc định nếu không truyền lên
    if not agent_id:
        agents = frappe.get_all("AI Agent", limit=1)
        if not agents:
            frappe.throw(_("Chưa cấu hình Kịch bản AI (AI Agent) nào trên hệ thống."))
        agent_id = agents[0].name

    ai_agent = frappe.get_doc("AI Agent", agent_id)

    # TODO: Thay thế bằng link Webhook thực tế của n8n
    # host.docker.internal dùng để gọi từ trong Docker ra ngoài localhost của máy tính (nếu cài n8n local)
    N8N_WEBHOOK_URL = "http://host.docker.internal:5678/webhook/trigger-retell-call"
    
    payload = {
        "lead_id": lead.name,
        "customer_name": lead.first_name or lead.lead_name,
        "phone_number": phone_number,
        "retell_agent_id": ai_agent.retell_agent_id
    }

    try:
        # Gửi request sang n8n
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        frappe.msgprint(_("Đã gửi lệnh gọi tới n8n thành công!"))
        return {"status": "success", "message": "Call initiated"}
    except Exception as e:
        frappe.log_error(title="Voice AI Call Failed", message=frappe.get_traceback())
        frappe.throw(_("Lỗi khi kết nối với n8n: {0}").format(str(e)))


@frappe.whitelist(allow_guest=True)
def receive_call_result():
    """
    API Webhook: Nhận kết quả từ n8n sau khi cuộc gọi kết thúc.
    Tự động tạo lịch sử cuộc gọi và cập nhật trạng thái khách hàng.
    """
    data = frappe.local.form_dict
    
    lead_id = data.get("lead_id")
    call_id = data.get("call_id")
    transcript = data.get("transcript")
    summary = data.get("summary")
    recording_url = data.get("recording_url")
    intent = data.get("intent") # Cảm xúc: Interested, Not Interested...
    duration = data.get("duration", 0)
    
    if not lead_id or not call_id:
        frappe.throw("Thiếu thông tin bắt buộc: lead_id hoặc call_id", exc=frappe.exceptions.ValidationError)

    lead = frappe.get_doc("CRM Lead", lead_id)
    phone_number = lead.mobile_no or lead.phone

    # Tạo Lịch sử cuộc gọi (CRM Call Log)
    call_log = frappe.get_doc({
        "doctype": "CRM Call Log",
        "type": "Outgoing",
        "reference_doctype": "CRM Lead",
        "reference_docname": lead.name,
        "to": phone_number,
        "duration": duration,
        "status": "Completed", 
        "custom_retell_call_id": call_id,
        "custom_recording_url": recording_url,
        "custom_transcript": transcript,
        "custom_ai_summary": summary,
        "custom_ai_intent": intent,
        "summary": (summary[:140] + "...") if summary else "Cuộc gọi do Voice AI thực hiện"
    })
    call_log.insert(ignore_permissions=True)
    
    # Tự động cập nhật Mức độ quan tâm của Khách hàng dựa vào AI phân tích
    if intent:
        interest_mapping = {
            "Interested": "Quan tâm cao",
            "Not Interested": "Không quan tâm",
            "Call Back": "Trung bình"
        }
        if intent in interest_mapping:
            lead.custom_ai_interest_level = interest_mapping[intent]
            lead.save(ignore_permissions=True)

    frappe.db.commit()
    return {"status": "success", "call_log": call_log.name, "message": "Đã lưu lịch sử cuộc gọi thành công!"}

