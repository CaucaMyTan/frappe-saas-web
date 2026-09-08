<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Lịch hẹn</h3>
    </template>
    <template #right-header>
      <Button variant="solid" label="Tạo lịch hẹn" iconLeft="plus" @click="openCreate" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div class="border-b border-outline-gray-modals bg-surface-white px-4">
      <div class="flex items-center gap-4">
        <div class="flex gap-0">
          <button
            v-for="tab in dateTabs"
            :key="tab.id"
            class="px-3 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors"
            :class="
              activeDateTab === tab.id
                ? 'border-ink-gray-9 text-ink-gray-9'
                : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
            "
            @click="activeDateTab = tab.id"
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

    <div v-if="list.loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="list.data?.length" class="flex-1 overflow-auto">
      <table class="w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Khách hàng</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Số điện thoại</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Thời gian hẹn</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Ghi chú</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in list.data"
            :key="row.name"
            class="cursor-pointer border-b border-outline-gray-modals hover:bg-surface-gray-1"
            @click="openEdit(row.name)"
          >
            <td class="px-4 py-3 text-sm font-medium text-ink-gray-8">{{ row.contact_name || '—' }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-7">{{ row.contact_phone || '—' }}</td>
            <td class="px-4 py-3 text-sm text-ink-gray-7">{{ formatDateTime(row.scheduled_at) }}</td>
            <td class="px-4 py-3">
              <Badge :label="row.status || ''" :theme="statusTheme[row.status] || 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-5 max-w-[200px] truncate">{{ row.appointment_notes || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="calendar" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">
        {{ activeDateTab === 'today' ? 'Hôm nay không có lịch hẹn nào' : 'Không có lịch hẹn nào' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createListResource, Badge, FeatherIcon, Button } from 'frappe-ui'
import { ref, watch, onMounted } from 'vue'

const activeDateTab = ref('today')
const activeStatus = ref('all')

const dateTabs = [
  { id: 'today', label: 'Hôm nay' },
  { id: 'week', label: 'Tuần này' },
  { id: 'all', label: 'Tất cả' },
]

const statusPills = [
  { id: 'all', label: 'Tất cả' },
  { id: 'pending', label: 'Chờ xác nhận' },
  { id: 'confirmed', label: 'Đã xác nhận' },
  { id: 'completed', label: 'Hoàn thành' },
  { id: 'cancelled', label: 'Đã hủy' },
]

const statusTheme = {
  pending: 'gray',
  confirmed: 'green',
  completed: 'blue',
  cancelled: 'red',
}

const list = createListResource({
  doctype: 'Voice Appointment',
  fields: ['name', 'contact_name', 'contact_phone', 'scheduled_at', 'status', 'appointment_notes'],
  orderBy: 'scheduled_at asc',
  pageLength: 100,
})

function getDateRange() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const todayStr = today.toISOString().slice(0, 10)

  if (activeDateTab.value === 'today') {
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    return [['scheduled_at', '>=', todayStr], ['scheduled_at', '<', tomorrow.toISOString().slice(0, 10)]]
  }
  if (activeDateTab.value === 'week') {
    const nextWeek = new Date(today)
    nextWeek.setDate(nextWeek.getDate() + 7)
    return [['scheduled_at', '>=', todayStr], ['scheduled_at', '<', nextWeek.toISOString().slice(0, 10)]]
  }
  return []
}

function applyFilters() {
  const filters = []
  const dateRange = getDateRange()
  filters.push(...dateRange)
  if (activeStatus.value !== 'all') filters.push(['status', '=', activeStatus.value])
  list.update({ filters: filters.length ? filters : {} })
  list.reload()
}

watch([activeDateTab, activeStatus], applyFilters)
onMounted(applyFilters)

const { showModal } = useDoctypeModal()

function openCreate() {
  showModal({
    doctype: 'Voice Appointment',
    title: 'Tạo lịch hẹn',
    callbacks: { afterInsert: () => list.reload() },
  })
}

function openEdit(name) {
  showModal({
    doctype: 'Voice Appointment',
    name,
    title: 'Lịch hẹn',
    callbacks: { afterUpdate: () => list.reload() },
  })
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
