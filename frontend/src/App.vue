<script setup lang="ts">
import { onMounted } from 'vue'
import Navbar from '@/components/common/Navbar.vue'
import SystemHealth from '@/components/SystemHealthCheck.vue'
import { useAppStore } from '@/stores/useAppStore'
import { useAssistantStore } from '@/stores/useAssistantStore'

const appStore = useAppStore()
const assistantStore = useAssistantStore()

onMounted(() => {
  document.documentElement.dir = assistantStore.language === 'ur' ? 'rtl' : 'ltr'
  document.documentElement.lang = assistantStore.language
})
</script>

<template>
  <div class="min-h-screen bg-[#F7F1E7] text-[#3D2B20] flex flex-col font-inter selection:bg-[#76543D]/20 selection:text-[#76543D]">
    <!-- Minimal Header -->
    <Navbar />

    <!-- Main Content Area -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- System Health Diagnostics Modal (Preserved) -->
    <div
      v-if="appStore.isHealthModalOpen"
      class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      @click.self="appStore.closeHealthModal()"
    >
      <div class="relative w-full max-w-xl">
        <button
          @click="appStore.closeHealthModal()"
          class="absolute -top-10 right-0 text-slate-200 hover:text-white text-sm bg-slate-800/90 px-3 py-1 rounded-full cursor-pointer hover:bg-slate-700 shadow"
        >
          ✕ Close
        </button>
        <SystemHealth />
      </div>
    </div>
  </div>
</template>
