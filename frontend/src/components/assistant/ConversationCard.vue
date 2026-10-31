<script setup lang="ts">
import { useAssistantStore } from '@/stores/useAssistantStore'

const assistantStore = useAssistantStore()
</script>

<template>
  <div v-if="assistantStore.hasResponse" class="w-full space-y-5 pt-2">
    
    <!-- 1. Dedicated Scam Warning Banner (Shown ONLY when backend returns is_scam_warning: true) -->
    <div
      v-if="assistantStore.isScamWarning"
      class="w-full bg-[#F3DADA] border-2 border-[#E2B6B6] rounded-3xl p-5 sm:p-6 shadow-sm space-y-3 text-[#7A2222]"
      role="alert"
    >
      <div class="flex items-center gap-3">
        <svg class="w-6 h-6 shrink-0 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <h3
          :class="assistantStore.isUrdu ? 'font-urdu font-bold' : 'font-inter text-lg font-bold'"
        >
          {{ assistantStore.t.scamNoticeTitle }}
        </h3>
      </div>

      <p
        :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter text-base leading-relaxed'"
      >
        {{ assistantStore.t.scamNoticeText }}
      </p>

      <div class="pt-1 text-sm font-semibold opacity-95">
        {{ assistantStore.t.scamNoticeAdvice }}
      </div>
    </div>

    <!-- 2. Main Conversation Card (Surfaces: #FFFDF8 ivory) -->
    <div
      class="w-full bg-[#FFFDF8] border border-[#A7AD91]/35 rounded-3xl p-5 sm:p-7 shadow-sm space-y-5"
    >
      <!-- User Transcript Section -->
      <div class="space-y-1 pb-3 border-b border-[#A7AD91]/20">
        <span
          class="text-xs uppercase font-bold tracking-wider text-[#76543D]"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          {{ assistantStore.t.userSaid }}
        </span>
        <p
          class="text-lg sm:text-xl text-[#3D2B20]/85"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter italic'"
        >
          "{{ assistantStore.transcript }}"
        </p>
      </div>

      <!-- AI Response Section: The Largest Text in the Conversation Section -->
      <div class="space-y-1.5">
        <span
          class="text-xs uppercase font-bold tracking-wider text-[#3D2B20]/60"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          {{ assistantStore.t.aiSaid }}
        </span>
        <p
          class="text-[#3D2B20] font-medium"
          :class="[
            assistantStore.isUrdu
              ? 'font-urdu text-2xl sm:text-3xl'
              : 'font-fraunces text-2xl sm:text-3xl leading-snug'
          ]"
        >
          {{ assistantStore.aiResponse }}
        </p>
      </div>

      <!-- Action Step (If provided by backend) -->
      <div
        v-if="assistantStore.suggestedAction"
        class="pt-2 border-t border-[#A7AD91]/20 flex items-center gap-2.5"
      >
        <span
          class="px-2.5 py-1 rounded-lg bg-[#A7AD91]/30 text-[#3D2B20] text-xs font-bold uppercase tracking-wider shrink-0"
        >
          {{ assistantStore.t.nextStep }}
        </span>
        <span
          class="text-base sm:text-lg font-bold text-[#76543D]"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          {{ assistantStore.suggestedAction }}
        </span>
      </div>

      <!-- Conversation Controls: Repeat Response & Ask Another Question -->
      <div class="pt-3 border-t border-[#A7AD91]/20 flex flex-wrap items-center gap-3">
        <!-- Repeat Response Button -->
        <button
          type="button"
          @click="assistantStore.repeatResponse()"
          class="px-5 py-2.5 rounded-full bg-[#F7F1E7] hover:bg-[#ebdcc8] text-[#76543D] border border-[#A7AD91]/40 font-semibold text-base flex items-center gap-2 cursor-pointer transition-all duration-200 active:scale-95 shadow-2xs"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          <svg class="w-5 h-5 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
          </svg>
          <span>{{ assistantStore.t.repeatResponse }}</span>
        </button>

        <!-- Ask Another Question Button -->
        <button
          type="button"
          @click="assistantStore.askAnother()"
          class="px-5 py-2.5 rounded-full bg-[#76543D] hover:bg-[#5f422f] text-[#FFFDF8] font-semibold text-base flex items-center gap-2 cursor-pointer transition-all duration-200 active:scale-95 shadow-sm"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          <svg class="w-5 h-5 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
          </svg>
          <span>{{ assistantStore.t.askAnother }}</span>
        </button>
      </div>

    </div>
  </div>
</template>
