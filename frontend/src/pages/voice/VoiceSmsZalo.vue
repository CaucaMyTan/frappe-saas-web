<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">SMS & Zalo</h3>
    </template>
    <template #right-header>
      <Button variant="solid" :label="activeMainTab === 'history' ? 'Tạo lịch gửi' : 'Tạo mẫu tin'" iconLeft="plus" @click="openCreate" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <!-- Main tabs -->
    <div class="border-b border-outline-gray-modals bg-surface-white px-4">
      <div class="flex gap-0">
        <button
          v-for="tab in mainTabs"
          :key="tab.id"
          class="px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors"
          :class="
            activeMainTab === tab.id
              ? 'border-ink-gray-9 text-ink-gray-9'
              : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
          "
          @click="activeMainTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Lịch sử gửi tab -->
    <template v-if="activeMainTab === 'history'">
      <div class="border-b border-outline-gray-modals bg-surface-white px-4">
        <div class="flex items-center gap-4">
          <div class="flex gap-0">
            <button
              v-for="tab in channelTabs"
              :key="tab.id"
              class="px-3 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors"
              :class="
                activeChannel === tab.id
                  ? 'border-ink-gray-9 text-ink-gray-9'
                  : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
              "
              @click="activeChannel = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>
          <div class="h-4 w-px bg-outline-gray-modals" />
          <div class="flex gap-1.5 py-2">
            <button
              v-for="pill in statusPills"
              :key="pill.id"
              class="rounded-full px-3 py-0.5 text-xs font-medium transition-colors"
              :class="
                activeStatus === pill.id
                  ? 'bg-ink-gray-9 text-surface-white'
                  : 'bg-surface-gray-2 text-ink-gray-6 hover:bg-surface-gray-3'
              "
              @click="activeStatus = pill.id"
            >
              {{ pill.label }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="historyList.loading" class="flex flex-1 items-center justify-center">
        <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
      </div>

      <div v-else-if="historyList.data?.length" class="flex-1 overflow-auto">
        <table class="w-full border-collapse">
          <thead class="sticky top-0 z-10 bg-surface-white">
            <tr>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Khách hàng</th>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Số điện thoại</th>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Kênh</th>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Loại</th>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời gian</th>
              <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in historyList.data"
              :key="row.name"
              class="cursor-pointer border-b border-outline-gray-modals hover:bg-surface-gray-1"
              @click="openEditHistory(row.name)"
            >
              <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.contact_name || '—' }}</td>
              <td class="px-4 py-3 text-sm text-ink-gray-7">{{ row.contact_phone || '—' }}</td>
              <td class="px-4 py-3">
                <Badge :label="channelLabel[row.channel] || row.channel || '—'" :theme="channelTheme[row.channel] || 'gray'" size="sm" />
              </td>
              <td class="px-4 py-3 text-sm text-ink-gray-6">{{ triggerLabel[row.trigger_type] || row.trigger_type || '—' }}</td>
              <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatDateTime(row.scheduled_at) }}</td>
              <td class="px-4 py-3">
                <Badge :label="sendStatusLabel[row.status] || row.status || '—'" :theme="sendStatusTheme[row.status] || 'gray'" size="sm" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
        <FeatherIcon name="send" class="h-10 w-10" />
        <p class="text-sm font-medium text-ink-gray-5">Không có tin nhắn nào</p>
        <p class="text-xs">{{ activeChannel !== 'all' ? `Chưa có lịch gửi ${channelLabel[activeChannel]} nào` : 'Chưa có lịch gửi nào' }}</p>
      </div>
    </template>

    <!-- Mẫu tin nhắn tab -->
    <template v-else>
      <div v-if="templateList.loading" class="flex flex-1 items-center justify-center">
        <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
      </div>

      <div v-else-if="templateList.data?.length" class="flex-1 overflow-auto p-4">
        <div class="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="tpl in templateList.data"
            :key="tpl.name"
            class="cursor-pointer rounded-lg border border-outline-gray-modals bg-surface-white p-4 hover:border-outline-gray-3 transition-colors"
            @click="openEditTemplate(tpl.name)"
          >
            <div class="flex items-start justify-between mb-2">
              <p class="text-sm font-medium text-ink-gray-8">{{ tpl.template_name }}</p>
              <div class="flex gap-1.5">
                <Badge :label="channelLabel[tpl.channel] || tpl.channel" :theme="channelTheme[tpl.channel] || 'gray'" size="sm" />
                <Badge v-if="!tpl.is_active" label="Tắt" theme="red" size="sm" />
              </div>
            </div>
            <p class="text-xs text-ink-gray-5 mb-3">{{ tpl.template_type || '—' }}</p>
            <p class="text-xs text-ink-gray-4 line-clamp-3" v-html="stripHtml(tpl.content)" />
            <div class="mt-3 flex items-center justify-between border-t border-outline-gray-1 pt-2">
              <span class="text-xs text-ink-gray-4">Đã dùng {{ tpl.usage_count || 0 }} lần</span>
              <span v-if="tpl.char_count" class="text-xs text-ink-gray-4">~{{ tpl.char_count }} ký tự</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
        <FeatherIcon name="file-text" class="h-10 w-10" />
        <p class="text-sm font-medium text-ink-gray-5">Chưa có mẫu tin nhắn nào</p>
        <p class="text-xs">Tạo mẫu để gửi nhanh cho khách hàng qua Zalo hoặc SMS</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createListResource, Badge, FeatherIcon, Button } from 'frappe-ui'
