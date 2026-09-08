<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Lịch hẹn AI</h3>
    </template>
    <template #right-header>
      <Button variant="outline" label="Làm mới" iconLeft="refresh-cw" @click="loadAppointments" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div v-if="loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="appointments.length" class="flex-1 overflow-auto">
      <!-- Desktop table -->
      <table class="hidden md:table w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời gian hẹn</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Ghi chú</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Cal Booking ID</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Ngày tạo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in appointments" :key="row.id" class="border-b border-outline-gray-modals hover:bg-surface-gray-1">
            <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ formatTime(row.scheduled_at) }}</td>
            <td class="px-4 py-3">
              <Badge :label="apptStatusLabel[row.status] || row.status || '—'" :theme="apptStatusTheme[row.status] || 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-5 max-w-[240px] truncate">{{ row.appointment_notes || '—' }}</td>
            <td class="px-4 py-3 text-xs font-mono text-ink-gray-4">{{ row.cal_booking_id || '—' }}</td>
            <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatTime(row.created_at) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile cards -->
      <div class="md:hidden divide-y divide-outline-gray-modals">
        <div v-for="row in appointments" :key="row.id" class="px-4 py-3.5">
          <div class="flex items-start justify-between gap-2 mb-1.5">
            <div class="text-sm font-semibold text-ink-gray-9">📅 {{ formatTime(row.scheduled_at) }}</div>
            <Badge :label="apptStatusLabel[row.status] || row.status || '—'" :theme="apptStatusTheme[row.status] || 'gray'" size="sm" class="shrink-0" />
          </div>
          <div v-if="row.appointment_notes" class="text-sm text-ink-gray-6 mb-1 line-clamp-2">{{ row.appointment_notes }}</div>
          <div class="flex items-center gap-3 text-xs text-ink-gray-4">
            <span v-if="row.cal_booking_id" class="font-mono truncate max-w-[140px]">{{ row.cal_booking_id }}</span>
            <span>Tạo: {{ formatTime(row.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="calendar" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">Chưa có lịch hẹn nào</p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Badge, FeatherIcon, Button, call } from 'frappe-ui'
import { ref, onMounted } from 'vue'

const apptStatusLabel = {
  pending: 'Chờ xác nhận',
  confirmed: 'Đã xác nhận',
  cancelled: 'Đã hủy',
  completed: 'Hoàn thành',
}

const apptStatusTheme = {
  pending: 'gray',
  confirmed: 'green',
  cancelled: 'red',
  completed: 'blue',
}

const appointments = ref([])
const loading = ref(false)

async function loadAppointments() {
  loading.value = true
  try {
    const result = await call('voice_crm.api.proxy_get_appointments', { limit: 100 })
    appointments.value = Array.isArray(result) ? result : []
  } catch (e) {
    console.error('Lỗi tải lịch hẹn:', e)
    appointments.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadAppointments)

function formatTime(ts) {
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
