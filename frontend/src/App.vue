<script setup lang="ts">
import Navbar from '@/components/common/Navbar.vue'
import SystemHealth from '@/components/SystemHealthCheck.vue'
import { useAppStore } from '@/stores/useAppStore'

const appStore = useAppStore()
</script>

<template>
    <div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
        <!-- Global Navigation -->
        <Navbar />

        <!-- Router View Area -->
        <main class="flex-1">
            <router-view />
        </main>

        <!-- Floating System Health Trigger -->
        <button
            @click="appStore.openHealthModal()"
            class="fixed bottom-4 right-4 z-50 bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3.5 py-2 rounded-full border border-slate-700 shadow-xl flex items-center gap-2 transition-all cursor-pointer hover:scale-105 backdrop-blur-sm"
        >
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>System Health</span>
        </button>

        <!-- System Health Modal -->
        <div
            v-if="appStore.isHealthModalOpen"
            class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
            @click.self="appStore.closeHealthModal()"
        >
            <div class="relative w-full max-w-xl">
                <button
                    @click="appStore.closeHealthModal()"
                    class="absolute -top-10 right-0 text-slate-400 hover:text-white text-sm bg-slate-800/80 px-3 py-1 rounded-full cursor-pointer hover:bg-slate-700"
                >
                    ✕ Close
                </button>
                <SystemHealth />
            </div>
        </div>
    </div>
</template>