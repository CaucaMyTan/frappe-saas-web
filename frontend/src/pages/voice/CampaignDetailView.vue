<template>
  <div class="flex flex-1 flex-col overflow-hidden">

    <!-- Loading -->
    <div v-if="loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <template v-else-if="detail">
      <!-- KPI bar -->
      <div class="grid grid-cols-5 border-b border-outline-gray-modals bg-surface-white shrink-0">
        <div
          v-for="kpi in kpis"
          :key="kpi.label"
          class="px-5 py-4 text-center border-r border-outline-gray-modals last:border-0"
        >
          <div class="text-2xl font-bold" :class="kpi.color">{{ kpi.value }}</div>
          <div class="text-xs text-ink-gray-5 mt-0.5">{{ kpi.label }}</div>
        </div>
      </div>

      <!-- Progress + meta bar -->
      <div class="px-6 py-3 border-b border-outline-gray-modals bg-surface-gray-1 flex items-center gap-6 shrink-0">
        <div class="flex-1">
          <div class="flex items-center justify-between text-xs text-ink-gray-5 mb-1">
            <span>Tiến độ gọi</span>
            <span>{{ detail.called_count || 0 }} / {{ detail.total_count || 0 }}</span>
          </div>
          <div class="w-full h-2.5 bg-surface-gray-3 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500"
              :class="detail.status === 'running' ? 'bg-green-500' : 'bg-ink-gray-6'"
              :style="{ width: progressPct + '%' }"
            />
          </div>
        </div>
        <div class="text-xs text-ink-gray-4 flex gap-4 shrink-0">
          <span>Agent: <strong class="text-ink-gray-7">{{ detail.agent_label || detail.agent_key || '—' }}</strong></span>
          <span>Delay: <strong class="text-ink-gray-7">{{ (detail.delay_ms || 3000) / 1000 }}s</strong></span>
          <span v-if="detail.started_at">Bắt đầu: <strong class="text-ink-gray-7">{{ formatTime(detail.started_at) }}</strong></span>
        </div>
      </div>

      <!-- Action bar -->
      <div class="px-6 py-3 border-b border-outline-gray-modals bg-surface-white flex items-center gap-3 shrink-0">
        <!-- Not running: show Run button -->
        <Button
          v-if="!isRunning && (detail.status === 'draft' || detail.status === 'paused')"
          variant="solid"
          label="Chạy ngay"
          iconLeft="play"
          @click="startRunLoop"
        />

        <!-- Running: show live progress + pause -->
        <template v-if="isRunning">
          <div class="flex items-center gap-2 text-sm font-medium text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse shrink-0" />
            Đang gọi {{ runProgress.current }} / {{ runProgress.total }}
          </div>
          <Button
            variant="outline"
            label="Tạm dừng"
            iconLeft="pause"
            @click="requestPause"
          />
          <Button
            variant="ghost"
            label="Dừng hẳn"
            iconLeft="square"
            @click="requestStop"
          />
        </template>

        <!-- Completed status -->
        <div
          v-if="!isRunning && detail.status === 'completed'"
          class="text-xs text-ink-gray-5 bg-surface-gray-1 rounded-lg px-3 py-1.5"
        >
          Chiến dịch đã hoàn thành
        </div>

        <div class="flex-1" />
        <span class="text-xs text-ink-gray-4">
          Tạo: {{ formatTime(detail.created_at) }}
          <span v-if="detail.completed_at"> · Hoàn thành: {{ formatTime(detail.completed_at) }}</span>
        </span>
        <Button
          variant="ghost"
          label="Xóa"
          iconLeft="trash-2"
          theme="red"
          size="sm"
          :disabled="isRunning"
          :loading="actionLoading === 'delete'"
          @click="deleteCampaign"
        />
      </div>

      <!-- Results section -->
      <div class="flex flex-1 flex-col overflow-hidden px-6 pt-4">
        <!-- Result filter + description -->
        <div class="flex items-center justify-between mb-3 shrink-0">
          <h4 class="text-sm font-semibold text-ink-gray-8">Kết quả từng liên hệ</h4>
          <div class="flex gap-1 p-0.5 bg-surface-gray-2 rounded-lg">
            <button
              v-for="f in resultFilters"
              :key="f.id"
              @click="resultFilter = f.id"
              class="px-3 py-1 rounded-md text-xs transition-colors"
              :class="resultFilter === f.id
                ? 'bg-surface-white shadow-sm font-medium text-ink-gray-9'
                : 'text-ink-gray-5 hover:text-ink-gray-7'"
            >
              {{ f.label }}
              <span class="ml-0.5 text-ink-gray-4">({{ f.count }})</span>
            </button>
          </div>
        </div>

        <!-- Results table -->
        <div class="flex-1 overflow-auto border border-outline-gray-modals rounded-xl">
          <table class="w-full border-collapse text-sm">
            <thead class="sticky top-0 bg-surface-gray-1 z-10">
              <tr>
                <th class="px-4 py-2.5 text-left text-xs font-medium text-ink-gray-5 uppercase tracking-wide border-b border-outline-gray-modals">Tên</th>
                <th class="px-4 py-2.5 text-left text-xs font-medium text-ink-gray-5 uppercase tracking-wide border-b border-outline-gray-modals">Số điện thoại</th>
                <th class="px-4 py-2.5 text-left text-xs font-medium text-ink-gray-5 uppercase tracking-wide border-b border-outline-gray-modals">Trạng thái</th>
                <th class="px-4 py-2.5 text-left text-xs font-medium text-ink-gray-5 uppercase tracking-wide border-b border-outline-gray-modals">Kết quả</th>
                <th class="px-4 py-2.5 text-left text-xs font-medium text-ink-gray-5 uppercase tracking-wide border-b border-outline-gray-modals">Call ID</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(r, i) in filteredResults"
                :key="'r' + i"
                class="border-b border-outline-gray-modals last:border-0 hover:bg-surface-gray-1"
              >
                <td class="px-4 py-3 font-medium text-ink-gray-8">{{ r.name || '—' }}</td>
                <td class="px-4 py-3 font-mono text-ink-gray-6">{{ r.phone }}</td>
                <td class="px-4 py-3">
                  <Badge
                    :label="resultStatusLabel[r.status] || r.status || 'Chờ'"
                    :theme="resultStatusTheme[r.status] || 'gray'"
                    size="sm"
                  />
                </td>
                <td class="px-4 py-3">
                  <Badge
                    v-if="r.call_outcome"
                    :label="outcomeLabel[r.call_outcome] || r.call_outcome"
                    :theme="outcomeTheme[r.call_outcome] || 'gray'"
                    size="sm"
                  />
                  <span v-else-if="r.error" class="text-xs text-red-500 max-w-40 block truncate" :title="r.error">{{ r.error }}</span>
                  <span v-else class="text-xs text-ink-gray-3">—</span>
                </td>
                <td class="px-4 py-3 text-xs font-mono text-ink-gray-4 truncate max-w-36">{{ r.call_id || '—' }}</td>
              </tr>

              <!-- Pending (not yet called) contacts -->
              <template v-if="resultFilter === 'all' || resultFilter === 'pending'">
                <tr
                  v-for="(c, i) in pendingContacts"
                  :key="'p' + i"
                  class="border-b border-outline-gray-modals last:border-0 hover:bg-surface-gray-1"
                >
                  <td class="px-4 py-3 text-ink-gray-6">{{ c.name || '—' }}</td>
                  <td class="px-4 py-3 font-mono text-ink-gray-5">{{ c.phone }}</td>
                  <td class="px-4 py-3">
                    <Badge label="Chờ gọi" theme="gray" size="sm" />
                  </td>
                  <td class="px-4 py-3 text-xs text-ink-gray-3">—</td>
                  <td class="px-4 py-3 text-xs text-ink-gray-3">—</td>
                </tr>
              </template>

              <tr v-if="filteredResults.length === 0 && (resultFilter !== 'all' && resultFilter !== 'pending' || pendingContacts.length === 0)">
                <td colspan="5" class="px-4 py-12 text-center text-sm text-ink-gray-4">
                  Chưa có kết quả cho bộ lọc này
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="py-2 shrink-0" />
      </div>
    </template>

    <div v-else class="flex flex-1 items-center justify-center text-sm text-ink-gray-4">
      Không tải được dữ liệu chiến dịch
    </div>
  </div>
