<template>
  <Dialog v-model="isOpen" :options="{ size: '2xl' }">
    <template #body>
      <div class="bg-surface-white rounded-xl overflow-hidden">
        <!-- Header -->
        <div class="px-6 pt-5 pb-4 border-b border-outline-gray-modals flex items-start justify-between">
          <div class="flex-1 min-w-0 pr-4">
            <div class="flex items-center gap-2">
              <h3 class="text-lg font-semibold text-ink-gray-9 truncate">{{ campaign?.name || '—' }}</h3>
              <Badge
                :label="statusLabel[campaign?.status] || campaign?.status || '—'"
                :theme="statusTheme[campaign?.status] || 'gray'"
                size="sm"
              />
            </div>
            <p v-if="campaign?.description" class="text-sm text-ink-gray-5 mt-0.5">{{ campaign.description }}</p>
          </div>
          <Button variant="ghost" icon="x" @click="close" />
        </div>

        <!-- Loading detail -->
        <div v-if="loading" class="flex items-center justify-center py-16">
          <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
        </div>

        <template v-else-if="detail">
          <!-- KPI bar -->
          <div class="grid grid-cols-5 border-b border-outline-gray-modals">
            <div v-for="kpi in kpis" :key="kpi.label" class="px-4 py-3 text-center border-r border-outline-gray-modals last:border-0">
              <div class="text-xl font-bold" :class="kpi.color">{{ kpi.value }}</div>
              <div class="text-xs text-ink-gray-5 mt-0.5">{{ kpi.label }}</div>
            </div>
          </div>

          <!-- Progress bar -->
          <div class="px-6 py-3 border-b border-outline-gray-modals">
            <div class="flex items-center justify-between text-xs text-ink-gray-5 mb-1">
              <span>Tiến độ gọi</span>
              <span>{{ detail.called_count || 0 }} / {{ detail.total_count || 0 }}</span>
            </div>
            <div class="w-full h-2 bg-surface-gray-2 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all"
                :class="detail.status === 'running' ? 'bg-green-500' : 'bg-ink-gray-6'"
                :style="{ width: progressPct + '%' }"
              />
            </div>
          </div>

          <!-- Action buttons -->
          <div class="px-6 py-3 border-b border-outline-gray-modals flex items-center gap-2">
            <Button
              v-if="detail.status === 'draft' || detail.status === 'paused'"
              variant="solid"
              label="Chạy ngay"
              iconLeft="play"
              size="sm"
              :loading="actionLoading === 'run'"
              @click="runCampaign"
            />
            <Button
              v-if="detail.status === 'running'"
              variant="outline"
              label="Tạm dừng"
              iconLeft="pause"
              size="sm"
              :loading="actionLoading === 'pause'"
              @click="pauseCampaign"
            />
            <Button
              v-if="detail.status === 'running' || detail.status === 'paused'"
              variant="outline"
              label="Dừng hẳn"
              iconLeft="square"
              size="sm"
              :loading="actionLoading === 'stop'"
              @click="stopCampaign"
            />
            <div class="flex-1" />
            <Button
              variant="ghost"
              label="Xóa chiến dịch"
              iconLeft="trash-2"
              size="sm"
              theme="red"
              :loading="actionLoading === 'delete'"
              @click="deleteCampaign"
            />
          </div>

          <!-- Results section -->
          <div class="px-6 pt-4 pb-2">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-semibold text-ink-gray-8">Kết quả từng số</h4>
              <!-- Result filter tabs -->
              <div class="flex gap-1 p-0.5 bg-surface-gray-2 rounded-lg text-xs">
                <button
                  v-for="f in resultFilters"
                  :key="f.id"
                  @click="resultFilter = f.id"
                  class="px-2.5 py-1 rounded-md transition-colors"
                  :class="resultFilter === f.id ? 'bg-surface-white shadow-sm font-medium text-ink-gray-9' : 'text-ink-gray-5 hover:text-ink-gray-7'"
                >{{ f.label }} ({{ f.count }})</button>
              </div>
            </div>

            <!-- Results table -->
            <div class="max-h-64 overflow-y-auto border border-outline-gray-modals rounded-lg">
              <table class="w-full border-collapse text-sm">
                <thead class="sticky top-0 bg-surface-gray-1">
                  <tr>
                    <th class="px-3 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Tên</th>
                    <th class="px-3 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Số điện thoại</th>
                    <th class="px-3 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Trạng thái</th>
                    <th class="px-3 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Kết quả</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(r, i) in filteredResults"
                    :key="i"
                    class="border-t border-outline-gray-modals hover:bg-surface-gray-1"
                  >
                    <td class="px-3 py-2 font-medium text-ink-gray-8">{{ r.name || '—' }}</td>
                    <td class="px-3 py-2 font-mono text-ink-gray-6">{{ r.phone }}</td>
                    <td class="px-3 py-2">
                      <Badge
                        :label="resultStatusLabel[r.status] || r.status || 'Chờ'"
                        :theme="resultStatusTheme[r.status] || 'gray'"
                        size="sm"
                      />
                    </td>
                    <td class="px-3 py-2">
                      <Badge
                        v-if="r.call_outcome"
                        :label="outcomeLabel[r.call_outcome] || r.call_outcome"
                        :theme="outcomeTheme[r.call_outcome] || 'gray'"
                        size="sm"
                      />
                      <span v-else-if="r.error" class="text-xs text-red-500 truncate max-w-32 block">{{ r.error }}</span>
                      <span v-else class="text-xs text-ink-gray-3">—</span>
                    </td>
                  </tr>
                  <!-- Show pending contacts that haven't been called yet -->
                  <template v-if="resultFilter === 'all' || resultFilter === 'pending'">
                    <tr
                      v-for="(c, i) in pendingContacts"
                      :key="'p' + i"
                      class="border-t border-outline-gray-modals hover:bg-surface-gray-1"
                    >
                      <td class="px-3 py-2 font-medium text-ink-gray-6">{{ c.name || '—' }}</td>
                      <td class="px-3 py-2 font-mono text-ink-gray-5">{{ c.phone }}</td>
                      <td class="px-3 py-2">
                        <Badge label="Chờ gọi" theme="gray" size="sm" />
                      </td>
                      <td class="px-3 py-2 text-xs text-ink-gray-3">—</td>
                    </tr>
                  </template>
                  <tr v-if="!filteredResults.length && (!pendingContacts.length || (resultFilter !== 'all' && resultFilter !== 'pending'))">
                    <td colspan="4" class="px-3 py-8 text-center text-sm text-ink-gray-4">
                      Chưa có kết quả cho bộ lọc này
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Footer meta -->
          <div class="px-6 py-3 text-xs text-ink-gray-4 flex gap-4">
            <span>Tạo: {{ formatTime(detail.created_at) }}</span>
            <span v-if="detail.started_at">Bắt đầu: {{ formatTime(detail.started_at) }}</span>
            <span v-if="detail.completed_at">Hoàn thành: {{ formatTime(detail.completed_at) }}</span>
            <span>Delay: {{ (detail.delay_ms || 3000) / 1000 }}s</span>
          </div>
        </template>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { Dialog, Badge, Button, FeatherIcon, call, toast } from 'frappe-ui'
