<template>
  <!-- ── HEADER ── -->
  <LayoutHeader>
    <template #left-header>
      <!-- List view -->
      <h3 v-if="!selectedCampaign" class="text-lg font-medium text-ink-gray-7">
        Chiến dịch AutoCall
      </h3>
      <!-- Detail view — breadcrumb -->
      <div v-else class="flex items-center gap-1.5">
        <button
          class="text-lg font-medium text-ink-gray-4 hover:text-ink-gray-7 transition-colors"
          @click="backToList"
        >
          Chiến dịch AutoCall
        </button>
        <span class="text-ink-gray-3 text-lg">›</span>
        <span class="text-lg font-medium text-ink-gray-9">{{ selectedCampaign.name }}</span>
        <Badge
          :label="statusLabel[selectedCampaign.status] || selectedCampaign.status"
          :theme="statusTheme[selectedCampaign.status] || 'gray'"
          size="sm"
          class="ml-1"
        />
      </div>
    </template>

    <template #right-header>
      <!-- List header actions -->
      <Button
        v-if="!selectedCampaign"
        variant="outline"
        label="Làm mới"
        iconLeft="refresh-cw"
        size="sm"
        @click="loadCampaigns"
      />
      <!-- Detail header: back button -->
      <Button
        v-else
        variant="ghost"
        label="Quay lại danh sách"
        iconLeft="arrow-left"
        size="sm"
        @click="backToList"
      />
    </template>
  </LayoutHeader>

  <!-- ══ LIST VIEW ══════════════════════════════════════════════ -->
  <template v-if="!selectedCampaign">

    <!-- Stats bar — 2x2 grid on mobile, single row on desktop -->
    <div class="border-b border-outline-gray-modals bg-surface-gray-1 px-4 py-3">
      <div class="grid grid-cols-2 gap-3 md:flex md:items-center md:gap-8">
        <div v-for="s in stats" :key="s.label" class="text-center">
          <div class="text-xl font-bold" :class="s.color">{{ s.value }}</div>
          <div class="text-xs text-ink-gray-5 mt-0.5">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <!-- Manual call box — stacked on mobile, inline on desktop -->
    <div class="border-b border-outline-gray-modals bg-surface-white px-4 py-3">
      <div class="flex items-center gap-1.5 mb-2">
        <div class="w-7 h-7 rounded-full bg-surface-gray-2 flex items-center justify-center shrink-0">
          <FeatherIcon name="phone" class="h-3.5 w-3.5 text-ink-gray-6" />
        </div>
        <span class="text-sm font-medium text-ink-gray-7">Gọi thủ công</span>
      </div>
      <div class="flex flex-col gap-2 md:flex-row md:items-center md:gap-3">
        <input
          v-model="manualName"
          type="text"
          placeholder="Tên khách hàng (tùy chọn)"
          class="w-full md:w-48 rounded-lg border border-outline-gray-modals px-3 py-2 text-sm focus:outline-none focus:border-ink-gray-5"
        />
        <input
          v-model="manualPhone"
          type="tel"
          placeholder="Số điện thoại *"
          class="w-full md:w-44 rounded-lg border border-outline-gray-modals px-3 py-2 text-sm font-mono focus:outline-none focus:border-ink-gray-5"
          @keyup.enter="triggerManualCall"
        />
        <select
          v-model="manualAgentKey"
          class="w-full md:w-auto rounded-lg border border-outline-gray-modals px-3 py-2 text-sm bg-surface-white focus:outline-none focus:border-ink-gray-5"
        >
          <option value="cold">Gọi Lạnh</option>
          <option value="warm">Gọi Ấm</option>
          <option value="cskh">Chăm sóc KH</option>
          <option value="receptionist">Lễ Tân</option>
        </select>
        <div class="flex items-center gap-2">
          <Button
            variant="solid"
            label="Gọi ngay"
            iconLeft="phone-call"
            size="sm"
            :loading="manualCallLoading"
            :disabled="!manualPhone.trim()"
            @click="triggerManualCall"
            class="flex-1 md:flex-none"
          />
          <span v-if="manualCallStatus" class="text-xs text-green-600 font-medium">{{ manualCallStatus }}</span>
        </div>
      </div>
    </div>

    <!-- Filter tabs + create button -->
    <div class="border-b border-outline-gray-modals bg-surface-white px-2 flex items-center justify-between">
      <div class="flex overflow-x-auto scrollbar-none">
        <button
          v-for="tab in statusTabs"
          :key="tab.id"
          class="px-3 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap"
          :class="activeFilter === tab.id
            ? 'border-ink-gray-9 text-ink-gray-9'
            : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'"
          @click="activeFilter = tab.id"
        >
          {{ tab.label }}
          <span
            class="ml-1 text-xs rounded-full px-1.5 py-0.5"
            :class="activeFilter === tab.id ? 'bg-ink-gray-9 text-white' : 'bg-surface-gray-2 text-ink-gray-5'"
          >{{ tab.count }}</span>
        </button>
      </div>
      <Button
        variant="solid"
        label="Tạo"
        iconLeft="plus"
        size="sm"
        class="shrink-0 ml-2"
        @click="showCreate = true"
      />
    </div>

    <!-- Error -->
    <div
      v-if="errorMsg"
      class="mx-4 mt-4 rounded bg-red-50 px-4 py-3 text-sm text-red-700 border border-red-200 flex items-center justify-between shrink-0"
    >
      <span>{{ errorMsg }}</span>
      <button class="ml-2 text-red-400 hover:text-red-600" @click="errorMsg = ''">✕</button>
    </div>

    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Loading -->
      <div v-if="loading" class="flex flex-1 items-center justify-center">
        <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
      </div>

      <!-- Desktop: Table | Mobile: Cards -->
      <div v-else-if="filteredCampaigns.length" class="flex-1 overflow-auto">

        <!-- Desktop table (hidden on mobile) -->
        <table class="hidden md:table w-full border-collapse">
          <thead class="sticky top-0 z-10 bg-surface-white">
            <tr>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tên chiến dịch</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Agent AI</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tiến độ</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Đặt lịch</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Ngày tạo</th>
              <th class="border-b border-outline-gray-modals px-4 py-2.5"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in filteredCampaigns"
              :key="row.id"
              class="border-b border-outline-gray-modals hover:bg-surface-gray-1 cursor-pointer"
              @click="openCampaign(row)"
            >
              <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.name || '—' }}</td>
              <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.agent_label || row.agent_key || '—' }}</td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1.5">
                  <span v-if="row.status === 'running'" class="w-2 h-2 rounded-full bg-green-500 animate-pulse shrink-0" />
                  <Badge :label="statusLabel[row.status] || row.status || '—'" :theme="statusTheme[row.status] || 'gray'" size="sm" />
                </div>
              </td>
              <td class="px-4 py-3 text-sm text-ink-gray-6">
                <div class="flex items-center gap-2">
                  <span class="tabular-nums">{{ row.called_count || 0 }} / {{ row.total_count || 0 }}</span>
                  <div v-if="row.total_count" class="w-16 h-1.5 bg-surface-gray-2 rounded-full overflow-hidden shrink-0">
                    <div
                      class="h-full rounded-full"
                      :class="row.status === 'running' ? 'bg-green-500' : 'bg-ink-gray-5'"
                      :style="{ width: Math.min(100, Math.round(((row.called_count || 0) / row.total_count) * 100)) + '%' }"
                    />
                  </div>
                </div>
              </td>
              <td class="px-4 py-3 text-sm text-ink-gray-6 tabular-nums">{{ row.booked_count || 0 }}</td>
              <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatTime(row.created_at) }}</td>
              <td class="px-4 py-3" @click.stop>
                <Button v-if="row.status === 'draft' || row.status === 'paused'" variant="subtle" label="Chạy" iconLeft="play" size="sm" :loading="runningId === row.id" @click="quickRun(row)" />
                <div v-else-if="row.status === 'running'" class="flex items-center gap-1 text-xs text-green-600 font-medium">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                  Đang chạy
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Mobile cards (hidden on desktop) -->
        <div class="md:hidden divide-y divide-outline-gray-modals">
          <div
            v-for="row in filteredCampaigns"
            :key="row.id"
            class="px-4 py-3.5 active:bg-surface-gray-1 cursor-pointer"
            @click="openCampaign(row)"
          >
            <!-- Row 1: name + status -->
            <div class="flex items-start justify-between gap-2 mb-2">
              <div class="flex items-center gap-1.5 min-w-0">
                <span v-if="row.status === 'running'" class="w-2 h-2 rounded-full bg-green-500 animate-pulse shrink-0 mt-0.5" />
                <span class="text-sm font-semibold text-ink-gray-9 truncate">{{ row.name || '—' }}</span>
              </div>
              <Badge :label="statusLabel[row.status] || row.status || '—'" :theme="statusTheme[row.status] || 'gray'" size="sm" class="shrink-0" />
            </div>
            <!-- Row 2: agent + progress bar -->
            <div class="mb-2">
              <div class="flex items-center justify-between text-xs text-ink-gray-5 mb-1">
                <span>{{ row.agent_label || row.agent_key || 'Không có agent' }}</span>
                <span class="tabular-nums">{{ row.called_count || 0 }}/{{ row.total_count || 0 }} cuộc gọi</span>
              </div>
              <div v-if="row.total_count" class="h-1.5 bg-surface-gray-2 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all"
                  :class="row.status === 'running' ? 'bg-green-500' : 'bg-ink-gray-5'"
                  :style="{ width: Math.min(100, Math.round(((row.called_count || 0) / row.total_count) * 100)) + '%' }"
                />
              </div>
            </div>
            <!-- Row 3: booking count + date + action -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3 text-xs text-ink-gray-5">
                <span>📅 {{ row.booked_count || 0 }} lịch hẹn</span>
                <span>{{ formatTime(row.created_at) }}</span>
              </div>
              <div @click.stop>
                <Button
                  v-if="row.status === 'draft' || row.status === 'paused'"
                  variant="subtle"
                  label="Chạy"
                  iconLeft="play"
                  size="sm"
                  :loading="runningId === row.id"
                  @click="quickRun(row)"
                />
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Empty -->
      <div v-else class="flex flex-1 flex-col items-center justify-center gap-3 text-ink-gray-4">
        <FeatherIcon name="phone-call" class="h-12 w-12" />
        <p class="text-sm font-medium text-ink-gray-5">Chưa có chiến dịch nào</p>
        <Button variant="solid" label="Tạo chiến dịch đầu tiên" iconLeft="plus" @click="showCreate = true" />
      </div>
    </div>

  </template>

  <!-- ══ DETAIL VIEW ═══════════════════════════════════════════ -->
  <CampaignDetailView
    v-else
    :campaign="selectedCampaign"
    @updated="onDetailUpdated"
    @deleted="backToList"
  />

  <!-- Modal tạo chiến dịch -->
  <CampaignCreateModal
    :show="showCreate"
    @close="showCreate = false"
    @created="onCampaignCreated"
  />
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Badge, FeatherIcon, Button, call, toast } from 'frappe-ui'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import CampaignCreateModal from './CampaignCreateModal.vue'
import CampaignDetailView from './CampaignDetailView.vue'

