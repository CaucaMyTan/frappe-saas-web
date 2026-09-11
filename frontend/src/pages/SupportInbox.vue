<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Cần hỗ trợ</h3>
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div class="border-b border-outline-gray-modals bg-surface-white px-4">
      <div class="flex items-center gap-4">
        <div class="flex gap-0">
          <button
            v-for="tab in ownerTabs"
            :key="tab.id"
            class="px-3 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors"
            :class="
              activeOwner === tab.id
                ? 'border-ink-gray-9 text-ink-gray-9'
                : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
            "
            @click="activeOwner = tab.id"
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

    <div v-else-if="list.data?.length" class="flex-1 overflow-auto p-4 space-y-2">
      <div
        v-for="item in list.data"
        :key="item.name"
        class="rounded-lg border border-outline-gray-modals bg-surface-white p-4 hover:border-outline-gray-3 transition-colors"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <Badge
                :label="item.type === 'Incoming' ? 'Gọi vào' : 'Gọi ra'"
                :theme="item.type === 'Incoming' ? 'blue' : 'orange'"
                size="sm"
              />
              <Badge
                :label="callStatusLabel[item.status] || item.status || 'Nhỡ máy'"
                :theme="statusTheme[item.status] || 'red'"
                size="sm"
              />
            </div>
            <p class="text-sm font-medium text-ink-gray-8">
              {{ item.caller || item.from || 'Số ẩn danh' }}
            </p>
            <p class="text-xs text-ink-gray-4 mt-0.5">{{ formatTime(item.start_time) }}</p>
            <p v-if="item.note" class="text-sm text-ink-gray-6 mt-2 line-clamp-2">{{ item.note }}</p>
          </div>
          <div class="flex flex-col gap-1.5 flex-shrink-0">
            <Button size="sm" variant="outline" label="Gọi lại" iconLeft="phone" />
            <Button size="sm" variant="outline" label="Đặt lịch" iconLeft="calendar" />
          </div>
        </div>
        <div class="mt-3 flex items-center justify-between border-t border-outline-gray-modals pt-2">
          <div class="flex items-center gap-2">
            <span class="text-xs text-ink-gray-4">Phụ trách:</span>
            <UserAvatar v-if="item._assign && parseAssign(item._assign)[0]" :user="parseAssign(item._assign)[0]" size="xs" class="mr-1" />
            <span class="text-xs text-ink-gray-6">
              {{ item._assign ? (parseAssign(item._assign)[0] ? getUser(parseAssign(item._assign)[0]).full_name : 'Chưa phân công') : 'Chưa phân công' }}
            </span>
          </div>
          <Button
            size="sm"
            variant="ghost"
            label="Phân công"
            iconLeft="user-plus"
            @click.stop="openAssign(item)"
          />
        </div>
      </div>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-3 text-ink-gray-4">
      <FeatherIcon name="check-circle" class="h-12 w-12 text-ink-green-3" />
      <p class="text-sm font-medium text-ink-gray-5">Không có ca nào cần xử lý</p>
      <p class="text-xs text-ink-gray-4">Tất cả cuộc gọi đã được xử lý</p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { createListResource, Badge, FeatherIcon, Button } from 'frappe-ui'
import { ref, watch, onMounted } from 'vue'

const { user } = sessionStore()
const { getUser } = usersStore()

const activeOwner = ref('mine')
const activeStatus = ref('all')

const ownerTabs = [
  { id: 'mine', label: 'Của tôi' },
  { id: 'all', label: 'Tất cả' },
]

const statusPills = [
  { id: 'all', label: 'Tất cả' },
  { id: 'missed', label: 'Nhỡ máy' },
  { id: 'incoming', label: 'Inbound' },
]

const callStatusLabel = {
  Completed: 'Hoàn thành',
  Missed: 'Nhỡ máy',
  'No Answer': 'Không nghe',
  Busy: 'Đang bận',
  Failed: 'Thất bại',
  Cancelled: 'Đã hủy',
}

const statusTheme = {
  Completed: 'green',
  Missed: 'red',
  'No Answer': 'red',
  Busy: 'yellow',
  Failed: 'red',
}

const list = createListResource({
  doctype: 'CRM Call Log',
  fields: ['name', 'type', 'status', 'from', 'to', 'caller', 'start_time', 'duration', 'note', 'reference_docname', '_assign'],
  orderBy: 'start_time desc',
  pageLength: 50,
})

function buildFilters() {
  const filters = []
  if (activeOwner.value === 'mine') filters.push(['_assign', 'like', `%${user.value}%`])
  if (activeStatus.value === 'missed') filters.push(['status', '=', 'Missed'])
  if (activeStatus.value === 'incoming') filters.push(['type', '=', 'Incoming'])
  return filters.length ? filters : {}
}

function applyFilters() {
  list.update({ filters: buildFilters() })
  list.reload()
}

watch([activeOwner, activeStatus], applyFilters)
onMounted(applyFilters)

function parseAssign(assignStr) {
  try { return JSON.parse(assignStr || '[]') } catch { return [] }
}

function openAssign(item) {
  // TODO: open frappe assign dialog
  frappe.ui.form.assign_to.dialog({
    obj: { doctype: 'CRM Call Log', name: item.name },
    method: 'frappe.desk.form.assign_to.add',
    callback: () => list.reload(),
  })
}

function formatTime(ts) {
  if (!ts) return ''
  try {
    return new Date(ts).toLocaleString('vi-VN', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
    })
  } catch {
    return ts
  }
}
</script>