import { ref, computed, watch } from 'vue'

const props = defineProps({ campaign: Object, show: Boolean })
const emit = defineEmits(['close', 'updated'])

const isOpen = computed({
  get: () => props.show,
  set: (v) => { if (!v) emit('close') },
})

const detail = ref(null)
const loading = ref(false)
const actionLoading = ref('')
const resultFilter = ref('all')

// ── Status maps ───────────────────────────────
const statusLabel = {
  draft: 'Nháp', running: 'Đang chạy', paused: 'Tạm dừng', completed: 'Hoàn thành',
}
const statusTheme = {
  draft: 'gray', running: 'green', paused: 'yellow', completed: 'blue',
}
const resultStatusLabel = {
  pending: 'Chờ', calling: 'Đang gọi', done: 'Xong', error: 'Lỗi',
}
const resultStatusTheme = {
  pending: 'gray', calling: 'yellow', done: 'green', error: 'red',
}
const outcomeLabel = {
  booked: 'Đặt lịch', no_answer: 'Không nghe', rejected: 'Từ chối',
}
const outcomeTheme = {
  booked: 'green', no_answer: 'gray', rejected: 'red',
}

// ── Load detail ───────────────────────────────
async function loadDetail() {
  if (!props.campaign?.id) return
  loading.value = true
  try {
    detail.value = await call('voice_crm.api.proxy_get_campaign_detail', { campaign_id: props.campaign.id })
  } catch (e) {
    console.error('Lỗi tải chi tiết chiến dịch:', e)
  } finally {
    loading.value = false
  }
}

