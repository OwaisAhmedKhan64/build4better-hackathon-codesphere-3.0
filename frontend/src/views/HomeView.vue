<script setup lang="ts">
import { useAssistantStore } from '@/stores/useAssistantStore'
import AssistantHero from '@/components/assistant/AssistantHero.vue'
import AssistantButton from '@/components/assistant/AssistantButton.vue'
import ConversationCard from '@/components/assistant/ConversationCard.vue'

const assistantStore = useAssistantStore()
</script>

<template>
  <div
    class="min-h-full py-4 sm:py-6 px-4 sm:px-6"
    :dir="assistantStore.isUrdu ? 'rtl' : 'ltr'"
  >
    <div class="max-w-[720px] mx-auto space-y-6 sm:space-y-8">
      
      <!-- 1. Centered Welcoming Hero (No cards or borders) -->
      <section aria-label="Hero Section">
        <AssistantHero />
      </section>

      <!-- 2. Main Microphone Interaction (The focal point of the page) -->
      <section aria-label="Microphone Interaction">
        <AssistantButton />
      </section>

      <!-- 3. Conversation & Response (Displayed ONLY after real backend response) -->
      <section aria-live="polite">
        <ConversationCard />
      </section>

    </div>
  </div>
</template>
