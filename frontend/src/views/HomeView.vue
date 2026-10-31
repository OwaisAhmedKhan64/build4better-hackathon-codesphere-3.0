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

      <!-- 2. Main Microphone Interaction & Picture-in-Picture Integration -->
      <section aria-label="Microphone Interaction">
        
        <!-- TELEPORT INTO FLOATING PIP WINDOW (When Document PiP is open) -->
        <Teleport
          v-if="assistantStore.isPipOpen && assistantStore.pipMountTarget"
          :to="assistantStore.pipMountTarget"
        >
          <AssistantButton in-pip />
        </Teleport>

        <!-- IN-TAB CONTROLS (When PiP is closed or not yet active) -->
        <div v-if="!assistantStore.isPipOpen" class="space-y-4">
          <AssistantButton />

          <!-- Reopen Floating PiP Button (if assistant is active but PiP was closed) -->
          <div
            v-if="assistantStore.workflowState !== 'idle'"
            class="text-center pt-1"
          >
            <button
              type="button"
              @click="assistantStore.openPipWindow()"
              class="text-xs sm:text-sm text-[#76543D] hover:text-[#5f422f] underline cursor-pointer font-medium transition-colors"
              :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
            >
              ⧉ {{ assistantStore.t.reopenPip }}
            </button>
          </div>
        </div>

        <!-- MAIN PAGE GUIDANCE CARD (Displayed when PiP is floating over other pages) -->
        <div
          v-else
          class="bg-[#FFFDF8] border border-[#A7AD91]/35 rounded-3xl p-6 sm:p-8 text-center space-y-4 shadow-sm"
        >
          <!-- Active Screen Sharing Tag -->
          <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#7F8A68]/15 text-[#3D2B20] text-xs sm:text-sm font-medium">
            <span class="w-2 h-2 rounded-full bg-[#7F8A68] animate-pulse"></span>
            <span :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'">
              {{ assistantStore.t.screenSharingActive }}
            </span>
          </div>

          <!-- PiP Active Heading -->
          <h2
            class="text-xl sm:text-2xl font-bold text-[#3D2B20]"
            :class="assistantStore.isUrdu ? 'font-urdu' : 'font-fraunces'"
          >
            {{ assistantStore.t.pipActiveHeading }}
          </h2>

          <!-- Prominent Main Page Hint (Requirement 9) -->
          <p
            class="text-base sm:text-lg text-[#3D2B20]/80 max-w-md mx-auto leading-relaxed"
            :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
          >
            {{ assistantStore.t.pipSwitchHint }}
          </p>

          <!-- Controls to return controls to tab or stop -->
          <div class="pt-2 flex flex-wrap items-center justify-center gap-3">
            <button
              type="button"
              @click="assistantStore.closePipWindow()"
              class="px-5 py-2.5 rounded-full border-[1.5px] border-[#76543D] text-[#76543D] hover:bg-[#76543D]/10 text-sm sm:text-base font-semibold transition-all cursor-pointer shadow-2xs"
              :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
            >
              {{ assistantStore.t.bringControlsBack }}
            </button>

            <button
              type="button"
              @click="assistantStore.stopAssistant()"
              class="px-5 py-2.5 rounded-full bg-[#76543D] hover:bg-[#5f422f] text-[#FFFDF8] text-sm sm:text-base font-semibold transition-all cursor-pointer shadow-sm"
              :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
            >
              {{ assistantStore.t.stopAssistant }}
            </button>
          </div>
        </div>

        <!-- PiP Unsupported Hint (Requirement 7) -->
        <div
          v-if="assistantStore.pipUnsupportedNotice && !assistantStore.isPipOpen"
          class="mt-4 max-w-md mx-auto text-xs sm:text-sm text-[#76543D]/80 bg-[#FFFDF8] border border-[#A7AD91]/30 rounded-2xl p-3 text-center shadow-2xs"
          :class="assistantStore.isUrdu ? 'font-urdu' : 'font-inter'"
        >
          💡 {{ assistantStore.t.pipUnsupportedHint }}
        </div>

      </section>

      <!-- 3. Conversation & Response (Full transcript, large AI response & scam warning on main page) -->
      <section aria-live="polite">
        <ConversationCard />
      </section>

    </div>
  </div>
</template>