watch(() => props.show, (v) => {
  if (v) {
    resultFilter.value = 'all'
    loadDetail()
  }
})

// ── KPIs ──────────────────────────────────────
const kpis = computed(() => {
  if (!detail.value) return []
  const d = detail.value
  const rate = d.total_count ? Math.round(((d.booked_count || 0) / d.total_count) * 100) : 0
  return [
    { label: 'Tổng số', value: d.total_count || 0, color: 'text-ink-gray-9' },
    { label: 'Đã gọi', value: d.called_count || 0, color: 'text-ink-gray-7' },
    { label: 'Đặt lịch', value: d.booked_count || 0, color: 'text-green-600' },
    { label: 'Không nghe', value: d.no_answer_count || 0, color: 'text-ink-gray-5' },
    { label: 'Tỉ lệ', value: rate + '%', color: rate > 20 ? 'text-green-600' : 'text-ink-gray-7' },
  ]
})

const progressPct = computed(() => {
  if (!detail.value?.total_count) return 0
  return Math.min(100, Math.round(((detail.value.called_count || 0) / detail.value.total_count) * 100))
})

// ── Results filtering ─────────────────────────
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
  if (resultFilter.value === 'all' || resultFilter.value === 'pending') return allResults.value
  if (resultFilter.value === 'booked') return allResults.value.filter(r => r.call_outcome === 'booked')
  if (resultFilter.value === 'no_answer') return allResults.value.filter(r => r.call_outcome === 'no_answer')
  if (resultFilter.value === 'error') return allResults.value.filter(r => r.status === 'error')
  return allResults.value
})

// ── Actions ───────────────────────────────────
async function runCampaign() {
  actionLoading.value = 'run'
  try {
    await call('voice_crm.api.proxy_update_campaign', { campaign_id: detail.value.id, status: 'running' })
    await call('voice_crm.api.proxy_run_campaign', { campaign_id: detail.value.id })
    toast({ title: 'Đã kích hoạt chiến dịch', variant: 'success' })
    await loadDetail()
    emit('updated')
  } catch (e) {
    toast({ title: 'Lỗi: ' + (e.message || e), variant: 'error' })
  } finally {
    actionLoading.value = ''
  }
}

async function pauseCampaign() {
  actionLoading.value = 'pause'
  try {
    await call('voice_crm.api.proxy_update_campaign', { campaign_id: detail.value.id, status: 'paused' })
    toast({ title: 'Đã tạm dừng chiến dịch', variant: 'success' })
    await loadDetail()
    emit('updated')
  } catch (e) {
    toast({ title: 'Lỗi: ' + (e.message || e), variant: 'error' })
  } finally {
    actionLoading.value = ''
  }
}

async function stopCampaign() {
  actionLoading.value = 'stop'
  try {
    await call('voice_crm.api.proxy_update_campaign', { campaign_id: detail.value.id, status: 'completed' })
    toast({ title: 'Đã dừng chiến dịch', variant: 'success' })
    await loadDetail()
    emit('updated')
  } catch (e) {
    toast({ title: 'Lỗi: ' + (e.message || e), variant: 'error' })
  } finally {
    actionLoading.value = ''
  }
}

async function deleteCampaign() {
  if (!confirm(`Xóa chiến dịch "${detail.value?.name}"? Hành động này không thể hoàn tác.`)) return
  actionLoading.value = 'delete'
  try {
    await call('voice_crm.api.proxy_delete_campaign', { campaign_id: detail.value.id })
    toast({ title: 'Đã xóa chiến dịch', variant: 'success' })
    emit('updated')
    close()
  } catch (e) {
    toast({ title: 'Lỗi xóa: ' + (e.message || e), variant: 'error' })
  } finally {
    actionLoading.value = ''
  }
}

function close() {
  emit('close')
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