// ── Status maps ───────────────────────────────
const statusLabel = {
  draft: 'Nháp', running: 'Đang chạy', paused: 'Tạm dừng', completed: 'Hoàn thành',
}
const statusTheme = {
  draft: 'gray', running: 'green', paused: 'yellow', completed: 'blue',
}

// ── State ─────────────────────────────────────
const campaigns = ref([])
const loading = ref(false)
const errorMsg = ref('')
const runningId = ref(null)
const showCreate = ref(false)
const selectedCampaign = ref(null)
const activeFilter = ref('all')

// ── Manual call ───────────────────────────────
const manualName = ref('')
const manualPhone = ref('')
const manualAgentKey = ref('cold')
const manualCallLoading = ref(false)
const manualCallStatus = ref('')

async function triggerManualCall() {
  const phone = manualPhone.value.trim()
  if (!phone) return
  manualCallLoading.value = true
  manualCallStatus.value = ''
  try {
    await call('voice_crm.api.proxy_trigger_call', {
      phone,
      name: manualName.value.trim() || undefined,
      agent_key: manualAgentKey.value,
    })
    manualCallStatus.value = `✓ Đang gọi ${phone}`
    manualPhone.value = ''
    manualName.value = ''
    setTimeout(() => { manualCallStatus.value = '' }, 5000)
  } catch (e) {
    toast({ title: 'Lỗi gọi điện: ' + (e.message || e), variant: 'error' })
  } finally {
    manualCallLoading.value = false
  }
}

