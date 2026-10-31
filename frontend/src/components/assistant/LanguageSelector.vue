<script setup lang="ts">
import { useAssistantStore } from '@/stores/useAssistantStore'

const assistantStore = useAssistantStore()
</script>

<template>
  <div
    class="inline-flex items-center rounded-full bg-[#FFFDF8] border border-[#A7AD91]/40 p-1 shadow-xs"
    role="group"
    aria-label="Language selection"
  >
    <!-- Urdu Segment -->
    <button
      type="button"
      @click="assistantStore.setLanguage('ur')"
      :class="[
        assistantStore.language === 'ur'
          ? 'bg-[#76543D] text-[#FFFDF8] font-bold shadow-xs'
          : 'text-[#3D2B20] hover:text-[#76543D] hover:bg-[#F7F1E7]/60 font-medium'
      ]"
      class="h-[44px] min-h-[44px] px-5 rounded-full transition-all duration-200 cursor-pointer font-urdu text-[18px] flex items-center justify-center leading-none select-none"
      aria-label="اردو زبان منتخب کریں"
    >
      اردو
    </button>

    <!-- English Segment -->
    <button
      type="button"
      @click="assistantStore.setLanguage('en')"
      :class="[
        assistantStore.language === 'en'
          ? 'bg-[#76543D] text-[#FFFDF8] font-bold shadow-xs'
          : 'text-[#3D2B20] hover:text-[#76543D] hover:bg-[#F7F1E7]/60 font-medium'
      ]"
      class="h-[44px] min-h-[44px] px-5 rounded-full transition-all duration-200 cursor-pointer font-inter text-[18px] flex items-center justify-center leading-none select-none"
      aria-label="Select English language"
    >
      English
    </button>
  </div>
</template>
