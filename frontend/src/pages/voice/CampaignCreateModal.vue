<template>
  <Dialog v-model="isOpen" :options="{ size: 'xl' }">
    <template #body>
      <div class="bg-surface-white rounded-xl overflow-hidden">
        <!-- Header -->
        <div class="px-6 pt-5 pb-4 border-b border-outline-gray-modals flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-ink-gray-9">Tạo chiến dịch AutoCall</h3>
            <p class="text-sm text-ink-gray-5 mt-0.5">{{ stepSubtitles[step - 1] }}</p>
          </div>
          <Button variant="ghost" icon="x" @click="close" />
        </div>

        <!-- Step progress -->
        <div class="px-6 py-3 flex items-center gap-1 text-sm border-b border-outline-gray-modals bg-surface-gray-1">
          <template v-for="(label, i) in stepLabels" :key="i">
            <div class="flex items-center gap-1.5">
              <div
                class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium shrink-0"
                :class="i + 1 < step ? 'bg-green-500 text-white' : i + 1 === step ? 'bg-ink-gray-9 text-white' : 'bg-surface-gray-3 text-ink-gray-4'"
              >
                <FeatherIcon v-if="i + 1 < step" name="check" class="h-3 w-3" />
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span :class="i + 1 === step ? 'text-ink-gray-9 font-medium' : 'text-ink-gray-4'">{{ label }}</span>
            </div>
            <span v-if="i < stepLabels.length - 1" class="text-ink-gray-3 mx-1">›</span>
          </template>
        </div>

        <!-- Content -->
        <div class="px-6 py-5 min-h-72">

          <!-- Step 1: Info -->
          <div v-if="step === 1" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-ink-gray-7 mb-1">
                Tên chiến dịch <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.name"
                type="text"
                placeholder="VD: Telesale Data Lạnh Tháng 5/2026"
                class="w-full rounded-lg border border-outline-gray-modals px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ink-gray-3 focus:border-ink-gray-5"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-ink-gray-7 mb-1">
                Mô tả <span class="text-xs text-ink-gray-4 font-normal">(tùy chọn)</span>
              </label>
              <input
                v-model="form.description"
                type="text"
                placeholder="Mô tả ngắn về mục tiêu chiến dịch"
                class="w-full rounded-lg border border-outline-gray-modals px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ink-gray-3 focus:border-ink-gray-5"
              />
            </div>
          </div>

          <!-- Step 2: Contacts -->
          <div v-else-if="step === 2">
            <div class="flex items-center justify-between mb-4">
              <!-- Sub tabs -->
              <div class="flex gap-1 p-1 bg-surface-gray-2 rounded-lg">
                <button
                  v-for="t in contactTabs"
                  :key="t.id"
                  @click="switchContactTab(t.id)"
                  class="px-3 py-1 text-sm rounded-md transition-colors"
                  :class="contactTab === t.id ? 'bg-surface-white shadow-sm text-ink-gray-9 font-medium' : 'text-ink-gray-5 hover:text-ink-gray-7'"
                >{{ t.label }}</button>
              </div>
              <span class="text-sm text-ink-gray-5">
                <strong class="text-ink-gray-9">{{ validContacts.length }}</strong> số hợp lệ
              </span>
            </div>

            <!-- Manual input -->
            <div v-if="contactTab === 'manual'">
              <div class="max-h-56 overflow-y-auto space-y-2 pr-1 mb-3">
                <div
                  v-for="(row, i) in form.contacts"
                  :key="i"
                  class="flex gap-2 items-center"
                >
                  <span class="text-xs text-ink-gray-3 w-5 text-right shrink-0">{{ i + 1 }}</span>
                  <input
                    v-model="row.name"
                    type="text"
                    placeholder="Tên (tùy chọn)"
                    class="flex-1 rounded border border-outline-gray-modals px-2 py-1.5 text-sm focus:outline-none focus:border-ink-gray-5"
                  />
                  <input
                    v-model="row.phone"
                    type="text"
                    placeholder="Số điện thoại *"
                    class="flex-1 rounded border border-outline-gray-modals px-2 py-1.5 text-sm font-mono focus:outline-none focus:border-ink-gray-5"
                  />
                  <button
                    @click="form.contacts.splice(i, 1)"
                    class="shrink-0 p-1 text-ink-gray-3 hover:text-red-500 transition-colors"
                  >
                    <FeatherIcon name="x" class="h-4 w-4" />
                  </button>
                </div>
                <div v-if="!form.contacts.length" class="text-center py-6 text-sm text-ink-gray-4">
                  Chưa có số nào. Nhấn "+ Thêm số" để bắt đầu.
                </div>
              </div>
              <button
                @click="form.contacts.push({ name: '', phone: '' })"
                class="flex items-center gap-1.5 text-sm text-ink-gray-5 hover:text-ink-gray-9 transition-colors"
              >
                <FeatherIcon name="plus-circle" class="h-4 w-4" />
                Thêm số
              </button>
            </div>

            <!-- CSV paste -->
            <div v-else-if="contactTab === 'csv'">
              <p class="text-xs text-ink-gray-4 mb-2">
                Mỗi dòng một số. Định dạng: <code class="bg-surface-gray-2 px-1 py-0.5 rounded font-mono">Tên,SĐT</code> hoặc chỉ <code class="bg-surface-gray-2 px-1 py-0.5 rounded font-mono">SĐT</code>
              </p>
              <textarea
                v-model="csvText"
                rows="9"
                placeholder="Nguyễn Văn An,0912345678&#10;0987654321&#10;Trần Thị Bình,0901234567"
                class="w-full rounded-lg border border-outline-gray-modals px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-ink-gray-3 resize-none"
                @input="parseCsv"
              />
              <p class="text-xs text-ink-gray-5 mt-1.5">
                Phát hiện <span class="font-medium text-green-600">{{ validContacts.length }} số</span> hợp lệ
              </p>
            </div>

            <!-- CRM contacts -->
            <div v-else-if="contactTab === 'crm'">
              <div class="flex items-center gap-2 mb-3">
                <input
                  v-model="crmSearch"
                  type="text"
                  placeholder="Tìm theo tên, số điện thoại..."
                  class="flex-1 rounded-lg border border-outline-gray-modals px-3 py-1.5 text-sm focus:outline-none focus:border-ink-gray-5"
                  @input="debouncedCrmSearch"
                />
              </div>
              <div v-if="crmLoading" class="flex justify-center py-10">
                <FeatherIcon name="loader" class="h-5 w-5 animate-spin text-ink-gray-4" />
              </div>
              <div v-else class="border border-outline-gray-modals rounded-lg overflow-hidden max-h-52 overflow-y-auto">
                <div
                  v-for="c in crmContacts"
                  :key="c.id"
                  class="flex items-center gap-3 px-3 py-2 hover:bg-surface-gray-1 cursor-pointer border-b border-outline-gray-modals last:border-0"
                  @click="toggleCrmContact(c)"
                >
                  <input
                    type="checkbox"
                    :checked="selectedCrmIds.has(c.id)"
                    class="rounded shrink-0"
                    readonly
                  />
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-ink-gray-8 truncate">{{ c.full_name || 'Không tên' }}</div>
                    <div class="text-xs font-mono text-ink-gray-5">{{ c.phone }}</div>
                  </div>
                  <span v-if="c.call_count" class="text-xs text-ink-gray-4 shrink-0">{{ c.call_count }} cuộc</span>
                </div>
                <div v-if="!crmContacts.length" class="px-4 py-8 text-center text-sm text-ink-gray-4">
                  Không tìm thấy khách hàng nào
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Settings -->
          <div v-else-if="step === 3" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-ink-gray-7 mb-2">
                Agent AI <span class="text-red-500">*</span>
              </label>
              <div v-if="agentLoading" class="text-sm text-ink-gray-4 py-4 text-center">
                <FeatherIcon name="loader" class="h-4 w-4 animate-spin inline mr-2" />Đang tải...
              </div>
              <div v-else-if="!availableAgents.length" class="text-sm text-red-600 py-2 bg-red-50 rounded-lg px-3">
                Chưa cấu hình Agent. Vào <strong>Cài đặt AI</strong> để thêm Agent ID.
              </div>
              <div v-else class="grid grid-cols-2 gap-2">
                <button
                  v-for="a in availableAgents"
                  :key="a.key"
                  @click="form.agent_key = a.key"
                  class="border-2 rounded-xl px-4 py-3 text-left transition-all"
                  :class="form.agent_key === a.key
                    ? 'border-ink-gray-9 bg-ink-gray-9 text-white'
                    : 'border-outline-gray-modals hover:border-ink-gray-5 text-ink-gray-7'"
                >
                  <div class="text-sm font-medium">{{ a.label }}</div>
                  <div class="text-xs mt-0.5 opacity-60">{{ a.key }}</div>
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-ink-gray-7 mb-2">
                Thời gian giữa các cuộc gọi: <strong>{{ form.delay_seconds }}s</strong>
              </label>
              <input
                v-model.number="form.delay_seconds"
                type="range" min="1" max="10" step="1"
                class="w-full accent-ink-gray-9"
              />
              <div class="flex justify-between text-xs text-ink-gray-4 mt-1">
                <span>1s (nhanh nhất)</span><span>10s (chậm nhất)</span>
              </div>
            </div>

            <!-- Summary card -->
            <div class="rounded-xl bg-surface-gray-1 px-4 py-3 text-sm space-y-1">
              <p class="font-semibold text-ink-gray-8 mb-2">Tóm tắt chiến dịch</p>
              <p class="text-ink-gray-6">📋 <strong>{{ form.name }}</strong></p>
              <p class="text-ink-gray-6">👥 <strong>{{ validContacts.length }}</strong> liên hệ</p>
              <p class="text-ink-gray-6">🤖 Agent: <strong>{{ availableAgents.find(a => a.key === form.agent_key)?.label || '—' }}</strong></p>
              <p class="text-ink-gray-6">⏱ Delay: <strong>{{ form.delay_seconds }}s</strong> giữa mỗi cuộc gọi</p>
            </div>
          </div>

        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-outline-gray-modals flex justify-between items-center bg-surface-gray-1">
          <Button
            v-if="step > 1"
            variant="ghost"
            label="Quay lại"
            iconLeft="arrow-left"
            @click="step--"
          />
          <div v-else />
          <div class="flex gap-2">
            <Button variant="ghost" label="Hủy" @click="close" />
            <Button
              v-if="step < 3"
              variant="solid"
              label="Tiếp theo"
              iconRight="arrow-right"
              :disabled="!canProceed"
              @click="nextStep"
            />
            <Button
              v-else
              variant="solid"
              label="Tạo chiến dịch"
              iconLeft="check"
              :loading="submitting"
              :disabled="!canSubmit"
              @click="submit"
            />
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { Dialog, Button, FeatherIcon, call, toast } from 'frappe-ui'
import { ref, watch, computed } from 'vue'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close', 'created'])