// ── Load campaigns ────────────────────────────
async function loadCampaigns() {
  loading.value = true
  errorMsg.value = ''
  try {
    const result = await call('voice_crm.api.proxy_get_campaigns', { limit: 50 })
    campaigns.value = Array.isArray(result) ? result : []
    // Update selectedCampaign if user is viewing detail
    if (selectedCampaign.value) {
      const updated = campaigns.value.find(c => c.id === selectedCampaign.value.id)
      if (updated) selectedCampaign.value = updated
    }
  } catch (e) {
    errorMsg.value = 'Lỗi tải dữ liệu: ' + (e.message || JSON.stringify(e))
    campaigns.value = []
  } finally {
    loading.value = false
  }
}

// ── Quick run from list ───────────────────────
async function quickRun(campaign) {
  if (runningId.value) return
  runningId.value = campaign.id
  try {
    await call('voice_crm.api.proxy_update_campaign', { campaign_id: campaign.id, status: 'running' })
    await call('voice_crm.api.proxy_run_campaign', { campaign_id: campaign.id })
    toast({ title: `Đã kích hoạt "${campaign.name}"`, variant: 'success' })
    setTimeout(loadCampaigns, 2000)
  } catch (e) {
    toast({ title: 'Không thể chạy: ' + (e.message || e), variant: 'error' })
  } finally {
    runningId.value = null
  }
}

