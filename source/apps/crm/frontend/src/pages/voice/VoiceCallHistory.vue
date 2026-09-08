<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Lịch sử Gọi</h3>
    </template>
    <template #right-header>
      <Button variant="outline" label="Làm mới" iconLeft="refresh-cw" size="sm" @click="loadCalls" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">

    <!-- Filter bar — stacked on mobile -->
    <div class="border-b border-outline-gray-modals bg-surface-white px-4 py-2 flex flex-wrap items-center gap-2">
      <div class="flex gap-1 p-0.5 bg-surface-gray-2 rounded-lg text-xs">
        <button
          v-for="f in directionFilters"
          :key="f.id"
          @click="directionFilter = f.id"
          class="px-2.5 py-1 rounded-md transition-colors"
          :class="directionFilter === f.id ? 'bg-surface-white shadow-sm font-medium text-ink-gray-9' : 'text-ink-gray-5 hover:text-ink-gray-7'"
        >{{ f.label }}</button>
      </div>
      <div class="flex gap-1 p-0.5 bg-surface-gray-2 rounded-lg text-xs">
        <button
          v-for="f in statusFilters"
          :key="f.id"
          @click="statusFilter = f.id"
          class="px-2.5 py-1 rounded-md transition-colors"
          :class="statusFilter === f.id ? 'bg-surface-white shadow-sm font-medium text-ink-gray-9' : 'text-ink-gray-5 hover:text-ink-gray-7'"
        >{{ f.label }}</button>
      </div>
      <span class="text-xs text-ink-gray-4 ml-auto">{{ filteredCalls.length }} cuộc</span>
    </div>

    <!-- Table -->
    <div v-if="loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="filteredCalls.length" class="flex-1 overflow-auto">
      <!-- Desktop table -->
      <table class="hidden md:table w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tên khách</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Số gọi đến</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Hướng</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời lượng</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời gian</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tóm tắt AI</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filteredCalls" :key="row.id" class="border-b border-outline-gray-modals hover:bg-surface-gray-1">
            <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.contact_name || '—' }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-7 font-mono">{{ row.contact_phone || '—' }}</td>
            <td class="px-4 py-3">
              <Badge :label="row.direction === 'inbound' ? 'Gọi đến' : 'Gọi ra'" :theme="row.direction === 'inbound' ? 'blue' : 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3">
              <Badge :label="callStatusLabel[row.status] || row.status || '—'" :theme="callStatusTheme[row.status] || 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ formatDuration(row.duration_seconds) }}</td>
            <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatTime(row.created_at) }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-5 max-w-[220px] truncate">{{ row.summary || '—' }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile cards -->
      <div class="md:hidden divide-y divide-outline-gray-modals">
        <div v-for="row in filteredCalls" :key="row.id" class="px-4 py-3.5">
          <!-- Row 1: name + badges -->
          <div class="flex items-start justify-between gap-2 mb-1.5">
            <div class="min-w-0">
              <div class="text-sm font-semibold text-ink-gray-9 truncate">{{ row.contact_name || 'Không rõ' }}</div>
              <div class="text-xs font-mono text-ink-gray-6 mt-0.5">{{ row.contact_phone || '—' }}</div>
            </div>
            <div class="flex items-center gap-1 shrink-0">
              <Badge :label="row.direction === 'inbound' ? 'Đến' : 'Ra'" :theme="row.direction === 'inbound' ? 'blue' : 'gray'" size="sm" />
              <Badge :label="callStatusLabel[row.status] || row.status || '—'" :theme="callStatusTheme[row.status] || 'gray'" size="sm" />
            </div>
          </div>
          <!-- Row 2: duration + time + summary -->
          <div class="flex items-center gap-3 text-xs text-ink-gray-5">
            <span v-if="row.duration_seconds">⏱ {{ formatDuration(row.duration_seconds) }}</span>
            <span>{{ formatTime(row.created_at) }}</span>
          </div>
          <div v-if="row.summary" class="mt-1 text-xs text-ink-gray-5 line-clamp-2">{{ row.summary }}</div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="phone-missed" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">Không có cuộc gọi nào</p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Badge, FeatherIcon, Button, call } from 'frappe-ui'
import { ref, computed, onMounted } from 'vue'

const calls = ref([])
const loading = ref(false)
const directionFilter = ref('all')
const statusFilter = ref('all')

const directionFilters = [
  { id: 'all', label: 'Tất cả' },
  { id: 'inbound', label: 'Gọi đến' },
  { id: 'outbound', label: 'Gọi ra' },
]
const statusFilters = [
  { id: 'all', label: 'Tất cả' },
  { id: 'completed', label: 'Hoàn thành' },
  { id: 'no_answer', label: 'Không nghe' },
]

const callStatusLabel = {
  completed: 'Hoàn thành', no_answer: 'Không nghe',
  busy: 'Đang bận', failed: 'Thất bại', voicemail: 'Hộp thư thoại',
}
const callStatusTheme = {
  completed: 'green', no_answer: 'red', busy: 'yellow', failed: 'red', voicemail: 'gray',
}

// Merge call_started (no_answer, has contact info) + call_ended (completed, has duration)
// using retell_call_id as the join key
function mergeCalls(raw) {
  const groups = {}
  const orphans = []

  for (const c of raw) {
    if (!c.retell_call_id) { orphans.push(c); continue }
    if (!groups[c.retell_call_id]) groups[c.retell_call_id] = []
    groups[c.retell_call_id].push(c)
  }

  const result = []
  for (const records of Object.values(groups)) {
    if (records.length === 1) { result.push(records[0]); continue }
    const completed = records.find(r => r.status === 'completed')
    const noAnswer  = records.find(r => r.status === 'no_answer')
    if (completed && noAnswer) {
      result.push({
        ...completed,
        contact_name:  completed.contact_name  || noAnswer.contact_name,
        contact_phone: completed.contact_phone || noAnswer.contact_phone,
      })
    } else {
      // unexpected pair — keep the one with most info
      result.push(records.reduce((best, r) =>
        (r.contact_name || r.duration_seconds) ? r : best
      ))
    }
  }

  result.push(...orphans)
  result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  return result
}

const mergedCalls = computed(() => mergeCalls(calls.value))

const filteredCalls = computed(() => {
  let list = mergedCalls.value
  if (directionFilter.value !== 'all') list = list.filter(c => c.direction === directionFilter.value)
  if (statusFilter.value !== 'all') list = list.filter(c => c.status === statusFilter.value)
  return list
})

async function loadCalls() {
  loading.value = true
  try {
    const result = await call('voice_crm.api.proxy_get_calls', { limit: 500 })
    calls.value = Array.isArray(result) ? result : []
  } catch (e) {
    console.error('Lỗi tải lịch sử gọi:', e)
    calls.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadCalls)

function formatDuration(secs) {
  if (!secs) return '—'
  const m = Math.floor(secs / 60)
  const s = secs % 60
  return m > 0 ? `${m}p ${s}s` : `${s}s`
}

function formatTime(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString('vi-VN', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })
  } catch { return ts }
}
</script>