const isOpen = ref(false)
watch(() => props.show, (v) => { isOpen.value = v }, { immediate: true })
watch(isOpen, (v) => { if (!v) emit('close') })

const step = ref(1)
const submitting = ref(false)

const stepLabels = ['Thông tin', 'Danh sách số', 'Cài đặt']
const stepSubtitles = [
  'Đặt tên và mô tả cho chiến dịch',
  'Thêm danh sách số điện thoại cần gọi',
  'Chọn AI Agent và thời gian giữa các cuộc gọi',
]

const form = ref({
  name: '',
  description: '',
  contacts: [],
  agent_key: '',
  delay_seconds: 3,
})

// ── Contact tabs ──────────────────────────────
const contactTabs = [
  { id: 'manual', label: 'Nhập tay' },
  { id: 'csv', label: 'Dán CSV' },
  { id: 'crm', label: 'Từ CRM' },
]
const contactTab = ref('manual')

function switchContactTab(tabId) {
  if (form.value.contacts.length > 0 && tabId !== contactTab.value) {
    form.value.contacts = []
  }
  contactTab.value = tabId
  if (tabId === 'crm' && !crmContacts.value.length) loadCrmContacts()
}

// ── CSV parsing ───────────────────────────────
const csvText = ref('')

function parseCsv() {
  const lines = csvText.value.split('\n').map(l => l.trim()).filter(Boolean)
  const result = []
  for (const line of lines) {
    const parts = line.split(',').map(p => p.trim())
    let name = '', phone = ''
    if (parts.length >= 2) {
      // Check if first part looks like a phone number
      if (/^\d{9,11}$/.test(parts[0].replace(/\D/g, ''))) {
        phone = parts[0]
        name = parts[1] || ''
      } else {
        name = parts[0]
        phone = parts[1]
      }
    } else {
      phone = parts[0]
    }
    const digits = phone.replace(/\D/g, '')
    if (digits.length >= 9) {
      result.push({ name, phone: digits })
    }
  }
  form.value.contacts = result
}