// ── Navigation ────────────────────────────────
function openCampaign(row) {
  selectedCampaign.value = row
}

function backToList() {
  selectedCampaign.value = null
  loadCampaigns()
}

function onDetailUpdated() {
  loadCampaigns()
}

function onCampaignCreated() {
  loadCampaigns()
}

// ── Filter & Stats ────────────────────────────
const statusTabs = computed(() => [
  { id: 'all', label: 'Tất cả', count: campaigns.value.length },
  { id: 'running', label: 'Đang chạy', count: campaigns.value.filter(c => c.status === 'running').length },
  { id: 'draft', label: 'Nháp', count: campaigns.value.filter(c => c.status === 'draft').length },
  { id: 'paused', label: 'Tạm dừng', count: campaigns.value.filter(c => c.status === 'paused').length },
  { id: 'completed', label: 'Hoàn thành', count: campaigns.value.filter(c => c.status === 'completed').length },
])

const filteredCampaigns = computed(() => {
  if (activeFilter.value === 'all') return campaigns.value
  return campaigns.value.filter(c => c.status === activeFilter.value)
})

const stats = computed(() => {
  const totalCalls = campaigns.value.reduce((s, c) => s + (c.called_count || 0), 0)
  const totalBooked = campaigns.value.reduce((s, c) => s + (c.booked_count || 0), 0)
  const rate = totalCalls > 0 ? Math.round((totalBooked / totalCalls) * 100) : 0
  return [
    { label: 'Chiến dịch', value: campaigns.value.length, color: 'text-ink-gray-9' },
    { label: 'Tổng đã gọi', value: totalCalls, color: 'text-ink-gray-7' },
    { label: 'Đặt lịch', value: totalBooked, color: 'text-green-600' },
    { label: 'Tỉ lệ', value: rate + '%', color: rate >= 20 ? 'text-green-600' : 'text-ink-gray-7' },
  ]
})

// ── Auto-refresh ──────────────────────────────
let refreshTimer = null

function startAutoRefresh() {
  stopAutoRefresh()
  refreshTimer = setInterval(() => {
    if (campaigns.value.some(c => c.status === 'running')) {
      loadCampaigns()
    } else {
      stopAutoRefresh()
    }
  }, 8000)
}

function stopAutoRefresh() {
  if (refreshTimer) { clearInterval(refreshTimer); refreshTimer = null }
}

onMounted(async () => {
  await loadCampaigns()
  if (campaigns.value.some(c => c.status === 'running')) startAutoRefresh()
})

onUnmounted(stopAutoRefresh)

function formatTime(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString('vi-VN', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
    })
  } catch { return ts }
}
</script>
