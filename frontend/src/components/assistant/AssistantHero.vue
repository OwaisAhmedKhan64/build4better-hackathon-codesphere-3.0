<script setup lang="ts">
import { useAssistantStore } from '@/stores/useAssistantStore'

const assistantStore = useAssistantStore()
</script>

<template>
  <div class="text-center space-y-2 sm:space-y-3 max-w-2xl mx-auto pt-1 sm:pt-2">
    <!-- Centered Welcoming Heading -->
    <h1
      :class="[
        assistantStore.isUrdu
          ? 'font-urdu font-bold'
          : 'font-fraunces font-bold tracking-tight'
      ]"
      class="text-2xl sm:text-3xl md:text-[34px] leading-tight text-[#3D2B20]"
    >
      {{ assistantStore.t.heroHeading }}
    </h1>

    <!-- Short Supporting Text (At least 18px body text on desktop) -->
    <p
      :class="[
        assistantStore.isUrdu
          ? 'font-urdu'
          : 'font-inter leading-relaxed'
      ]"
      class="text-[17px] sm:text-[18px] md:text-[19px] text-[#3D2B20]/80 font-normal max-w-xl mx-auto"
    >
      {{ assistantStore.t.heroSupporting }}
    </p>
  </div>
</template>