// ── CRM contacts ──────────────────────────────
const crmContacts = ref([])
const crmLoading = ref(false)
const crmSearch = ref('')
const selectedCrmIds = ref(new Set())
let crmSearchTimer = null

async function loadCrmContacts(search = '') {
  crmLoading.value = true
  try {
    const result = await call('voice_crm.api.proxy_get_contacts', { limit: 100, search: search || undefined })
    crmContacts.value = Array.isArray(result) ? result : []
  } catch (e) {
    crmContacts.value = []
  } finally {
    crmLoading.value = false
  }
}

function debouncedCrmSearch() {
  clearTimeout(crmSearchTimer)
  crmSearchTimer = setTimeout(() => loadCrmContacts(crmSearch.value), 400)
}

function toggleCrmContact(c) {
  const ids = new Set(selectedCrmIds.value)
  if (ids.has(c.id)) {
    ids.delete(c.id)
    form.value.contacts = form.value.contacts.filter(x => x._crmId !== c.id)
  } else {
    ids.add(c.id)
    form.value.contacts.push({ name: c.full_name || '', phone: c.phone, _crmId: c.id })
  }
  selectedCrmIds.value = ids
}

// ── Agent config ──────────────────────────────
const availableAgents = ref([])
const agentLoading = ref(false)