import { ref, watch, onMounted } from 'vue'

const activeMainTab = ref('history')
const activeChannel = ref('all')
const activeStatus = ref('all')

const mainTabs = [
  { id: 'history', label: 'Lịch sử gửi' },
  { id: 'templates', label: 'Mẫu tin nhắn' },
]

const channelTabs = [
  { id: 'all', label: 'Tất cả' },
  { id: 'zalo', label: 'Zalo' },
  { id: 'sms', label: 'SMS' },
]

const statusPills = [
  { id: 'all', label: 'Tất cả' },
  { id: 'pending', label: 'Chờ gửi' },
  { id: 'sent', label: 'Đã gửi' },
  { id: 'failed', label: 'Thất bại' },
]

const channelLabel = { zalo: 'Zalo', sms: 'SMS' }
const channelTheme = { zalo: 'blue', sms: 'green' }
const triggerLabel = {
  appointment_reminder: 'Nhắc lịch hẹn',
  followup: 'Theo dõi sau khám',
  birthday: 'Chúc mừng sinh nhật',
  promotion: 'Ưu đãi',
  manual: 'Thủ công',
}
const sendStatusLabel = { pending: 'Chờ gửi', sent: 'Đã gửi', failed: 'Thất bại' }
const sendStatusTheme = { pending: 'gray', sent: 'green', failed: 'red' }

const historyList = createListResource({
  doctype: 'CSKH Care Event',
  fields: ['name', 'contact_name', 'contact_phone', 'channel', 'trigger_type', 'scheduled_at', 'status'],
  orderBy: 'scheduled_at desc',
  pageLength: 100,
})

const templateList = createListResource({
  doctype: 'Message Template',
  fields: ['name', 'template_name', 'channel', 'template_type', 'content', 'is_active', 'usage_count', 'char_count'],
  orderBy: 'template_name asc',
  pageLength: 50,
  auto: true,
})

function buildHistoryFilters() {
  const filters = {}
  if (activeChannel.value !== 'all') filters.channel = activeChannel.value
  if (activeStatus.value !== 'all') filters.status = activeStatus.value
  return filters
}

function applyHistoryFilters() {
  historyList.update({ filters: buildHistoryFilters() })
  historyList.reload()
}

watch([activeChannel, activeStatus], applyHistoryFilters)
onMounted(applyHistoryFilters)

const { showModal } = useDoctypeModal()

function openCreate() {
  if (activeMainTab.value === 'history') {
    showModal({
      doctype: 'CSKH Care Event',
      title: 'Tạo lịch gửi',
      callbacks: { afterInsert: () => historyList.reload() },
    })
  } else {
    showModal({
      doctype: 'Message Template',
      title: 'Tạo mẫu tin nhắn',
      callbacks: { afterInsert: () => templateList.reload() },
    })
  }
}

function openEditHistory(name) {
  showModal({
    doctype: 'CSKH Care Event',
    name,
    title: 'Lịch gửi tin nhắn',
    callbacks: { afterUpdate: () => historyList.reload() },
  })
}

function openEditTemplate(name) {
  showModal({
    doctype: 'Message Template',
    name,
    title: 'Mẫu tin nhắn',
    callbacks: { afterUpdate: () => templateList.reload() },
  })
}

function stripHtml(html) {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
}

function formatDateTime(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString('vi-VN', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  } catch {
    return ts
  }
}
</script>
