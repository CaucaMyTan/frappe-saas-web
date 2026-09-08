<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Chiến dịch FB Lead</h3>
    </template>
    <template #right-header>
      <Button variant="outline" label="Làm mới" iconLeft="refresh-cw" @click="loadCampaigns" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div v-if="loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="campaigns.length" class="flex-1 overflow-auto">
      <table class="w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tên chiến dịch</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">FB Page</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Leads</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Đã gọi</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Đặt lịch</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Ngày tạo</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in campaigns"
            :key="row.id"
            class="border-b border-outline-gray-modals hover:bg-surface-gray-1"
          >
            <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.name || '—' }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-7">{{ row.fb_page_name || '—' }}</td>
            <td class="px-4 py-3">
              <Badge
                :label="fbStatusLabel[row.status] || row.status || '—'"
                :theme="fbStatusTheme[row.status] || 'gray'"
                size="sm"
              />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.leads_count || 0 }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.called_count || 0 }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.booked_count || 0 }}</td>
            <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatTime(row.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="facebook" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">Chưa có chiến dịch FB nào</p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Badge, FeatherIcon, Button, call } from 'frappe-ui'
import { ref, onMounted } from 'vue'

const fbStatusLabel = {
  active: 'Đang chạy',
  paused: 'Tạm dừng',
  ended: 'Kết thúc',
}

const fbStatusTheme = {
  active: 'green',
  paused: 'yellow',
  ended: 'gray',
}

const campaigns = ref([])
const loading = ref(false)

async function loadCampaigns() {
  loading.value = true
  try {
    const result = await call('voice_crm.api.proxy_get_fb_campaigns', { limit: 50 })
    campaigns.value = Array.isArray(result) ? result : []
  } catch (e) {
    console.error('Lỗi tải FB campaigns:', e)
    campaigns.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadCampaigns)

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
