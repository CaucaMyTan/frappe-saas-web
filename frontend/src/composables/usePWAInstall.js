import { ref, onMounted, onUnmounted } from 'vue'

// Captures the beforeinstallprompt event so we can trigger it later.
// Also detects if already installed (standalone mode).

const deferredPrompt = ref(null)
const isInstallable = ref(false)
const isInstalled = ref(
  window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true,
)

function handleBeforeInstall(e) {
  e.preventDefault()
  deferredPrompt.value = e
  if (!isInstalled.value) {
    isInstallable.value = true
  }
}

function handleAppInstalled() {
  isInstalled.value = true
  isInstallable.value = false
  deferredPrompt.value = null
}

// Register listeners once at module level so only one copy exists
window.addEventListener('beforeinstallprompt', handleBeforeInstall)
window.addEventListener('appinstalled', handleAppInstalled)

export function usePWAInstall() {
  async function promptInstall() {
    if (!deferredPrompt.value) return false
    deferredPrompt.value.prompt()
    const { outcome } = await deferredPrompt.value.userChoice
    deferredPrompt.value = null
    isInstallable.value = false
    return outcome === 'accepted'
  }

  return { isInstallable, isInstalled, promptInstall }
}