async function loadAgentConfig() {
  agentLoading.value = true
  try {
    const config = await call('voice_crm.api.proxy_get_client_config')
    if (config?.agents) {
      availableAgents.value = Object.entries(config.agents).map(([key, v]) => ({
        key, label: v.label,
      }))
      if (availableAgents.value.length && !form.value.agent_key) {
        form.value.agent_key = availableAgents.value[0].key
      }
    }
  } catch (e) {
    availableAgents.value = []
  } finally {
    agentLoading.value = false
  }
}

// ── Computed ──────────────────────────────────
const validContacts = computed(() =>
  form.value.contacts.filter(c => c.phone && c.phone.replace(/\D/g, '').length >= 9)
)

const canProceed = computed(() => {
  if (step.value === 1) return form.value.name.trim().length > 0
  if (step.value === 2) return validContacts.value.length > 0
  return false
})

const canSubmit = computed(() =>
  form.value.name.trim() && validContacts.value.length > 0 && form.value.agent_key
)

// ── Navigation ────────────────────────────────
function nextStep() {
  if (!canProceed.value) return
  if (step.value === 2) loadAgentConfig()
  step.value++
}

// ── Submit ────────────────────────────────────
async function submit() {
  if (!canSubmit.value) return
  submitting.value = true
  try {
    const contacts = validContacts.value.map(({ name, phone }) => ({ name, phone }))
    const result = await call('voice_crm.api.proxy_create_campaign', {
      name: form.value.name.trim(),
      description: form.value.description.trim(),
      agent_key: form.value.agent_key,
      contacts_json: JSON.stringify(contacts),
      delay_ms: form.value.delay_seconds * 1000,
    })
    toast({ title: `Đã tạo chiến dịch "${form.value.name}"`, variant: 'success' })
    emit('created', result)
    close()
  } catch (e) {
    toast({ title: 'Lỗi tạo chiến dịch: ' + (e.message || e), variant: 'error' })
  } finally {
    submitting.value = false
  }
}

// ── Reset & close ─────────────────────────────
function close() {
  emit('close')
}

watch(() => props.show, (v) => {
  if (v) {
    step.value = 1
    form.value = { name: '', description: '', contacts: [], agent_key: '', delay_seconds: 3 }
    contactTab.value = 'manual'
    csvText.value = ''
    crmSearch.value = ''
    selectedCrmIds.value = new Set()
    crmContacts.value = []
    availableAgents.value = []
  }
})
</script>
