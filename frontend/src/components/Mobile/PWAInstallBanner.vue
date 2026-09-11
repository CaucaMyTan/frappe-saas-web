<template>
  <!-- Android / Chrome: native install prompt available -->
  <Transition name="slide-up">
    <div
      v-if="showAndroid"
      class="fixed bottom-0 left-0 right-0 z-50 bg-surface-white border-t border-outline-gray-modals px-4 py-3 shadow-lg"
    >
      <div class="flex items-center gap-3">
        <img :src="'/assets/crm/manifest/manifest-icon-192.maskable.png'" class="h-10 w-10 rounded-xl shrink-0" alt="Voice CRM" />
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold text-ink-gray-9">Cài Voice CRM</p>
          <p class="text-xs text-ink-gray-5">Thêm vào màn hình chính để dùng như app</p>
        </div>
        <Button variant="solid" label="Cài đặt" size="sm" @click="install" />
        <button class="text-ink-gray-4 hover:text-ink-gray-6 p-1" @click="dismiss">
          <FeatherIcon name="x" class="h-4 w-4" />
        </button>
      </div>
    </div>
  </Transition>

  <!-- iOS: manual instruction (no native prompt on Safari) -->
  <Transition name="slide-up">
    <div
      v-if="showIOS"
      class="fixed bottom-0 left-0 right-0 z-50 bg-ink-gray-9 text-white px-4 py-4 shadow-lg"
    >
      <div class="flex items-start justify-between gap-2 mb-2">
        <p class="text-sm font-semibold">Thêm vào màn hình chính</p>
        <button class="text-white/60 hover:text-white p-0.5" @click="dismiss">
          <FeatherIcon name="x" class="h-4 w-4" />
        </button>
      </div>
      <ol class="space-y-1.5 text-xs text-white/80">
        <li class="flex items-center gap-2">
          <span class="bg-white/20 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold shrink-0">1</span>
          Nhấn nút <strong class="text-white mx-1">Chia sẻ</strong>
          <span class="text-white/60">(biểu tượng □↑ ở thanh dưới Safari)</span>
        </li>
        <li class="flex items-center gap-2">
          <span class="bg-white/20 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold shrink-0">2</span>
          Chọn <strong class="text-white">"Thêm vào Màn hình chính"</strong>
        </li>
        <li class="flex items-center gap-2">
          <span class="bg-white/20 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold shrink-0">3</span>
          Nhấn <strong class="text-white">Thêm</strong> — xong!
        </li>
      </ol>
    </div>
  </Transition>
</template>

<script setup>
import { FeatherIcon, Button } from 'frappe-ui'
import { ref, computed, onMounted } from 'vue'
import { usePWAInstall } from '@/composables/usePWAInstall'

const DISMISS_KEY = 'pwa_install_dismissed'

const { isInstallable, isInstalled, promptInstall } = usePWAInstall()
const dismissed = ref(false)

onMounted(() => {
  dismissed.value = !!localStorage.getItem(DISMISS_KEY)
})

const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent)
const isInStandaloneMode = isInstalled.value

// Show Android banner when native prompt is available
const showAndroid = computed(
  () => !dismissed.value && !isInStandaloneMode && isInstallable.value && !isIOS,
)

// Show iOS guide once, on Safari, when not already installed
const showIOS = computed(
  () => !dismissed.value && !isInStandaloneMode && isIOS && !isInstallable.value,
)

async function install() {
  await promptInstall()
  dismissed.value = true
}

function dismiss() {
  dismissed.value = true
  localStorage.setItem(DISMISS_KEY, '1')
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
