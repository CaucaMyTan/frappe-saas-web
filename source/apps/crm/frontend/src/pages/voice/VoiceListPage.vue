<template>
  <LayoutHeader v-if="showHeader">
    <template #left-header>
      <h3 class="text-lg font-medium text-ink-gray-7">{{ title }}</h3>
    </template>
    <template #right-header>
      <Button variant="solid" :label="__('Tạo mới')" iconLeft="plus" @click="openCreate" />
    </template>
  </LayoutHeader>

  <div class="flex flex-1 flex-col overflow-hidden">
    <div v-if="list.loading" class="flex flex-1 items-center justify-center">
      <FeatherIcon name="loader" class="h-6 w-6 animate-spin text-ink-gray-4" />
    </div>

    <div v-else-if="list.data?.length" class="flex-1 overflow-auto">
      <!-- Desktop table -->
      <table class="hidden md:table w-full border-collapse">
        <thead class="sticky top-0 z-10 bg-surface-white">
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              class="border-b border-outline-gray-modals px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-ink-gray-5"
            >
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in list.data"
            :key="row.name"
            class="cursor-pointer border-b border-outline-gray-modals hover:bg-surface-gray-1"
            @click="openEdit(row.name)"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="max-w-[240px] truncate px-4 py-3 text-sm text-ink-gray-8"
            >
              <Badge
                v-if="col.type === 'badge'"
                :label="getCellValue(row, col) || ''"
                :theme="col.themeMap?.[getCellValue(row, col)] || 'gray'"
                size="sm"
              />
              <span v-else>{{ getCellValue(row, col) || '—' }}</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile cards -->
      <div class="md:hidden divide-y divide-outline-gray-modals">
        <div
          v-for="row in list.data"
          :key="row.name"
          class="px-4 py-3.5 active:bg-surface-gray-1 cursor-pointer"
          @click="openEdit(row.name)"
        >
          <!-- First column = title -->
          <div class="text-sm font-semibold text-ink-gray-9 mb-1.5 truncate">
            {{ getCellValue(row, columns[0]) || row.name }}
          </div>
          <!-- Remaining columns as key-value pairs -->
          <div class="flex flex-wrap gap-x-4 gap-y-1">
            <div
              v-for="col in columns.slice(1)"
              :key="col.key"
              class="flex items-center gap-1.5 text-xs text-ink-gray-5"
            >
              <span class="text-ink-gray-4">{{ col.label }}:</span>
              <Badge
                v-if="col.type === 'badge'"
                :label="getCellValue(row, col) || ''"
                :theme="col.themeMap?.[getCellValue(row, col)] || 'gray'"
                size="sm"
              />
              <span v-else class="text-ink-gray-7 truncate max-w-[180px]">{{ getCellValue(row, col) || '—' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-ink-gray-4">
      <FeatherIcon name="inbox" class="h-10 w-10" />
      <span class="text-sm">Chưa có dữ liệu nào</span>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { createListResource, Badge, FeatherIcon, Button } from 'frappe-ui'
import { onMounted } from 'vue'

const props = defineProps({
  doctype: { type: String, required: true },
  title: { type: String, required: true },
  fields: { type: Array, default: () => ['name', 'creation'] },
  columns: { type: Array, default: () => [] },
  filters: { type: Object, default: () => ({}) },
  orderBy: { type: String, default: 'creation desc' },
  showHeader: { type: Boolean, default: true },
})

const list = createListResource({
  type: 'list',
  doctype: props.doctype,
  fields: props.fields,
  filters: props.filters,
  orderBy: props.orderBy,
  pageLength: 50,
})

onMounted(() => list.fetch())

const { showModal } = useDoctypeModal()

function openCreate() {
  showModal({
    doctype: props.doctype,
    title: `Tạo ${props.title}`,
    callbacks: { afterInsert: () => list.reload() },
  })
}

function openEdit(name) {
  showModal({
    doctype: props.doctype,
    name,
    title: props.title,
    callbacks: { afterUpdate: () => list.reload() },
  })
}

function getCellValue(row, col) {
  if (col.render) return col.render(row)
  return row[col.key]
}
</script>
