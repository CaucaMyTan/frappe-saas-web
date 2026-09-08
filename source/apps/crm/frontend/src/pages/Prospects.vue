<template>
  <LayoutHeader>
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">Tiềm năng</h3>
    </template>
    <template #right-header>
      <Button variant="solid" :label="__('Tạo mới')" iconLeft="plus" @click="openCreate" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div class="border-b border-outline-gray-modals bg-surface-white px-4">
      <div class="flex items-center gap-4">
        <div class="flex gap-0">
          <button
            v-for="tab in ownerTabs"
            :key="tab.id"
            class="px-3 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors flex items-center gap-1.5"
            :class="
              activeOwner === tab.id
                ? 'border-ink-gray-9 text-ink-gray-9'
                : 'border-transparent text-ink-gray-5 hover:text-ink-gray-7'
            "
            @click="activeOwner = tab.id"
          >
            {{ tab.label }}
            <span
              v-if="tab.id === 'mine' && mineCount > 0"
              class="inline-flex items-center justify-center rounded-full bg-ink-gray-9 text-surface-white text-xs font-semibold px-1.5 py-0.5 min-w-[20px]"
              :class="activeOwner !== 'mine' ? '!bg-surface-gray-3 !text-ink-gray-6' : ''"
            >{{ mineCount }}</span>
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
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Tên khách</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Số điện thoại</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Trạng thái</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Nguồn</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Phụ trách</th>
            <th class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5">Cập nhật</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in list.data"
            :key="row.name"
            class="cursor-pointer border-b border-outline-gray-modals hover:bg-surface-gray-1"
            @click="openEdit(row.name)"
          >
            <td class="px-4 py-3">
              <div class="text-sm font-medium text-ink-gray-8">{{ row.lead_name || '—' }}</div>
              <div class="text-xs text-ink-gray-4">{{ row.organization || '' }}</div>
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-7">{{ row.mobile_no || '—' }}</td>
            <td class="px-4 py-3">
              <Badge :label="statusLabel[row.status] || row.status || ''" :theme="statusTheme[row.status] || 'gray'" size="sm" />
            </td>
            <td class="px-4 py-3 text-sm text-ink-gray-6">{{ row.source || '—' }}</td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-2">
                <UserAvatar v-if="row.lead_owner" :user="row.lead_owner" size="xs" />
                <span class="text-sm text-ink-gray-6">
                  {{ row.lead_owner ? getUser(row.lead_owner).full_name : '—' }}
                </span>
              </div>
            </td>
            <td class="px-4 py-3 text-xs text-ink-gray-4">{{ formatDate(row.modified) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="users" class="h-10 w-10" />
      <p class="text-sm font-medium text-ink-gray-5">Không có khách tiềm năng nào</p>
      <p v-if="activeOwner === 'mine'" class="text-xs text-ink-gray-4">
        Chưa có khách nào được phân công cho bạn
      </p>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { createListResource, Badge, FeatherIcon, Button } from 'frappe-ui'
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const { user } = sessionStore()
const { getUser } = usersStore()
const router = useRouter()

const activeOwner = ref('mine')
const activeStatus = ref('all')

const ownerTabs = [
  { id: 'mine', label: 'Của tôi' },
  { id: 'all', label: 'Tất cả' },
]

const statusPills = [
  { id: 'all', label: 'Tất cả' },
  { id: 'New', label: 'Mới' },
  { id: 'Contacted', label: 'Đã liên hệ' },
  { id: 'Replied', label: 'Đã phản hồi' },
  { id: 'Converted', label: 'Đã chốt' },
]

const statusLabel = {
  New: 'Mới',
  Contacted: 'Đã liên hệ',
  Replied: 'Đã phản hồi',
  Converted: 'Đã chốt',
  Nurture: 'Nuôi dưỡng',
  Junk: 'Spam',
  Unqualified: 'Không phù hợp',
  Qualified: 'Tiềm năng cao',
}

const statusTheme = {
  New: 'blue',
  Contacted: 'yellow',
  Replied: 'orange',
  Converted: 'green',
  Nurture: 'purple',
  Junk: 'gray',
}

const mineCount = ref(0)

const list = createListResource({
  doctype: 'CRM Lead',
  fields: ['name', 'lead_name', 'mobile_no', 'status', 'source', 'lead_owner', 'organization', 'modified'],
  filters: { converted: 0 },
  orderBy: 'modified desc',
  pageLength: 50,
})

function buildFilters() {
  const f = { converted: 0 }
  if (activeOwner.value === 'mine') f.lead_owner = user.value
  if (activeStatus.value !== 'all') f.status = activeStatus.value
  return f
}

function applyFilters() {
  list.update({ filters: buildFilters() })
  list.reload()
}

watch(() => list.data, (data) => {
  if (activeOwner.value === 'mine') {
    mineCount.value = data?.length || 0
  }
})

watch([activeOwner, activeStatus], applyFilters)
onMounted(applyFilters)

const { showModal } = useDoctypeModal()

function openCreate() {
  showModal({
    doctype: 'CRM Lead',
    title: 'Tạo khách tiềm năng',
    callbacks: { afterInsert: () => list.reload() },
  })
}

function openEdit(name) {
  router.push({ name: 'Lead', params: { leadId: name } })
}

function formatDate(ts) {
  if (!ts) return ''
  try {
    return new Date(ts).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
  } catch {
    return ts
  }
}
</script>
