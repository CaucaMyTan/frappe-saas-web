<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-base font-semibold text-ink-gray-9">Cấu hình Voice AI</h3>
    </template>
    <template #right-header>
      <Button variant="solid" label="Chỉnh sửa" iconLeft="edit-2" @click="openEdit" />
    </template>
  </LayoutHeader>

  <div class="flex-1 overflow-auto p-6">
    <div v-if="config.get.loading" class="flex h-full items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else class="mx-auto max-w-3xl space-y-4">

      <div class="rounded-lg border border-outline-gray-modals bg-surface-white">
        <div class="border-b border-outline-gray-modals px-4 py-3">
          <h4 class="text-sm font-semibold text-ink-gray-7">Thông tin Doanh nghiệp</h4>
        </div>
        <div class="divide-y divide-outline-gray-modals px-4">
          <div v-for="f in businessFields" :key="f.key" class="flex items-center justify-between py-3">
            <span class="text-sm text-ink-gray-5">{{ f.label }}</span>
            <span class="text-sm font-medium text-ink-gray-8">{{ config.doc?.[f.key] || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-outline-gray-modals bg-surface-white">
        <div class="border-b border-outline-gray-modals px-4 py-3">
          <h4 class="text-sm font-semibold text-ink-gray-7">Cấu hình Retell AI</h4>
        </div>
        <div class="divide-y divide-outline-gray-modals px-4">
          <div v-for="f in retellFields" :key="f.key" class="flex items-center justify-between py-3">
            <span class="text-sm text-ink-gray-5">{{ f.label }}</span>
            <span class="font-mono text-sm text-ink-gray-8">{{ config.doc?.[f.key] || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-outline-gray-modals bg-surface-white">
        <div class="border-b border-outline-gray-modals px-4 py-3">
          <h4 class="text-sm font-semibold text-ink-gray-7">Cấu hình Tích hợp</h4>
        </div>
        <div class="divide-y divide-outline-gray-modals px-4">
          <div v-for="f in integrationFields" :key="f.key" class="flex items-center justify-between py-3">
            <span class="text-sm text-ink-gray-5">{{ f.label }}</span>
            <span class="font-mono text-sm text-ink-gray-8">{{ config.doc?.[f.key] || '—' }}</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createDocumentResource, FeatherIcon, Button } from 'frappe-ui'
import { onMounted } from 'vue'

const config = createDocumentResource({
  doctype: 'Voice CRM Client',
  name: 'Voice CRM Client',
})

onMounted(() => config.get.submit())

const { showModal } = useDoctypeModal()

function openEdit() {
  showModal({
    doctype: 'Voice CRM Client',
    name: 'Voice CRM Client',
    title: 'Cấu hình Voice AI',
    callbacks: { afterUpdate: () => config.get.submit() },
  })
}

const businessFields = [
  { key: 'clinic_name', label: 'Tên Clinic' },
  { key: 'industry', label: 'Ngành nghề' },
  { key: 'package', label: 'Gói cước' },
  { key: 'status', label: 'Trạng thái' },
  { key: 'owner_name', label: 'Chủ sở hữu' },
  { key: 'contact_email', label: 'Email liên hệ' },
  { key: 'owner_phone', label: 'SĐT' },
]

const retellFields = [
  { key: 'retell_phone_number', label: 'Số điện thoại Retell' },
  { key: 'retell_phone_id', label: 'Retell Phone ID' },
  { key: 'agent_receptionist_id', label: 'Agent Lễ tân' },
  { key: 'agent_cold_id', label: 'Agent Cold' },
  { key: 'agent_cskh_id', label: 'Agent CSKH' },
  { key: 'agent_warm_id', label: 'Agent Warm' },
]

const integrationFields = [
  { key: 'calcom_event_type_id', label: 'Cal.com Event Type ID' },
  { key: 'telegram_chat_id', label: 'Telegram Chat ID' },
  { key: 'zapbx_ip', label: 'ZapBX IP' },
  { key: 'zapbx_port', label: 'ZapBX Port' },
]
</script>
