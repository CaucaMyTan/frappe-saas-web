<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Chiến dịch</h3>
    </template>
    <template #right-header>
      <Button variant="solid" label="Tạo mới" iconLeft="plus" @click="openCreate" />
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

    <div class="flex flex-1 flex-col overflow-hidden">
      <VoiceListPage
        v-if="activeTab === 'cold'"
        doctype="AI Campaign"
        title="Chiến dịch AutoCall"
        :fields="coldFields"
        :columns="coldColumns"
        :show-header="false"
      />
      <VoiceListPage
        v-else-if="activeTab === 'fb'"
        doctype="FB Campaign"
        title="Chiến dịch FB Lead"
        :fields="fbFields"
        :columns="fbColumns"
        :show-header="false"
      />
      <VoiceListPage
        v-else-if="activeTab === 'cskh'"
        doctype="CSKH Care Event"
        title="Chăm sóc KH"
        :fields="cskhFields"
        :columns="cskhColumns"
        :show-header="false"
      />
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import VoiceListPage from './voice/VoiceListPage.vue'
import { Button } from 'frappe-ui'
import { ref } from 'vue'
import { useDoctypeModal } from '@/composables/doctypeModal'

const activeTab = ref('cold')

const tabs = [
  { id: 'cold', label: 'AutoCall' },
  { id: 'fb', label: 'FB Lead' },
  { id: 'cskh', label: 'Chăm sóc KH' },
]

const { showModal } = useDoctypeModal()

const doctypeMap = {
  cold: 'AI Campaign',
  fb: 'FB Campaign',
  cskh: 'CSKH Care Event',
}

function openCreate() {
  showModal({ doctype: doctypeMap[activeTab.value], title: 'Tạo chiến dịch' })
}

const coldFields = ['name', 'campaign_name', 'ai_agent', 'status', 'total_calls', 'successful_calls', 'creation']
const coldColumns = [
  { key: 'campaign_name', label: 'Tên chiến dịch' },
  { key: 'ai_agent', label: 'AI Agent' },
  {
    key: 'status',
    label: 'Trạng thái',
    type: 'badge',
    themeMap: { Draft: 'gray', Running: 'green', Paused: 'yellow', Completed: 'blue' },
  },
  { key: 'total_calls', label: 'Tổng cuộc gọi' },
  { key: 'successful_calls', label: 'Thành công' },
]

const fbFields = ['name', 'campaign_name', 'fb_page_name', 'status', 'leads_count', 'called_count', 'booked_count']
const fbColumns = [
  { key: 'campaign_name', label: 'Tên chiến dịch' },
  { key: 'fb_page_name', label: 'FB Page' },
  {
    key: 'status',
    label: 'Trạng thái',
    type: 'badge',
    themeMap: { active: 'green', paused: 'yellow', ended: 'gray' },
  },
  { key: 'leads_count', label: 'Leads' },
  { key: 'called_count', label: 'Đã gọi' },
  { key: 'booked_count', label: 'Đã đặt lịch' },
]

const cskhFields = ['name', 'contact_name', 'contact_phone', 'channel', 'status', 'scheduled_at']
const cskhColumns = [
  { key: 'contact_name', label: 'Khách hàng' },
  { key: 'contact_phone', label: 'Số điện thoại' },
  {
    key: 'channel',
    label: 'Kênh',
    type: 'badge',
    themeMap: { zalo: 'blue', sms: 'green' },
  },
  {
    key: 'status',
    label: 'Trạng thái',
    type: 'badge',
    themeMap: { pending: 'gray', sent: 'green', failed: 'red' },
  },
  { key: 'scheduled_at', label: 'Thời gian' },
]
</script>
