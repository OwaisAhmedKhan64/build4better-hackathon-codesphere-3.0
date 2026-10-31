<script setup lang="ts">
import { onMounted } from 'vue'
import { useAssistantStore } from '@/stores/useAssistantStore'
import { useAppStore } from '@/stores/useAppStore'
import LanguageSelector from '@/components/assistant/LanguageSelector.vue'

const assistantStore = useAssistantStore()
const appStore = useAppStore()
const isDev = import.meta.env.DEV

onMounted(() => {
  assistantStore.checkBackendHealth()
})
</script>

<template>
  <header class="w-full border-b border-[#A7AD91]/25 bg-[#FFFDF8]/80 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-[720px] mx-auto px-4 sm:px-6 h-24 flex items-center justify-between">
      <!-- Prominent Brand with Tagline -->
      <div class="flex flex-col justify-center select-none py-1">
        <span
          class="font-bold text-[#3D2B20] text-[26px] sm:text-[36px] tracking-tight leading-none"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-fraunces'"
        >
          {{ assistantStore.currentAppName }}
        </span>
        <span
          class="text-[11px] sm:text-[15px] text-[#3D2B20]/65 tracking-wide mt-0.5 font-medium leading-tight"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          {{ assistantStore.t.brandTagline }}
        </span>
      </div>

      <!-- Controls: Language Selector, Conditional Connection Warning, Dev Diagnostics -->
      <div class="flex items-center gap-3">
        <!-- Backend Connection Warning (Visible ONLY when backend is unreachable) -->
        <div
          v-if="!assistantStore.isBackendReachable"
          class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#F3DADA] border border-[#E2B6B6] text-[#7A2222] text-xs sm:text-sm font-semibold animate-pulse"
          role="status"
          aria-live="polite"
        >
          <span class="w-2 h-2 rounded-full bg-rose-600"></span>
          <span :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'">
            {{ assistantStore.t.connectionProblem }}
          </span>
        </div>

        <!-- Language Selector -->
        <LanguageSelector />

        <!-- Development Mode Only: Subtle diagnostic dot trigger -->
        <button
          v-if="isDev"
          type="button"
          @click="appStore.openHealthModal()"
          class="p-1.5 text-[#3D2B20]/40 hover:text-[#76543D] rounded-full transition-colors cursor-pointer"
          title="System Diagnostics (Dev Mode)"
          aria-label="Open Diagnostics"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-[#7F8A68] inline-block"></span>
        </button>
      </div>
    </div>
  </header>
</template>
