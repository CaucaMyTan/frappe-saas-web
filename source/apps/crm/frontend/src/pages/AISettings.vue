<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Cài đặt AI</h3>
    </template>
    <template #right-header>
      <Button
        v-if="activeTab === 'config'"
        variant="solid"
        label="Chỉnh sửa"
        iconLeft="edit-2"
        @click="openEditConfig"
      />
      <Button
        v-else-if="activeTab === 'agents'"
        variant="solid"
        label="Tạo mới"
        iconLeft="plus"
        @click="openCreateAgent"
      />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div class="border-b border-outline-gray-modals">
      <div class="flex gap-0 px-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors"
          :class="
            activeTab === tab.id
              ? 'border-ink-gray-9 text-ink-gray-9'
              : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
          "
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-auto">
      <div v-if="activeTab === 'config'">
        <div v-if="config.get.loading" class="flex h-full items-center justify-center p-12">
          <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
        </div>
        <div v-else class="mx-auto max-w-3xl space-y-4 p-6">
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

      <div v-else-if="activeTab === 'agents'" class="flex flex-1 flex-col h-full">
        <div v-if="agents.loading" class="flex h-32 items-center justify-center">
          <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
        </div>
        <div v-else-if="agents.data?.length" class="overflow-auto">
          <table class="w-full border-collapse">
            <thead class="sticky top-0 z-10 bg-surface-white">
              <tr>
                <th v-for="col in agentColumns" :key="col.key" class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">
                  {{ col.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in agents.data" :key="row.name"
                class="cursor-pointer border-b border-outline-gray-modals hover:bg-surface-gray-1"
                @click="openEditAgent(row.name)">
                <td v-for="col in agentColumns" :key="col.key" class="max-w-[240px] truncate px-4 py-3 text-sm text-ink-gray-8">
                  {{ row[col.key] || '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4 py-12">
          <FeatherIcon name="cpu" class="h-10 w-10" />
          <span class="text-sm">Chưa có kịch bản nào</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createDocumentResource, createListResource, FeatherIcon, Button } from 'frappe-ui'
import { ref, onMounted } from 'vue'

const activeTab = ref('config')
const tabs = [
  { id: 'config', label: 'Cài đặt hệ thống' },
  { id: 'agents', label: 'Kịch bản AI' },
]

const { showModal } = useDoctypeModal()

const config = createDocumentResource({
  doctype: 'Voice CRM Client',
  name: 'Voice CRM Client',
})

const agents = createListResource({
  type: 'list',
  doctype: 'AI Agent',
  fields: ['name', 'agent_name', 'retell_agent_id'],
  orderBy: 'creation desc',
  pageLength: 50,
})

onMounted(() => {
  config.get.submit()
  agents.reload()
})

function openEditConfig() {
  showModal({
    doctype: 'Voice CRM Client',
    name: 'Voice CRM Client',
    title: 'Cài đặt hệ thống',
    callbacks: { afterUpdate: () => config.get.submit() },
  })
}

function openCreateAgent() {
  showModal({
    doctype: 'AI Agent',
    title: 'Tạo kịch bản AI',
    callbacks: { afterInsert: () => agents.reload() },
  })
}

function openEditAgent(name) {
  showModal({
    doctype: 'AI Agent',
    name,
    title: 'Kịch bản AI',
    callbacks: { afterUpdate: () => agents.reload() },
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

const agentColumns = [
  { key: 'name', label: 'Mã' },
  { key: 'agent_name', label: 'Tên kịch bản' },
  { key: 'retell_agent_id', label: 'Retell Agent ID' },
]
</script>