</template>

<script setup>
import { Badge, Button, FeatherIcon, call, toast } from 'frappe-ui'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({ campaign: Object })
const emit = defineEmits(['back', 'updated', 'deleted'])

const detail = ref(null)
const loading = ref(false)
const actionLoading = ref('')
const resultFilter = ref('all')

// ── Status maps ───────────────────────────────
const resultStatusLabel = { pending: 'Chờ', calling: 'Đang gọi', done: 'Xong', error: 'Lỗi' }
const resultStatusTheme = { pending: 'gray', calling: 'yellow', done: 'green', error: 'red' }
const outcomeLabel = { booked: 'Đặt lịch', no_answer: 'Không nghe', rejected: 'Từ chối' }
const outcomeTheme = { booked: 'green', no_answer: 'gray', rejected: 'red' }

// ── Load ──────────────────────────────────────
async function loadDetail() {
  if (!props.campaign?.id) return
  loading.value = true
  try {
    detail.value = await call('voice_crm.api.proxy_get_campaign_detail', {
      campaign_id: props.campaign.id,
    })
  } catch (e) {
    console.error('Lỗi tải chi tiết:', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadDetail)
watch(() => props.campaign?.id, loadDetail)

// ── KPIs ──────────────────────────────────────
const kpis = computed(() => {
  if (!detail.value) return []
  const d = detail.value
  const total = isRunning.value ? runProgress.value.total : (d.total_count || 0)
  const called = isRunning.value ? runProgress.value.called : (d.called_count || 0)
  const rate = total ? Math.round(((d.booked_count || 0) / total) * 100) : 0
  return [
    { label: 'Tổng số', value: total, color: 'text-ink-gray-9' },
    { label: 'Đã gọi', value: called, color: 'text-ink-gray-7' },
    { label: 'Đặt lịch', value: d.booked_count || 0, color: 'text-green-600' },
    { label: 'Không nghe', value: d.no_answer_count || 0, color: 'text-ink-gray-5' },
    { label: 'Tỉ lệ', value: rate + '%', color: rate >= 20 ? 'text-green-600' : 'text-ink-gray-7' },
  ]
})

const progressPct = computed(() => {
  if (isRunning.value && runProgress.value.total) {
    return Math.min(100, Math.round((runProgress.value.called / runProgress.value.total) * 100))
  }
  if (!detail.value?.total_count) return 0
  return Math.min(100, Math.round(((detail.value.called_count || 0) / detail.value.total_count) * 100))
})

// ── Results ───────────────────────────────────
const allResults = computed(() => Array.isArray(detail.value?.results) ? detail.value.results : [])

const pendingContacts = computed(() => {
  if (!detail.value) return []
  const calledPhones = new Set(allResults.value.map(r => r.phone))
  return (detail.value.contacts || []).filter(c => !calledPhones.has(c.phone))
})

const resultFilters = computed(() => [
  { id: 'all', label: 'Tất cả', count: allResults.value.length + pendingContacts.value.length },
  { id: 'pending', label: 'Chờ gọi', count: pendingContacts.value.length },
  { id: 'booked', label: 'Đặt lịch', count: allResults.value.filter(r => r.call_outcome === 'booked').length },
  { id: 'no_answer', label: 'Không nghe', count: allResults.value.filter(r => r.call_outcome === 'no_answer').length },
  { id: 'error', label: 'Lỗi', count: allResults.value.filter(r => r.status === 'error').length },
])

const filteredResults = computed(() => {
  switch (resultFilter.value) {
    case 'booked': return allResults.value.filter(r => r.call_outcome === 'booked')
    case 'no_answer': return allResults.value.filter(r => r.call_outcome === 'no_answer')
    case 'error': return allResults.value.filter(r => r.status === 'error')
    default: return allResults.value
  }
})

// ── Browser-side run loop (giống Vercel) ──────
// Retell được gọi trực tiếp từng số, n8n nhận webhook từ Retell để cập nhật results
const isRunning = ref(false)
const runProgress = ref({ current: 0, total: 0, called: 0 })
let stopSignal = false   // 'pause' | 'stop' | false
let stopMode = null

async function startRunLoop() {
  if (!detail.value) return
  const contacts = detail.value.contacts || []
  if (!contacts.length) {
    toast({ title: 'Chiến dịch không có liên hệ nào', variant: 'error' })
    return
  }

  isRunning.value = true
  stopSignal = false
  stopMode = null
  runProgress.value = { current: 0, total: contacts.length, called: 0 }

  try {
    // Đánh dấu running trong Supabase
    await call('voice_crm.api.proxy_update_campaign', {
      campaign_id: detail.value.id,
      status: 'running',
    })
    if (detail.value) detail.value = { ...detail.value, status: 'running' }

    const agentKey = detail.value.agent_key || 'cold'
    const delayMs = detail.value.delay_ms || 3000

    for (let i = 0; i < contacts.length; i++) {
      if (stopSignal) break

      const contact = contacts[i]
      runProgress.value.current = i + 1

      try {
        await call('voice_crm.api.proxy_trigger_call', {
          phone: contact.phone,
          name: contact.name || '',
          agent_key: agentKey,
        })
        runProgress.value.called++
      } catch (e) {
        console.error(`Lỗi gọi ${contact.phone}:`, e)
        // Tiếp tục với số tiếp theo
      }

      // Delay giữa các cuộc gọi (có thể bị interrupt bởi pause/stop)
      if (i < contacts.length - 1 && !stopSignal) {
        await cancellableDelay(delayMs)
      }
    }

    // Cập nhật trạng thái cuối
    const finalStatus = stopSignal
      ? (stopMode === 'stop' ? 'completed' : 'paused')
      : 'completed'

    await call('voice_crm.api.proxy_update_campaign', {
      campaign_id: detail.value.id,
      status: finalStatus,
    })

    const msg = stopSignal
      ? (stopMode === 'stop' ? `Đã dừng sau ${runProgress.value.called} cuộc gọi` : `Đã tạm dừng sau ${runProgress.value.called} cuộc gọi`)
      : `Hoàn thành! Đã kích hoạt ${runProgress.value.called} cuộc gọi`
    toast({ title: msg, variant: 'success' })

    await loadDetail()
    emit('updated')
  } catch (e) {
    toast({ title: 'Lỗi: ' + (e.message || e), variant: 'error' })
  } finally {
    isRunning.value = false
    stopSignal = false
    stopMode = null
  }
}

// Delay có thể interrupt mỗi 200ms để phản ứng với pause/stop ngay
function cancellableDelay(ms) {
  return new Promise(resolve => {
    const end = Date.now() + ms
    const tick = () => {
      if (stopSignal || Date.now() >= end) return resolve()
      setTimeout(tick, 200)
    }
    tick()
  })
}

function requestPause() {
  stopSignal = true
  stopMode = 'pause'
  toast({ title: 'Đang tạm dừng sau cuộc gọi hiện tại...', variant: 'info' })
}

function requestStop() {
  stopSignal = true
  stopMode = 'stop'
  toast({ title: 'Đang dừng hẳn...', variant: 'info' })
}

// Stop loop nếu user rời khỏi trang
onUnmounted(() => {
  if (isRunning.value) {
    stopSignal = true
    stopMode = 'pause'
  }
})

// ── Delete ────────────────────────────────────
async function deleteCampaign() {
  if (!confirm(`Xóa chiến dịch "${detail.value?.name}"? Không thể hoàn tác.`)) return
  actionLoading.value = 'delete'
  try {
    await call('voice_crm.api.proxy_delete_campaign', { campaign_id: detail.value.id })
    toast({ title: 'Đã xóa chiến dịch', variant: 'success' })
    emit('deleted')
  } catch (e) {
    toast({ title: 'Lỗi xóa: ' + (e.message || e), variant: 'error' })
  } finally {
    actionLoading.value = ''
  }
}

function formatTime(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString('vi-VN', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  } catch { return ts }
}
</script>
