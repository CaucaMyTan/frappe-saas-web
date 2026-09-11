<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Chăm sóc KH (Zalo/SMS)</h3>
    </template>
    <template #right-header>
      <Button variant="outline" label="Làm mới" iconLeft="refresh-cw" @click="loadEvents" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div v-if="loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="events.length" class="flex-1 overflow-auto">
      <!-- Desktop table -->
      <table class="hidden md:table w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Khách hàng</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Số điện thoại</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Kênh</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Loại trigger</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời gian dự kiến</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in events" :key="row.id" class="border-b border-outline-gray-modals hover:bg-surface-gray-1">
            <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.contact_name || '—' }}</td>
            <td class="px-4 py-3 text-sm font-mono text-ink-gray-7">{{ row.contact_phone || '—' }}</td>
            <td class="px-4 py-3">
              <Badge :label="row.channel ? row.channel.toUpperCase() : '—'" :theme="row.channel === 'zalo' ? 'blue' : row.channel === 'sms' ? 'green' : 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.trigger_type || '—' }}</td>
            <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatTime(row.scheduled_at) }}</td>
            <td class="px-4 py-3">
              <Badge :label="cskhStatusLabel[row.status] || row.status || '—'" :theme="cskhStatusTheme[row.status] || 'gray'" size="sm" />
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile cards -->
      <div class="md:hidden divide-y divide-outline-gray-modals">
        <div v-for="row in events" :key="row.id" class="px-4 py-3.5">
          <div class="flex items-start justify-between gap-2 mb-1.5">
            <div class="min-w-0">
              <div class="text-sm font-semibold text-ink-gray-9 truncate">{{ row.contact_name || '—' }}</div>
              <div class="text-xs font-mono text-ink-gray-6 mt-0.5">{{ row.contact_phone || '—' }}</div>
            </div>
            <Badge :label="cskhStatusLabel[row.status] || row.status || '—'" :theme="cskhStatusTheme[row.status] || 'gray'" size="sm" class="shrink-0" />
          </div>
          <div class="flex items-center gap-2 flex-wrap">
            <Badge :label="row.channel ? row.channel.toUpperCase() : '—'" :theme="row.channel === 'zalo' ? 'blue' : row.channel === 'sms' ? 'green' : 'gray'" size="sm" />
            <span class="text-xs text-ink-gray-5">{{ row.trigger_type || '—' }}</span>
            <span class="text-xs text-ink-gray-4 ml-auto">{{ formatTime(row.scheduled_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="message-circle" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">Chưa có sự kiện chăm sóc nào</p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Badge, FeatherIcon, Button, call } from 'frappe-ui'
import { ref, onMounted } from 'vue'

const cskhStatusLabel = {
  pending: 'Chờ gửi',
  sent: 'Đã gửi',
  failed: 'Thất bại',
}

const cskhStatusTheme = {
  pending: 'gray',
  sent: 'green',
  failed: 'red',
}

const events = ref([])
const loading = ref(false)

async function loadEvents() {
  loading.value = true
  try {
    const result = await call('voice_crm.api.proxy_get_cskh_events', { limit: 100 })
    events.value = Array.isArray(result) ? result : []
  } catch (e) {
    console.error('Lỗi tải CSKH events:', e)
    events.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadEvents)

function formatTime(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString('vi-VN', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
    })
  } catch {
    return ts
  }
}
</script>
