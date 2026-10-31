<script setup lang="ts">
import { computed } from 'vue'
import { useAssistantStore } from '@/stores/useAssistantStore'

const assistantStore = useAssistantStore()

const dotColorClass = computed(() => {
  if (assistantStore.errorCode) return 'bg-rose-500'
  switch (assistantStore.workflowState) {
    case 'idle':
      return 'bg-[#76543D]/40'
    case 'requesting_permissions':
      return 'bg-amber-600 animate-pulse'
    case 'ready':
      return 'bg-[#7F8A68]' // Deeper sage status dot
    case 'listening':
      return 'bg-[#76543D] animate-ping'
    case 'processing':
      return 'bg-[#76543D] animate-pulse'
    default:
      return 'bg-[#7F8A68]'
  }
})
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center space-y-3 sm:space-y-4 select-none">
    
    <!-- Focal Point: Circular Microphone Button (160px - 176px) with Concentric Rings -->
    <div class="relative flex items-center justify-center p-4">
      
      <!-- Outer Concentric Ring 2 -->
      <div
        class="absolute -inset-3 sm:-inset-4 rounded-full border border-[#76543D]/10 bg-[#76543D]/[0.02] pointer-events-none transition-all duration-300"
      ></div>

      <!-- Outer Concentric Ring 1 -->
      <div
        class="absolute -inset-1 sm:-inset-1.5 rounded-full border border-[#76543D]/15 bg-[#76543D]/[0.04] pointer-events-none transition-all duration-200"
      ></div>

      <!-- Main Button -->
      <button
        type="button"
        @click="assistantStore.handleMainAction()"
        :disabled="assistantStore.isProcessing"
        :class="[
          assistantStore.isListening ? 'pulse-listening scale-[1.02]' : 'hover:scale-[1.03]',
          assistantStore.isProcessing ? 'opacity-90 cursor-wait' : 'cursor-pointer active:scale-[0.98]'
        ]"
        class="relative z-10 w-40 h-40 sm:w-44 sm:h-44 rounded-full bg-[#76543D] hover:bg-[#634531] text-[#FFFDF8] shadow-xl shadow-[#76543D]/20 transition-all duration-300 flex flex-col items-center justify-center p-3.5 focus:outline-none focus:ring-4 focus:ring-[#A7AD91]/40 border-2 border-[#FFFDF8]/20"
        :aria-label="assistantStore.buttonText"
      >
        <!-- Elegant SVG Microphone Artwork -->
        <div class="mb-1.5 transition-transform duration-300">
          <svg
            v-if="!assistantStore.isProcessing"
            class="w-9 h-9 stroke-current fill-none"
            viewBox="0 0 24 24"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" x2="12" y1="19" y2="22" />
            <line x1="8" x2="16" y1="22" y2="22" />
          </svg>

          <!-- Processing Spinner -->
          <svg
            v-else
            class="w-9 h-9 animate-spin stroke-current fill-none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>

        <!-- Button Label (At least 20px font size) -->
        <span
          :class="[
            assistantStore.isUrdu ? 'font-urdu font-bold' : 'font-inter font-bold leading-tight'
          ]"
          class="text-[19px] sm:text-[20px] text-center px-1"
        >
          {{ assistantStore.buttonText }}
        </span>
      </button>
    </div>

    <!-- Active Screen-Sharing Indicator (Requirement 5) -->
    <div
      v-if="assistantStore.isScreenSharing"
      class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-[#7F8A68]/15 border border-[#7F8A68]/30 text-[#3D2B20] text-xs sm:text-sm font-medium transition-all"
    >
      <span class="w-1.5 h-1.5 rounded-full bg-[#7F8A68] animate-pulse"></span>
      <span :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'">
        {{ assistantStore.t.screenSharingActive }}
      </span>
    </div>

    <!-- Single Status Line and Status Dot (Requirement 4 & 8) -->
    <div class="flex items-center justify-center gap-2 text-base sm:text-[17px] text-[#3D2B20]/85 min-h-[28px]">
      <span class="w-2.5 h-2.5 rounded-full shrink-0" :class="dotColorClass"></span>
      <span
        :class="[
          assistantStore.isUrdu ? 'font-urdu font-medium' : 'font-inter font-medium'
        ]"
      >
        {{ assistantStore.currentStatusText }}
      </span>
    </div>

    <!-- Next-Step Calm Hint Line (Requirement 7) -->
    <p
      class="text-sm sm:text-[15px] text-[#3D2B20]/65 font-normal max-w-md mx-auto text-center px-2 min-h-[22px]"
      :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
    >
      {{ assistantStore.nextStepHint }}
    </p>

    <!-- Secondary Stop Assistant Button (Requirement 2) -->
    <div class="pt-1">
      <button
        v-if="assistantStore.workflowState !== 'idle'"
        type="button"
        @click="assistantStore.stopAssistant()"
        class="min-h-[48px] min-w-[180px] px-6 py-2.5 rounded-full border-[1.5px] border-[#76543D] text-[#76543D] bg-transparent hover:bg-[#76543D]/10 focus:outline-none focus:ring-2 focus:ring-[#76543D]/40 text-[18px] font-semibold transition-all duration-200 cursor-pointer flex items-center justify-center gap-2 no-underline active:scale-98 shadow-2xs"
        :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
      >
        {{ assistantStore.t.stopAssistant }}
      </button>
    </div>

  </div>
</template>
