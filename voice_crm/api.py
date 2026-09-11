import frappe

def create_doctypes():
    frappe.flags.in_install = True

    # 1. AI Campaign Target (Child DocType)
    if not frappe.db.exists("DocType", "AI Campaign Target"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "AI Campaign Target",
            "module": "Voice Crm",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "lead", "label": "Khách hàng (Lead)", "fieldtype": "Link", "options": "CRM Lead", "in_list_view": 1, "reqd": 1},
                {"fieldname": "status", "label": "Trạng thái gọi", "fieldtype": "Select", "options": "Pending\nCalled\nFailed", "default": "Pending", "in_list_view": 1},
                {"fieldname": "call_log", "label": "Lịch sử cuộc gọi", "fieldtype": "Link", "options": "CRM Call Log", "in_list_view": 1, "read_only": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: AI Campaign Target")

    # 2. AI Agent
    if not frappe.db.exists("DocType", "AI Agent"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "AI Agent",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "field:agent_name",
            "fields": [
                {"fieldname": "agent_name", "label": "Tên kịch bản AI", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "retell_agent_id", "label": "Retell Agent ID", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "prompt_template", "label": "Nội dung Kịch bản (Prompt)", "fieldtype": "Text Editor"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: AI Agent")

    # 3. AI Campaign
    if not frappe.db.exists("DocType", "AI Campaign"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "AI Campaign",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "format:CAMP-{####}",
            "fields": [
                {"fieldname": "campaign_name", "label": "Tên chiến dịch", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "ai_agent", "label": "Chọn Kịch bản AI", "fieldtype": "Link", "options": "AI Agent", "reqd": 1},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "Draft\nRunning\nPaused\nCompleted", "default": "Draft"},
                {"fieldname": "targets_section", "label": "Danh sách gọi", "fieldtype": "Section Break"},
                {"fieldname": "target_leads", "label": "Khách hàng", "fieldtype": "Table", "options": "AI Campaign Target"},
                {"fieldname": "stats_section", "label": "Thống kê", "fieldtype": "Section Break"},
                {"fieldname": "total_calls", "label": "Tổng số đã gọi", "fieldtype": "Int", "read_only": 1},
                {"fieldname": "successful_calls", "label": "Số cuộc thành công", "fieldtype": "Int", "read_only": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: AI Campaign")

    # 4. Voice CRM Client
    if not frappe.db.exists("DocType", "Voice CRM Client"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Voice CRM Client",
            "module": "Voice Crm",
            "custom": 1,
            "issingle": 1,
            "fields": [
                {"fieldname": "clinic_name", "label": "Tên Clinic", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "slug", "label": "Slug", "fieldtype": "Data"},
                {"fieldname": "industry", "label": "Ngành nghề", "fieldtype": "Select", "options": "dental\nspa\nclinic\nother"},
                {"fieldname": "package", "label": "Gói cước", "fieldtype": "Select", "options": "basic\nstandard\npremium"},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "trial\nactive\nsuspended"},
                
                {"fieldname": "retell_config", "label": "Cấu hình Retell AI", "fieldtype": "Section Break"},
                {"fieldname": "retell_phone_number", "label": "Retell Phone Number", "fieldtype": "Data"},
                {"fieldname": "retell_phone_id", "label": "Retell Phone ID", "fieldtype": "Data"},
                {"fieldname": "agent_receptionist_id", "label": "Agent Receptionist ID", "fieldtype": "Data"},
                {"fieldname": "agent_cold_id", "label": "Agent Cold ID", "fieldtype": "Data"},
                {"fieldname": "agent_cskh_id", "label": "Agent CSKH ID", "fieldtype": "Data"},
                {"fieldname": "agent_warm_id", "label": "Agent Warm ID", "fieldtype": "Data"},
                
                {"fieldname": "integration_config", "label": "Cấu hình Tích hợp", "fieldtype": "Section Break"},
                {"fieldname": "zapbx_ip", "label": "ZapBX IP", "fieldtype": "Data"},
                {"fieldname": "zapbx_port", "label": "ZapBX Port", "fieldtype": "Int", "default": 5060},
                {"fieldname": "calcom_event_type_id", "label": "Cal.com Event Type ID", "fieldtype": "Data"},
                {"fieldname": "calcom_api_key", "label": "Cal.com API Key", "fieldtype": "Password"},
                {"fieldname": "telegram_chat_id", "label": "Telegram Chat ID", "fieldtype": "Data"},
                
                {"fieldname": "business_info", "label": "Thông tin Doanh nghiệp", "fieldtype": "Section Break"},
                {"fieldname": "owner_name", "label": "Tên Chủ sở hữu", "fieldtype": "Data"},
                {"fieldname": "owner_phone", "label": "SĐT Chủ sở hữu", "fieldtype": "Data"},
                {"fieldname": "owner_zalo", "label": "Zalo Chủ sở hữu", "fieldtype": "Data"},
                {"fieldname": "contact_email", "label": "Email Liên hệ", "fieldtype": "Data"},
                {"fieldname": "monthly_fee", "label": "Phí hàng tháng", "fieldtype": "Currency"},
                {"fieldname": "contract_start", "label": "Ngày bắt đầu hợp đồng", "fieldtype": "Date"},
                {"fieldname": "trial_ends_at", "label": "Ngày kết thúc dùng thử", "fieldtype": "Date"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: Voice CRM Client")

    # 5. Voice Appointment
    if not frappe.db.exists("DocType", "Voice Appointment"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Voice Appointment",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "format:APT-{####}",
            "fields": [
                {"fieldname": "contact", "label": "Khách hàng", "fieldtype": "Link", "options": "CRM Lead", "reqd": 1, "in_list_view": 1},
                {"fieldname": "call_log", "label": "Cuộc gọi", "fieldtype": "Link", "options": "CRM Call Log"},
                {"fieldname": "scheduled_at", "label": "Thời gian hẹn", "fieldtype": "Datetime", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "pending\nconfirmed\ncancelled\ncompleted", "default": "pending", "in_list_view": 1},
                {"fieldname": "cal_booking_id", "label": "Cal.com Booking ID", "fieldtype": "Data"},
                {"fieldname": "appointment_notes", "label": "Ghi chú", "fieldtype": "Text"},
                {"fieldname": "created_by_ai", "label": "Tạo bởi AI", "fieldtype": "Check", "default": 1},
                {"fieldname": "tenant_id", "label": "Tenant ID", "fieldtype": "Data", "hidden": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: Voice Appointment")

    # 6. CSKH Care Event
    if not frappe.db.exists("DocType", "CSKH Care Event"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "CSKH Care Event",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "format:CSKH-{####}",
            "fields": [
                {"fieldname": "contact", "label": "Khách hàng", "fieldtype": "Link", "options": "CRM Lead", "reqd": 1},
                {"fieldname": "call_log", "label": "Cuộc gọi liên quan", "fieldtype": "Link", "options": "CRM Call Log"},
                {"fieldname": "appointment", "label": "Lịch hẹn liên quan", "fieldtype": "Link", "options": "Voice Appointment"},
                {"fieldname": "trigger_type", "label": "Loại Trigger", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "channel", "label": "Kênh gửi", "fieldtype": "Select", "options": "zalo\nsms", "default": "zalo"},
                {"fieldname": "scheduled_at", "label": "Thời gian dự kiến", "fieldtype": "Datetime", "reqd": 1},
                {"fieldname": "sent_at", "label": "Thời gian đã gửi", "fieldtype": "Datetime"},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "pending\nsent\nfailed", "default": "pending"},
                {"fieldname": "contact_phone", "label": "SĐT Liên hệ", "fieldtype": "Data"},
                {"fieldname": "contact_name", "label": "Tên Liên hệ", "fieldtype": "Data"},
                {"fieldname": "message_content", "label": "Nội dung tin nhắn", "fieldtype": "Text"},
                {"fieldname": "zalo_response", "label": "Phản hồi từ Zalo", "fieldtype": "Code"},
                {"fieldname": "retry_count", "label": "Số lần thử lại", "fieldtype": "Int", "default": 0},
                {"fieldname": "metadata", "label": "Metadata", "fieldtype": "Code"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: CSKH Care Event")

    # 7. FB Campaign
    if not frappe.db.exists("DocType", "FB Campaign"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "FB Campaign",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "format:FBC-{####}",
            "fields": [
                {"fieldname": "campaign_name", "label": "Tên Chiến dịch FB", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "fb_page_id", "label": "FB Page ID", "fieldtype": "Data"},
                {"fieldname": "fb_page_name", "label": "Tên FB Page", "fieldtype": "Data"},
                {"fieldname": "post_id", "label": "Post ID", "fieldtype": "Data"},
                {"fieldname": "dm_script", "label": "Kịch bản DM", "fieldtype": "Text Editor"},
                {"fieldname": "agent_key", "label": "Agent xử lý", "fieldtype": "Select", "options": "agent_warm_id\nagent_cold_id\nagent_receptionist_id"},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "active\npaused\nended", "default": "active"},
                {"fieldname": "leads_count", "label": "Số Leads", "fieldtype": "Int", "read_only": 1},
                {"fieldname": "called_count", "label": "Đã gọi", "fieldtype": "Int", "read_only": 1},
                {"fieldname": "booked_count", "label": "Đã đặt lịch", "fieldtype": "Int", "read_only": 1},
                {"fieldname": "started_at", "label": "Bắt đầu lúc", "fieldtype": "Datetime"},
                {"fieldname": "ended_at", "label": "Kết thúc lúc", "fieldtype": "Datetime"},
                {"fieldname": "notes", "label": "Ghi chú", "fieldtype": "Text"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: FB Campaign")

    # 8. Facebook Lead
    if not frappe.db.exists("DocType", "Facebook Lead"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Facebook Lead",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "format:FBL-{####}",
            "fields": [
                {"fieldname": "commenter_name", "label": "Tên FB", "fieldtype": "Data"},
                {"fieldname": "real_name", "label": "Tên thật", "fieldtype": "Data"},
                {"fieldname": "commenter_fb_id", "label": "FB ID", "fieldtype": "Data"},
                {"fieldname": "phone", "label": "Số điện thoại", "fieldtype": "Data"},
                {"fieldname": "fb_campaign", "label": "Chiến dịch FB", "fieldtype": "Link", "options": "FB Campaign"},
                {"fieldname": "call_log", "label": "Call Log", "fieldtype": "Link", "options": "CRM Call Log"},
                {"fieldname": "comment_id", "label": "Comment ID", "fieldtype": "Data", "unique": 1},
                {"fieldname": "post_id", "label": "Post ID", "fieldtype": "Data"},
                {"fieldname": "raw_comment", "label": "Nội dung Comment", "fieldtype": "Text"},
                {"fieldname": "services_mentioned", "label": "Dịch vụ quan tâm", "fieldtype": "Small Text"},
                {"fieldname": "sentiment", "label": "Cảm xúc", "fieldtype": "Select", "options": "\npositive\nneutral\nnegative"},
                {"fieldname": "priority", "label": "Mức ưu tiên", "fieldtype": "Select", "options": "HOT\nWARM\nCOLD", "default": "WARM"},
                {"fieldname": "lead_score", "label": "Điểm Lead", "fieldtype": "Int", "default": 0},
                {"fieldname": "lead_status", "label": "Trạng thái Lead", "fieldtype": "Select", "options": "new\ncontacted\nqualified\nlost", "default": "new"},
                {"fieldname": "call_status", "label": "Trạng thái Gọi", "fieldtype": "Select", "options": "pending\ncalled\nfailed", "default": "pending"},
                {"fieldname": "next_action", "label": "Hành động tiếp theo", "fieldtype": "Text"},
                {"fieldname": "outcome", "label": "Kết quả", "fieldtype": "Text"},
                {"fieldname": "last_call_summary", "label": "Tóm tắt cuộc gọi cuối", "fieldtype": "Text Editor"},
                {"fieldname": "dm_sent_at", "label": "Gửi DM lúc", "fieldtype": "Datetime"},
                {"fieldname": "phone_received_at", "label": "Nhận SĐT lúc", "fieldtype": "Datetime"},
                {"fieldname": "contacted_at", "label": "Đã liên hệ lúc", "fieldtype": "Datetime"},
                {"fieldname": "notes", "label": "Ghi chú", "fieldtype": "Text"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: Facebook Lead")

    # 9. AI Inbound Config
    if not frappe.db.exists("DocType", "AI Inbound Config"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "AI Inbound Config",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "field:phone_number",
            "fields": [
                {"fieldname": "phone_number", "label": "Số điện thoại", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "label", "label": "Tên đường dây", "fieldtype": "Data", "in_list_view": 1},
                {"fieldname": "retell_agent_id", "label": "Retell Agent ID", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "is_active", "label": "Đang hoạt động", "fieldtype": "Check", "default": 1, "in_list_view": 1},
                {"fieldname": "script_section", "label": "Kịch bản", "fieldtype": "Section Break"},
                {"fieldname": "greeting_message", "label": "Lời chào mở đầu", "fieldtype": "Small Text"},
                {"fieldname": "response_speed", "label": "Tốc độ phản hồi", "fieldtype": "Select", "options": "Chậm\nBình thường\nNhanh\nRất nhanh", "default": "Bình thường"},
                {"fieldname": "script_template", "label": "Kịch bản chi tiết", "fieldtype": "Text Editor"},
                {"fieldname": "notes", "label": "Ghi chú nội bộ", "fieldtype": "Text"},
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: AI Inbound Config")

    # 10. Message Template
    if not frappe.db.exists("DocType", "Message Template"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Message Template",
            "module": "Voice Crm",
            "custom": 1,
            "autoname": "field:template_name",
            "fields": [
                {"fieldname": "template_name", "label": "Tên mẫu", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "channel", "label": "Kênh gửi", "fieldtype": "Select", "options": "zalo\nsms", "default": "zalo", "in_list_view": 1, "reqd": 1},
                {"fieldname": "template_type", "label": "Loại mẫu", "fieldtype": "Select",
                 "options": "Xác nhận lịch hẹn\nNhắc lịch tái khám\nCảm ơn sau khám\nƯu đãi & Khuyến mãi\nTùy chỉnh",
                 "default": "Tùy chỉnh", "in_list_view": 1},
                {"fieldname": "is_active", "label": "Đang dùng", "fieldtype": "Check", "default": 1},
                {"fieldname": "content_section", "label": "Nội dung", "fieldtype": "Section Break"},
                {"fieldname": "content", "label": "Nội dung tin nhắn", "fieldtype": "Text Editor", "reqd": 1,
                 "description": "Dùng {name} cho tên khách, {datetime} cho thời gian, {clinic} cho tên phòng khám"},
                {"fieldname": "preview_section", "label": "Thông tin thêm", "fieldtype": "Section Break"},
                {"fieldname": "char_count", "label": "Số ký tự (ước tính)", "fieldtype": "Int", "read_only": 1},
                {"fieldname": "usage_count", "label": "Lần đã dùng", "fieldtype": "Int", "read_only": 1, "default": 0},
                {"fieldname": "notes", "label": "Ghi chú", "fieldtype": "Small Text"},
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created DocType: Message Template")

def create_custom_fields():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    
    custom_fields = {
        "CRM Lead": [
            {"fieldname": "custom_supabase_id", "label": "Supabase ID", "fieldtype": "Data", "insert_after": "status", "read_only": 1},
            {"fieldname": "custom_stage", "label": "Giai đoạn (Stage)", "fieldtype": "Select", "options": "\nnew\ncontacted\nqualified\nbooked\nlost", "insert_after": "custom_supabase_id"},
            {"fieldname": "custom_ai_interest_level", "label": "Mức độ quan tâm (AI)", "fieldtype": "Select", "options": "\nQuan tâm cao\nTrung bình\nKhông quan tâm\nChưa gọi", "insert_after": "custom_stage"},
            {"fieldname": "custom_services_interested", "label": "Dịch vụ quan tâm", "fieldtype": "Small Text", "insert_after": "custom_ai_interest_level"},
            {"fieldname": "custom_occupation", "label": "Nghề nghiệp", "fieldtype": "Data", "insert_after": "custom_services_interested"},
            {"fieldname": "custom_birthday", "label": "Ngày sinh", "fieldtype": "Date", "insert_after": "custom_occupation"},
            {"fieldname": "custom_followup_at", "label": "Hẹn gọi lại lúc", "fieldtype": "Datetime", "insert_after": "custom_birthday"},
            {"fieldname": "custom_last_call_summary", "label": "Tóm tắt cuộc gọi cuối", "fieldtype": "Text Editor", "insert_after": "custom_followup_at"},
            {"fieldname": "custom_returning_caller", "label": "Khách gọi lại", "fieldtype": "Check", "insert_after": "custom_last_call_summary"},
            {"fieldname": "custom_call_count", "label": "Tổng số cuộc gọi", "fieldtype": "Int", "insert_after": "custom_returning_caller", "read_only": 1},
            {"fieldname": "custom_last_called_at", "label": "Gọi lần cuối lúc", "fieldtype": "Datetime", "insert_after": "custom_call_count", "read_only": 1},
            {"fieldname": "custom_lead_source_detail", "label": "Nguồn chi tiết (Ad ID/Form)", "fieldtype": "Data", "insert_after": "source"}
        ],
        "CRM Call Log": [
            {"fieldname": "custom_voice_ai_section", "label": "Thông tin Voice AI", "fieldtype": "Section Break", "insert_after": "duration"},
            {"fieldname": "custom_retell_call_id", "label": "Retell Call ID", "fieldtype": "Data", "read_only": 1},
            {"fieldname": "custom_recording_url", "label": "Link Ghi âm", "fieldtype": "Data"},
            {"fieldname": "custom_call_direction", "label": "Hướng gọi", "fieldtype": "Select", "options": "inbound\noutbound", "default": "inbound"},
            {"fieldname": "custom_call_type", "label": "Loại cuộc gọi", "fieldtype": "Select", "options": "inbound\noutbound\ncampaign\ncskh", "default": "inbound"},
            {"fieldname": "custom_is_qualified", "label": "Đã Qualified", "fieldtype": "Check"},
            {"fieldname": "custom_appointment_booked", "label": "Đã đặt lịch", "fieldtype": "Check"},
            {"fieldname": "custom_ai_intent", "label": "Phân loại cảm xúc (Intent)", "fieldtype": "Select", "options": "\nInterested\nNot Interested\nCall Back\nVoicemail"},
            {"fieldname": "custom_retry_count", "label": "Số lần thử lại", "fieldtype": "Int", "default": 0},
            {"fieldname": "custom_no_answer_count", "label": "Số lần không nghe máy", "fieldtype": "Int", "default": 0},
            {"fieldname": "custom_appointment_datetime", "label": "Thời gian đặt lịch", "fieldtype": "Datetime"},
            {"fieldname": "custom_appointment_notes", "label": "Ghi chú đặt lịch", "fieldtype": "Text"},
            {"fieldname": "custom_ai_summary", "label": "AI Tóm tắt", "fieldtype": "Text Editor"},
            {"fieldname": "custom_transcript", "label": "Bản dịch (Transcript)", "fieldtype": "Text Editor"},
            {"fieldname": "custom_raw_data", "label": "Raw Data", "fieldtype": "Code"}
        ]
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    print("Created Custom Fields for CRM Lead and Call Log")

def setup_permissions():
    doctypes = [
        "AI Campaign Target", "AI Agent", "AI Campaign", "Voice CRM Client",
        "Voice Appointment", "CSKH Care Event", "FB Campaign", "Facebook Lead"
    ]
    for dt in doctypes:
        if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": "System Manager"}):
            perm = frappe.new_doc("Custom DocPerm")
            perm.parent = dt
            perm.parenttype = "DocType"
            perm.parentfield = "permissions"
            perm.role = "System Manager"
            perm.read = 1
            perm.write = 1
            perm.create = 1
            perm.delete = 1
            perm.insert(ignore_permissions=True)
            print(f"Granted System Manager permissions for {dt}")

def setup_all():
    create_doctypes()
    create_custom_fields()
    add_tenant_id_field()
    add_integration_fields()
    setup_permissions()
    frappe.db.commit()
    print("ALL DONE")


def add_tenant_id_field():
    dt = frappe.get_doc("DocType", "Voice CRM Client")
    existing = [f.fieldname for f in dt.fields]
    if "tenant_id" not in existing:
        dt.append("fields", {
            "fieldname": "tenant_id",
            "label": "Supabase Tenant ID",
            "fieldtype": "Data",
            "description": "UUID của clinic trong bảng clients Supabase",
        })
        dt.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added tenant_id field")
    else:
        print("tenant_id already exists")


def add_integration_fields():
    """Add Supabase + n8n config fields to Voice CRM Client doctype."""
    dt = frappe.get_doc("DocType", "Voice CRM Client")

    existing = [f.fieldname for f in dt.fields]
    new_fields = [
        {"fieldname": "supabase_section", "label": "Supabase & n8n Config", "fieldtype": "Section Break"},
        {"fieldname": "supabase_url", "label": "Supabase URL", "fieldtype": "Data"},
        {"fieldname": "supabase_anon_key", "label": "Supabase Anon Key", "fieldtype": "Password"},
        {"fieldname": "supabase_service_key", "label": "Supabase Service Key", "fieldtype": "Password"},
        {"fieldname": "n8n_base_url", "label": "n8n Base URL", "fieldtype": "Data"},
        {"fieldname": "retell_api_key", "label": "Retell API Key", "fieldtype": "Password"},
    ]

    added = []
    for f in new_fields:
        if f["fieldname"] not in existing:
            dt.append("fields", f)
            added.append(f["fieldname"])

    if added:
        dt.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"Added fields: {added}")
    else:
        print("All fields already exist")


def save_integration_config():
    """Save Supabase and n8n credentials to Voice CRM Client.
    Read from environment variables — set these in your shell or .env before running setup_all.
    """
    import os
    doc = frappe.get_doc("Voice CRM Client")
    doc.supabase_url = os.environ.get("SUPABASE_URL", "")
    doc.supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    doc.supabase_service_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    doc.n8n_base_url = os.environ.get("N8N_BASE_URL", "")
    doc.retell_api_key = os.environ.get("RETELL_API_KEY", "")
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Saved integration config to Voice CRM Client")


@frappe.whitelist(allow_guest=True)
def post_call_handler(**kwargs):
    """
    Webhook handler for n8n/Retell AI to push call data into Frappe CRM.
    Accepts both WF1 field names (retell_call_id, contact_phone, duration_seconds)
    and legacy names (call_id, customer_phone, duration).
    """
    frappe.logger("voice_crm").info(f"Received post_call_handler webhook: {frappe.form_dict}")

    # Normalize field names — WF1 uses retell_call_id / contact_phone / duration_seconds
    call_id = kwargs.get("retell_call_id") or kwargs.get("call_id")
    customer_phone = kwargs.get("contact_phone") or kwargs.get("customer_phone")
    customer_name = kwargs.get("contact_name") or kwargs.get("customer_name") or customer_phone
    duration = int(kwargs.get("duration_seconds") or kwargs.get("duration") or 0)

    # WF1 sends status as 'no_answer'/'completed'; normalize to Frappe title-case
    raw_status = kwargs.get("status") or kwargs.get("call_status") or "completed"
    status_map = {
        "completed": "Completed",
        "no_answer": "No Answer",
        "failed": "Failed",
        "busy": "Busy",
    }
    call_status = status_map.get(raw_status.lower(), raw_status.title())

    if not call_id:
        frappe.throw("Missing call_id / retell_call_id", exc=frappe.exceptions.ValidationError)

    lead_name = None
    if customer_phone:
        leads = frappe.get_all("CRM Lead", filters={"mobile_no": customer_phone}, limit=1)
        if leads:
            lead_name = leads[0].name
        else:
            new_lead = frappe.get_doc({
                "doctype": "CRM Lead",
                "first_name": customer_name,
                "mobile_no": customer_phone,
                "source": "Voice AI",
                "custom_stage": "contacted",
            })
            new_lead.insert(ignore_permissions=True)
            lead_name = new_lead.name

    existing_log = frappe.db.exists("CRM Call Log", {"custom_retell_call_id": call_id})
    if existing_log:
        call_log = frappe.get_doc("CRM Call Log", existing_log)
    else:
        call_log = frappe.new_doc("CRM Call Log")

    direction = kwargs.get("direction", "inbound").lower()
    call_log.update({
        "from": customer_phone if direction == "inbound" else kwargs.get("agent_number", "AI Agent"),
        "to": kwargs.get("agent_number", "AI Agent") if direction == "inbound" else customer_phone,
        "type": "Incoming" if direction == "inbound" else "Outgoing",
        "status": call_status,
        "duration": duration,
        "reference_doctype": "CRM Lead" if lead_name else None,
        "reference_docname": lead_name,
        "custom_retell_call_id": call_id,
        "custom_recording_url": kwargs.get("recording_url"),
        "custom_call_direction": direction,
        "custom_is_qualified": kwargs.get("is_qualified", 0),
        "custom_appointment_booked": 1 if kwargs.get("appointment_booked") else 0,
        "custom_ai_intent": kwargs.get("intent", ""),
        "custom_ai_summary": kwargs.get("summary", ""),
        "custom_transcript": kwargs.get("transcript", ""),
        "custom_appointment_datetime": kwargs.get("appointment_datetime"),
        "custom_appointment_notes": kwargs.get("appointment_notes"),
        "custom_raw_data": frappe.as_json(kwargs),
    })
    call_log.save(ignore_permissions=True)

    if lead_name:
        doc_lead = frappe.get_doc("CRM Lead", lead_name)
        doc_lead.custom_last_call_summary = kwargs.get("summary")
        doc_lead.custom_last_called_at = frappe.utils.now()
        doc_lead.custom_call_count = (doc_lead.custom_call_count or 0) + 1

        if kwargs.get("appointment_booked"):
            doc_lead.custom_stage = "booked"
        elif call_status == "Completed":
            doc_lead.custom_stage = "contacted"

        doc_lead.save(ignore_permissions=True)

    # Auto-create Voice Appointment if booked
    if kwargs.get("appointment_booked") and kwargs.get("appointment_datetime") and lead_name:
        apt = frappe.get_doc({
            "doctype": "Voice Appointment",
            "contact": lead_name,
            "call_log": call_log.name,
            "scheduled_at": kwargs.get("appointment_datetime"),
            "appointment_notes": kwargs.get("appointment_notes"),
            "created_by_ai": 1,
        })
        apt.insert(ignore_permissions=True)

    return {"status": "success", "call_log": call_log.name, "lead": lead_name}

@frappe.whitelist(allow_guest=True)
def create_facebook_lead(**kwargs):
    """
    Webhook handler cho FB Lead Ads hoặc Comment via n8n
    """
    comment_id = kwargs.get("comment_id")
    fb_id = kwargs.get("commenter_fb_id")
    
    if not comment_id:
        frappe.throw("Missing comment_id", exc=frappe.exceptions.ValidationError)
        
    if frappe.db.exists("Facebook Lead", {"comment_id": comment_id}):
        return {"status": "skipped", "message": "Lead already exists"}
        
    fb_lead = frappe.get_doc({
        "doctype": "Facebook Lead",
        "commenter_name": kwargs.get("commenter_name"),
        "commenter_fb_id": fb_id,
        "comment_id": comment_id,
        "post_id": kwargs.get("post_id"),
        "raw_comment": kwargs.get("raw_comment"),
        "phone": kwargs.get("phone"),
        "fb_campaign": kwargs.get("fb_campaign")
    })
    fb_lead.insert(ignore_permissions=True)
    
    return {"status": "success", "fb_lead": fb_lead.name}

@frappe.whitelist(allow_guest=True)
def create_appointment(**kwargs):
    lead_id = kwargs.get("lead_id")
    if not lead_id:
        frappe.throw("Missing lead_id", exc=frappe.exceptions.ValidationError)
        
    apt = frappe.get_doc({
        "doctype": "Voice Appointment",
        "contact": lead_id,
        "scheduled_at": kwargs.get("scheduled_at"),
        "cal_booking_id": kwargs.get("cal_booking_id"),
        "appointment_notes": kwargs.get("notes"),
        "created_by_ai": 1
    })
    apt.insert(ignore_permissions=True)
    return {"status": "success", "appointment": apt.name}

@frappe.whitelist(allow_guest=False)
def get_pending_cskh():
    """Lấy danh sách task CSKH cần n8n xử lý (SMS/Zalo)"""
    events = frappe.get_all(
        "CSKH Care Event",
        filters={"status": "pending", "scheduled_at": ["<=", frappe.utils.now()]},
        fields=["name", "contact_phone", "contact_name", "message_content", "channel"]
    )
    return {"status": "success", "data": events}


@frappe.whitelist(allow_guest=False)
def get_pending_calls():
    """
    n8n polls this endpoint to get AI Campaign targets waiting to be called.
    Returns targets from all Running campaigns, including agent ID and lead phone.
    """
    running_campaigns = frappe.get_all(
        "AI Campaign",
        filters={"status": "Running"},
        fields=["name", "ai_agent"]
    )

    if not running_campaigns:
        return {"status": "success", "data": []}

    results = []
    for campaign in running_campaigns:
        agent_doc = frappe.get_value("AI Agent", campaign["ai_agent"], "retell_agent_id") if campaign["ai_agent"] else None

        targets = frappe.get_all(
            "AI Campaign Target",
            filters={"parent": campaign["name"], "parenttype": "AI Campaign", "status": "Pending"},
            fields=["name", "lead"]
        )

        for target in targets:
            if not target["lead"]:
                continue
            phone = frappe.get_value("CRM Lead", target["lead"], "mobile_no")
            if not phone:
                continue
            results.append({
                "campaign": campaign["name"],
                "target_row": target["name"],
                "lead": target["lead"],
                "phone": phone,
                "retell_agent_id": agent_doc,
            })

    return {"status": "success", "data": results}


@frappe.whitelist(allow_guest=False)
def update_campaign_target_status(target_row, campaign, call_status, call_log=None):
    """
    Called by n8n after attempting a call to update the AI Campaign Target row status.
    call_status: 'Called' | 'Failed'
    """
    if not frappe.db.exists("AI Campaign Target", target_row):
        frappe.throw("Target row not found", exc=frappe.exceptions.DoesNotExistError)

    campaign_doc = frappe.get_doc("AI Campaign", campaign)
    for row in campaign_doc.target_leads:
        if row.name == target_row:
            row.status = call_status
            if call_log:
                row.call_log = call_log
            break

    if call_status == "Called":
        campaign_doc.total_calls = (campaign_doc.total_calls or 0) + 1
    if call_status == "Called":
        campaign_doc.successful_calls = (campaign_doc.successful_calls or 0) + 1

    # Auto-complete campaign when all targets are done
    pending = [r for r in campaign_doc.target_leads if r.status == "Pending"]
    if not pending:
        campaign_doc.status = "Completed"

    campaign_doc.save(ignore_permissions=True)
    return {"status": "success"}


@frappe.whitelist(allow_guest=True)
def trigger_campaign(**kwargs):
    """
    n8n calls this when a new Facebook lead arrives to add them to the relevant AI Campaign.
    Expects: fb_lead_name OR (phone + commenter_name), fb_campaign
    Creates/links a CRM Lead, adds as Pending target to the campaign, returns agent info.
    """
    fb_campaign_name = kwargs.get("fb_campaign")
    phone = kwargs.get("phone")
    commenter_name = kwargs.get("commenter_name") or phone

    if not fb_campaign_name:
        frappe.throw("Missing fb_campaign", exc=frappe.exceptions.ValidationError)

    if not frappe.db.exists("FB Campaign", fb_campaign_name):
        frappe.throw("FB Campaign not found", exc=frappe.exceptions.DoesNotExistError)

    fb_campaign = frappe.get_doc("FB Campaign", fb_campaign_name)

    # Find the AI Campaign linked to this FB Campaign (match by name convention FBC-XXXX -> CAMP-XXXX)
    # Or caller can pass ai_campaign directly
    ai_campaign_name = kwargs.get("ai_campaign")
    if not ai_campaign_name:
        # Try to find a Running AI Campaign with same name as FB Campaign
        candidates = frappe.get_all(
            "AI Campaign",
            filters={"campaign_name": fb_campaign.campaign_name, "status": ["in", ["Draft", "Running"]]},
            limit=1,
            fields=["name", "status"]
        )
        if candidates:
            ai_campaign_name = candidates[0]["name"]

    # Ensure/create CRM Lead from phone
    lead_name = None
    if phone:
        leads = frappe.get_all("CRM Lead", filters={"mobile_no": phone}, limit=1)
        if leads:
            lead_name = leads[0].name
        else:
            new_lead = frappe.get_doc({
                "doctype": "CRM Lead",
                "first_name": commenter_name,
                "mobile_no": phone,
                "source": "Facebook",
                "custom_stage": "new",
                "custom_lead_source_detail": fb_campaign_name,
            })
            new_lead.insert(ignore_permissions=True)
            lead_name = new_lead.name

    agent_id = None
    if ai_campaign_name and lead_name:
        ai_campaign = frappe.get_doc("AI Campaign", ai_campaign_name)

        # Avoid duplicate targets
        already_added = any(row.lead == lead_name for row in ai_campaign.target_leads)
        if not already_added:
            ai_campaign.append("target_leads", {
                "lead": lead_name,
                "status": "Pending",
            })
            if ai_campaign.status == "Draft":
                ai_campaign.status = "Running"
            ai_campaign.leads_count = len(ai_campaign.target_leads)
            ai_campaign.save(ignore_permissions=True)

        if ai_campaign.ai_agent:
            agent_id = frappe.get_value("AI Agent", ai_campaign.ai_agent, "retell_agent_id")

    # Update FB Campaign counters
    fb_campaign.leads_count = (fb_campaign.leads_count or 0) + 1
    fb_campaign.save(ignore_permissions=True)

    return {
        "status": "success",
        "lead": lead_name,
        "ai_campaign": ai_campaign_name,
        "retell_agent_id": agent_id,
        "phone": phone,
    }


# ─────────────────────────────────────────────
#  SUPABASE PROXY ENDPOINTS
# ─────────────────────────────────────────────

def _supabase_is_configured():
    """Use local Frappe records until this development site has Supabase credentials."""
    try:
        doc = frappe.get_doc("Voice CRM Client")
    except Exception:
        return False
    return all(
        getattr(doc, field, None)
        for field in ("supabase_url", "supabase_service_key", "tenant_id")
    )


def _local_campaign_status(status):
    return {
        "Draft": "draft",
        "Running": "running",
        "Paused": "paused",
        "Completed": "completed",
    }.get(status or "Draft", str(status).lower())


def _local_campaign_payload(doc):
    agent_name = doc.ai_agent or ""
    agent_label = agent_name
    agent_lower = agent_name.lower()
    if "reception" in agent_lower:
        agent_key = "receptionist"
    elif "cskh" in agent_lower:
        agent_key = "cskh"
    elif "sales" in agent_lower:
        agent_key = "warm"
    else:
        agent_key = "cold"

    contacts = []
    for row in (doc.target_leads or []):
        if not row.lead:
            continue
        lead = frappe.db.get_value(
            "CRM Lead", row.lead, ["lead_name", "mobile_no"], as_dict=True
        )
        if lead:
            contacts.append({"id": row.lead, "name": lead.lead_name or row.lead, "phone": lead.mobile_no})
    total = int(doc.total_calls or 0)
    called = total if doc.status in ("Running", "Completed") else 0
    booked = int(doc.successful_calls or 0)
    return {
        "id": doc.name,
        "name": doc.campaign_name,
        "description": "Chiến dịch demo của Nha khoa An Tâm chạy trên dữ liệu local Frappe.",
        "agent_key": agent_key,
        "agent_label": agent_label,
        "status": _local_campaign_status(doc.status),
        "total_count": total,
        "called_count": called,
        "booked_count": booked,
        "error_count": 0,
        "no_answer_count": max(0, called - booked),
        "delay_ms": 900,
        "started_at": doc.creation if doc.status == "Running" else None,
        "completed_at": doc.modified if doc.status == "Completed" else None,
        "created_at": doc.creation,
        "contacts": contacts,
        "results": [],
    }


def _local_campaign_list(limit=20, offset=0):
    docs = frappe.get_all(
        "AI Campaign",
        fields=["name", "campaign_name", "ai_agent", "status", "total_calls", "successful_calls", "creation", "modified"],
        order_by="creation desc",
        limit_start=int(offset),
        limit_page_length=int(limit),
    )
    return [_local_campaign_payload(frappe.get_doc("AI Campaign", row.name)) for row in docs]


def _local_campaign_detail(campaign_id):
    if not frappe.db.exists("AI Campaign", campaign_id):
        frappe.throw("Không tìm thấy chiến dịch")
    return _local_campaign_payload(frappe.get_doc("AI Campaign", campaign_id))


def _local_contacts(limit=50, offset=0, search=None):
    filters = {}
    or_filters = None
    if search:
        like = f"%{search}%"
        or_filters = [["lead_name", "like", like], ["mobile_no", "like", like], ["email", "like", like]]
    leads = frappe.get_all(
        "CRM Lead",
        filters=filters,
        or_filters=or_filters,
        fields=["name", "lead_name", "mobile_no", "email", "status", "creation"],
        order_by="creation desc",
        limit_start=int(offset),
        limit_page_length=int(limit),
    )
    return [
        {
            "id": lead.name,
            "full_name": lead.lead_name,
            "phone": lead.mobile_no,
            "email": lead.email,
            "stage": lead.status,
            "call_count": 0,
            "created_at": lead.creation,
        }
        for lead in leads
    ]

@frappe.whitelist()
def proxy_get_calls(limit=50, offset=0, status=None, direction=None):
    from voice_crm.supabase_client import sb_get
    filters = {}
    if status:
        filters["status"] = f"eq.{status}"
    if direction:
        filters["direction"] = f"eq.{direction}"
    return sb_get("calls",
        filters=filters,
        fields="id,contact_name,contact_phone,status,duration_seconds,direction,summary,appointment_booked,recording_url,created_at,retell_call_id",
        order="created_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_get_contacts(limit=50, offset=0, search=None):
    if not _supabase_is_configured():
        return _local_contacts(limit, offset, search)
    from voice_crm.supabase_client import sb_get
    filters = {}
    if search:
        filters["or"] = f"(full_name.ilike.%{search}%,phone.ilike.%{search}%)"
    return sb_get("contacts",
        filters=filters,
        fields="id,full_name,phone,email,stage,interest_level,call_count,last_called_at,last_call_summary,created_at",
        order="created_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_create_contact(full_name, phone, email=None, notes=None, lead_source=None):
    from voice_crm.supabase_client import sb_post
    data = {"full_name": full_name, "phone": phone}
    if email: data["email"] = email
    if notes: data["notes"] = notes
    if lead_source: data["lead_source"] = lead_source
    return sb_post("contacts", data)


@frappe.whitelist()
def proxy_update_contact(contact_id, **kwargs):
    from voice_crm.supabase_client import sb_patch
    allowed = ["full_name", "phone", "email", "notes", "stage", "interest_level", "followup_at"]
    data = {k: v for k, v in kwargs.items() if k in allowed}
    return sb_patch("contacts", contact_id, data)


@frappe.whitelist()
def proxy_get_campaigns(limit=20, offset=0):
    if not _supabase_is_configured():
        return _local_campaign_list(limit, offset)
    from voice_crm.supabase_client import sb_get
    return sb_get("campaigns",
        fields="id,name,description,agent_key,agent_label,status,total_count,called_count,booked_count,error_count,no_answer_count,delay_ms,started_at,completed_at,created_at",
        order="created_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_create_campaign(name, agent_key, contacts_json, description=None, delay_ms=3000):
    import json
    if not _supabase_is_configured():
        contacts = json.loads(contacts_json) if isinstance(contacts_json, str) else contacts_json
        agent_names = {
            "cold": "Le Tan AI - Sales Demo",
            "warm": "Le Tan AI - Sales Demo",
            "cskh": "Le Tan AI - CSKH Demo",
            "receptionist": "Le Tan AI - Receptionist Demo",
        }
        campaign = frappe.get_doc({
            "doctype": "AI Campaign",
            "campaign_name": name,
            "ai_agent": agent_names.get(agent_key, agent_names["cold"]),
            "status": "Draft",
            "total_calls": len(contacts),
            "successful_calls": 0,
        })
        for contact in contacts:
            lead = frappe.db.exists("CRM Lead", {"mobile_no": contact.get("phone")})
            if lead:
                campaign.append("target_leads", {"lead": lead, "status": "Pending"})
        campaign.insert(ignore_permissions=True)
        return _local_campaign_payload(campaign)
    from voice_crm.supabase_client import sb_post
    contacts = json.loads(contacts_json) if isinstance(contacts_json, str) else contacts_json
    agent_label_map = {
        "cold": "Gọi Lạnh",
        "warm": "Gọi Ấm",
        "cskh": "Chăm sóc KH",
        "receptionist": "Lễ Tân",
    }
    return sb_post("campaigns", {
        "name": name,
        "description": description or "",
        "agent_key": agent_key,
        "agent_label": agent_label_map.get(agent_key, agent_key.title()),
        "contacts": contacts,
        "results": [],
        "total_count": len(contacts),
        "called_count": 0,
        "booked_count": 0,
        "error_count": 0,
        "no_answer_count": 0,
        "delay_ms": int(delay_ms),
        "status": "draft",
    })


@frappe.whitelist()
def proxy_run_campaign(campaign_id):
    if not _supabase_is_configured():
        campaign = frappe.get_doc("AI Campaign", campaign_id)
        campaign.status = "Running"
        campaign.save(ignore_permissions=True)
        return {"status": "demo_triggered", "campaign_id": campaign_id}
    from voice_crm.supabase_client import n8n_trigger
    result = n8n_trigger("campaign-run", {"campaign_id": campaign_id})
    return {"status": "triggered", "campaign_id": campaign_id, "n8n": result}


@frappe.whitelist()
def proxy_get_appointments(limit=50, offset=0, status=None):
    from voice_crm.supabase_client import sb_get
    filters = {}
    if status:
        filters["status"] = f"eq.{status}"
    return sb_get("appointments",
        filters=filters,
        fields="id,contact_id,call_id,scheduled_at,status,appointment_notes,cal_booking_id,created_at",
        order="scheduled_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_get_fb_campaigns(limit=20, offset=0):
    from voice_crm.supabase_client import sb_get
    return sb_get("fb_campaigns",
        fields="id,name,fb_page_name,post_id,agent_key,status,leads_count,called_count,booked_count,started_at,created_at",
        order="created_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_get_cskh_events(limit=50, offset=0, status=None, channel=None):
    from voice_crm.supabase_client import sb_get
    filters = {}
    if status:
        filters["status"] = f"eq.{status}"
    if channel:
        filters["channel"] = f"eq.{channel}"
    return sb_get("cskh_care_events",
        filters=filters,
        fields="id,contact_name,contact_phone,trigger_type,channel,scheduled_at,sent_at,status,message_content,created_at",
        order="scheduled_at.desc",
        limit=int(limit),
        offset=int(offset),
    )


@frappe.whitelist()
def proxy_send_sms(phone, message):
    from voice_crm.supabase_client import n8n_trigger, get_config
    config = get_config()
    return n8n_trigger("saas-send-sms", {
        "phone": phone,
        "message": message,
        "tenant_id": config.tenant_id,
    })


@frappe.whitelist()
def proxy_get_campaign_detail(campaign_id):
    if not _supabase_is_configured():
        return _local_campaign_detail(campaign_id)
    from voice_crm.supabase_client import sb_get_one
    return sb_get_one("campaigns", campaign_id)


@frappe.whitelist()
def proxy_update_campaign(campaign_id, status=None, name=None, description=None, agent_key=None, delay_ms=None):
    if not _supabase_is_configured():
        campaign = frappe.get_doc("AI Campaign", campaign_id)
        status_map = {"draft": "Draft", "running": "Running", "paused": "Paused", "completed": "Completed"}
        if status is not None:
            campaign.status = status_map.get(status, status)
            if campaign.status == "Completed" and not campaign.successful_calls:
                campaign.successful_calls = max(1, round((campaign.total_calls or 0) * 0.6))
        if name is not None:
            campaign.campaign_name = name
        if agent_key is not None:
            agent_names = {
                "cold": "Le Tan AI - Sales Demo",
                "warm": "Le Tan AI - Sales Demo",
                "cskh": "Le Tan AI - CSKH Demo",
                "receptionist": "Le Tan AI - Receptionist Demo",
            }
            campaign.ai_agent = agent_names.get(agent_key, campaign.ai_agent)
        campaign.save(ignore_permissions=True)
        return _local_campaign_payload(campaign)
    from voice_crm.supabase_client import sb_patch
    data = {}
    if status is not None:
        data["status"] = status
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if agent_key is not None:
        data["agent_key"] = agent_key
    if delay_ms is not None:
        data["delay_ms"] = int(delay_ms)
    if not data:
        frappe.throw("Không có field nào để cập nhật")
    return sb_patch("campaigns", campaign_id, data)


@frappe.whitelist()
def proxy_delete_campaign(campaign_id):
    if not _supabase_is_configured():
        frappe.delete_doc("AI Campaign", campaign_id, ignore_permissions=True)
        return {"ok": True}
    from voice_crm.supabase_client import sb_delete
    return sb_delete("campaigns", campaign_id)


@frappe.whitelist()
def proxy_get_client_config():
    doc = frappe.get_doc("Voice CRM Client")
    agent_map = {
        "cold": ("agent_cold_id", "Gọi Lạnh"),
        "warm": ("agent_warm_id", "Gọi Ấm"),
        "cskh": ("agent_cskh_id", "Chăm sóc KH"),
        "receptionist": ("agent_receptionist_id", "Lễ Tân"),
    }
    agents = {}
    for key, (field, label) in agent_map.items():
        agent_id = getattr(doc, field, None)
        if agent_id:
            agents[key] = {"id": agent_id, "label": label}
    if not agents:
        for agent in frappe.get_all("AI Agent", fields=["agent_name", "retell_agent_id"]):
            agent_name = (agent.agent_name or "").lower()
            if "reception" in agent_name:
                key, label = "receptionist", "Lễ Tân"
            elif "cskh" in agent_name:
                key, label = "cskh", "Chăm sóc KH"
            elif "sales" in agent_name:
                key, label = "warm", "Gọi Ấm"
            else:
                key, label = "cold", "Gọi Lạnh"
            agents[key] = {"id": agent.retell_agent_id, "label": label}
    return {
        "retell_phone_number": getattr(doc, "retell_phone_number", ""),
        "agents": agents,
    }


@frappe.whitelist()
def proxy_trigger_call(phone, name=None, agent_key="cold"):
    if not _supabase_is_configured():
        return {
            "status": "demo_calling",
            "call_id": f"demo-{frappe.generate_hash(length=8)}",
            "phone": phone,
            "name": name or "",
        }
    from voice_crm.supabase_client import retell_call
    doc = frappe.get_doc("Voice CRM Client")
    from_number = doc.retell_phone_number or ""
    agent_col_map = {
        "cold": "agent_cold_id",
        "warm": "agent_warm_id",
        "cskh": "agent_cskh_id",
        "receptionist": "agent_receptionist_id",
    }
    agent_col = agent_col_map.get(agent_key, "agent_cold_id")
    agent_id = getattr(doc, agent_col, None) or doc.agent_cold_id or ""
    if not agent_id:
        frappe.throw("Chưa cấu hình Agent ID cho loại này")
    if not from_number:
        frappe.throw("Chưa cấu hình số điện thoại Retell")
    result = retell_call(
        from_number=from_number,
        to_number=phone,
        agent_id=agent_id,
        customer_name=name or "",
    )
    return {"status": "calling", "call_id": result.get("call_id")}


@frappe.whitelist()
def proxy_manual_call(contact_id):
    import requests as req
    from voice_crm.supabase_client import sb_get_one, get_config, retell_call
    contact = sb_get_one("contacts", contact_id)
    if not contact:
        frappe.throw("Không tìm thấy khách hàng")
    config = get_config()
    client_r = req.get(
        f"{config.url}/rest/v1/clients",
        headers={"apikey": config.key, "Authorization": f"Bearer {config.key}"},
        params={"id": f"eq.{config.tenant_id}", "select": "retell_phone_number,agent_receptionist_id"},
        timeout=10,
    )
    client_data = client_r.json()[0] if client_r.ok and client_r.json() else {}
    result = retell_call(
        from_number=client_data.get("retell_phone_number", ""),
        to_number=contact["phone"],
        agent_id=client_data.get("agent_receptionist_id", ""),
        customer_name=contact.get("full_name", ""),
    )
    return {"status": "calling", "call_id": result.get("call_id"), "contact": contact["full_name"]}
