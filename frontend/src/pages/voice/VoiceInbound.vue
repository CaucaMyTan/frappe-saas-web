<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Cuộc gọi đến</h3>
    </template>
    <template #right-header>
      <Button variant="outline" label="Làm mới" iconLeft="refresh-cw" size="sm" @click="loadData" />
    </template>
  </LayoutHeader>

  <div class="flex-1 overflow-auto">
    <div v-if="loading" class="flex h-full items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else class="p-6 space-y-5 max-w-4xl mx-auto">

      <!-- Stats bar -->
      <div class="grid grid-cols-4 gap-4">
        <div class="rounded-lg border border-outline-gray-modals bg-surface-white px-4 py-3">
          <div class="text-xs text-ink-gray-4 mb-1">Số điện thoại</div>
          <div class="text-sm font-semibold text-ink-gray-9 font-mono">{{ phoneNumber || '—' }}</div>
        </div>
        <div class="rounded-lg border border-outline-gray-modals bg-surface-white px-4 py-3">
          <div class="text-xs text-ink-gray-4 mb-1">Hôm nay nhận</div>
          <div class="text-2xl font-bold text-ink-gray-9">{{ statsToday }}</div>
          <div class="text-xs text-ink-gray-4">30 ngày gần nhất: {{ statsAll }}</div>
        </div>
        <div class="rounded-lg border border-outline-gray-modals bg-surface-white px-4 py-3">
          <div class="text-xs text-ink-gray-4 mb-1">Gọi nhỡ cần xử lý</div>
          <div class="text-2xl font-bold text-red-500">{{ statsMissed }}</div>
          <div class="text-xs text-ink-gray-4">Cần gọi lại</div>
        </div>
        <div class="rounded-lg border border-outline-gray-modals bg-surface-white px-4 py-3">
          <div class="text-xs text-ink-gray-4 mb-1">Đặt lịch hôm nay</div>
          <div class="text-2xl font-bold text-green-600">{{ statsBooked }}</div>
          <div class="text-xs text-ink-gray-4">Tổng: {{ statsBookedAll }}</div>
        </div>
      </div>

      <!-- AI Inbound Config -->
      <div class="rounded-lg border border-outline-gray-modals bg-surface-white overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-outline-gray-modals">
          <div class="flex items-center gap-2">
            <FeatherIcon name="cpu" class="h-4 w-4 text-ink-gray-5" />
            <h4 class="text-sm font-semibold text-ink-gray-8">Cài đặt Trợ lý cuộc gọi đến</h4>
          </div>
          <div class="flex items-center gap-2">
            <Badge v-if="configRecord" :label="configRecord.is_active ? 'Hoạt động' : 'Tắt'" :theme="configRecord.is_active ? 'green' : 'gray'" size="sm" />
            <Button v-if="configRecord" variant="ghost" label="Chỉnh sửa" iconLeft="edit-2" size="sm" @click="openEditConfig" />
            <Button v-else variant="solid" label="Thêm cấu hình" iconLeft="plus" size="sm" @click="openCreateConfig" />
          </div>
        </div>

        <div v-if="configRecord" class="divide-y divide-outline-gray-modals">
          <div class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Số điện thoại</span>
            <span class="text-sm font-medium text-ink-gray-8 font-mono">{{ configRecord.phone_number || '—' }}</span>
          </div>
          <div class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Tên đường dây</span>
            <span class="text-sm font-medium text-ink-gray-8">{{ configRecord.label || '—' }}</span>
          </div>
          <div class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Câu mở đầu</span>
            <span class="text-sm text-ink-gray-7 italic">{{ configRecord.greeting_message || 'AI tự chọn' }}</span>
          </div>
          <div class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Tốc độ phản hồi</span>
            <span class="text-sm font-medium text-ink-gray-8">{{ configRecord.response_speed || 'Bình thường' }}</span>
          </div>
          <div v-if="configRecord.script_template" class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Kịch bản giao tiếp</span>
            <div class="flex-1 min-w-0">
              <div
                class="text-sm text-ink-gray-7 leading-relaxed max-h-32 overflow-y-auto whitespace-pre-wrap rounded bg-surface-gray-1 px-3 py-2 font-mono text-xs border border-outline-gray-modals cursor-pointer"
                @click="openEditConfig"
              >{{ configRecord.script_template }}</div>
              <p class="text-xs text-ink-gray-4 mt-1">{{ configRecord.script_template?.length || 0 }} ký tự · Nhấp để chỉnh sửa</p>
            </div>
          </div>
          <div v-else class="px-4 py-3 flex items-start gap-4">
            <span class="w-40 flex-shrink-0 text-sm text-ink-gray-5 pt-0.5">Kịch bản giao tiếp</span>
            <button class="text-sm text-ink-blue-3 hover:underline" @click="openEditConfig">Chưa có kịch bản — nhấp để thêm</button>
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-10 gap-2 text-ink-gray-4">
          <FeatherIcon name="phone-incoming" class="h-8 w-8" />
          <p class="text-sm">Chưa có cấu hình trợ lý cuộc gọi đến</p>
          <Button variant="solid" label="Thêm cấu hình" iconLeft="plus" size="sm" @click="openCreateConfig" />
        </div>
      </div>

      <!-- Recent inbound calls -->
      <div class="rounded-lg border border-outline-gray-modals bg-surface-white overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-outline-gray-modals">
          <div class="flex items-center gap-2">
            <FeatherIcon name="phone-incoming" class="h-4 w-4 text-ink-gray-5" />
            <h4 class="text-sm font-semibold text-ink-gray-8">Cuộc gọi kết nối gần đây</h4>
          </div>
          <span class="text-xs text-ink-gray-4">{{ recentConnected.length }} cuộc</span>
        </div>

        <div v-if="recentConnected.length">
          <table class="w-full border-collapse text-sm">
            <thead class="bg-surface-gray-1">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Tên khách</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Số gọi</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Trạng thái</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Thời lượng</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-ink-gray-5 uppercase">Thời gian</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in recentConnected" :key="row.id" class="border-t border-outline-gray-modals hover:bg-surface-gray-1">
                <td class="px-4 py-2.5 font-medium text-ink-gray-8">{{ row.contact_name || '—' }}</td>
                <td class="px-4 py-2.5 font-mono text-ink-gray-6">{{ row.contact_phone || '—' }}</td>
                <td class="px-4 py-2.5">
                  <Badge :label="callStatusLabel[row.status] || row.status || '—'" :theme="callStatusTheme[row.status] || 'gray'" size="sm" />
                </td>
                <td class="px-4 py-2.5 text-ink-gray-6">{{ formatDuration(row.duration_seconds) }}</td>
                <td class="px-4 py-2.5 text-xs text-ink-gray-4">{{ formatTime(row.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-8 gap-2 text-ink-gray-4">
          <FeatherIcon name="phone-off" class="h-7 w-7" />
          <p class="text-sm">Chưa có cuộc gọi đến nào</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createListResource, Badge, FeatherIcon, Button, call } from 'frappe-ui'
import { ref, computed, onMounted } from 'vue'

const loading = ref(false)
const inboundCalls = ref([])
const phoneNumber = ref('')

const callStatusLabel = {
  completed: 'Hoàn thành', no_answer: 'Không nghe',
  busy: 'Đang bận', failed: 'Thất bại', voicemail: 'Hộp thư thoại',
}
const callStatusTheme = {
  completed: 'green', no_answer: 'red', busy: 'yellow', failed: 'red', voicemail: 'gray',
}

// ── Config ──────────────────────────────────
const inboundConfigs = createListResource({
  doctype: 'AI Inbound Config',
  fields: ['name', 'phone_number', 'label', 'retell_agent_id', 'response_speed', 'greeting_message', 'script_template', 'is_active'],
  orderBy: 'creation asc',
  pageLength: 1,
  auto: true,
})

const configRecord = computed(() => inboundConfigs.data?.[0] || null)

const { showModal } = useDoctypeModal()

function openCreateConfig() {
  showModal({
    doctype: 'AI Inbound Config',
    title: 'Thêm cấu hình cuộc gọi đến',
    callbacks: { afterInsert: () => inboundConfigs.reload() },
  })
}

function openEditConfig() {
  if (!configRecord.value) return
  showModal({
    doctype: 'AI Inbound Config',
    name: configRecord.value.name,
    title: 'Cài đặt Trợ lý cuộc gọi đến',
    callbacks: { afterUpdate: () => inboundConfigs.reload() },
  })
}

// ── Stats ────────────────────────────────────
const today = new Date().toISOString().slice(0, 10)

const statsAll = computed(() => inboundCalls.value.length)
const statsToday = computed(() =>
  inboundCalls.value.filter(c => c.created_at?.slice(0, 10) === today).length
)
const statsMissed = computed(() =>
  inboundCalls.value.filter(c => c.status === 'no_answer').length
)
const statsBooked = computed(() =>
  inboundCalls.value.filter(c => c.appointment_booked && c.created_at?.slice(0, 10) === today).length
)
const statsBookedAll = computed(() =>
  inboundCalls.value.filter(c => c.appointment_booked).length
)

const recentConnected = computed(() =>
  inboundCalls.value.filter(c => c.status === 'completed').slice(0, 10)
)

// ── Load ─────────────────────────────────────
async function loadData() {
  loading.value = true
  try {
    const [calls, config] = await Promise.all([
      call('voice_crm.api.proxy_get_calls', { limit: 100, direction: 'inbound' }),
      call('voice_crm.api.proxy_get_client_config'),
    ])
    inboundCalls.value = Array.isArray(calls) ? calls : []
    phoneNumber.value = config?.retell_phone_number || ''
  } catch (e) {
    console.error('Lỗi tải dữ liệu:', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

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
