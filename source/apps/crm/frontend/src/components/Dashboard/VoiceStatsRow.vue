<template>
  <div class="grid grid-cols-2 gap-3 px-5 pb-1 sm:grid-cols-4">
    <RouterLink
      v-for="card in cards"
      :key="card.key"
      :to="card.to"
      class="group flex flex-col gap-1 rounded-lg border border-outline-gray-modals bg-surface-white px-4 py-3 transition-colors hover:border-outline-gray-3 hover:bg-surface-gray-1"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs font-medium text-ink-gray-5">{{ card.label }}</span>
        <component :is="card.icon" class="h-3.5 w-3.5 text-ink-gray-4 group-hover:text-ink-gray-6" />
      </div>
      <div class="flex items-end gap-2">
        <span class="text-2xl font-semibold leading-none" :class="card.valueClass">
          {{ statsResource.data ? statsResource.data[card.key] ?? '—' : '—' }}
        </span>
        <span v-if="card.suffix" class="mb-0.5 text-xs text-ink-gray-4">{{ card.suffix }}</span>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { RouterLink } from 'vue-router'
import LucidePhone from '~icons/lucide/phone'
import LucideUsers from '~icons/lucide/users'
import LucideCalendar from '~icons/lucide/calendar'
import LucideAlertCircle from '~icons/lucide/alert-circle'

const statsResource = createResource({
  url: 'crm.api.dashboard.get_voice_stats',
  auto: true,
})

const cards = [
  {
    key: 'calls_today',
    label: 'Cuộc gọi hôm nay',
    icon: LucidePhone,
    valueClass: 'text-ink-gray-9',
    to: { name: 'Call Logs' },
  },
  {
    key: 'new_leads_week',
    label: 'Tiềm năng tuần này',
    icon: LucideUsers,
    valueClass: 'text-ink-gray-9',
    to: { name: 'Prospects' },
    suffix: 'mới',
  },
  {
    key: 'appointments_today',
    label: 'Lịch hẹn hôm nay',
    icon: LucideCalendar,
    valueClass: 'text-ink-gray-9',
    to: { name: 'Appointments' },
  },
  {
    key: 'pending_support',
    label: 'Cần hỗ trợ',
    icon: LucideAlertCircle,
    valueClass: 'text-red-600',
    to: { name: 'Support Inbox' },
  },
]
</script>
