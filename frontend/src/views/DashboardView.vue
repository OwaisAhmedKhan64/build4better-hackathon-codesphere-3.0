<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/useAppStore'

const appStore = useAppStore()
const featureTitle = ref('')
const activeTab = ref<'overview' | 'features'>('overview')
</script>

<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
                <h1 class="text-2xl font-bold text-white tracking-tight">Project Workspace</h1>
                <p class="text-sm text-slate-400 mt-1">
                    Team {{ appStore.teamName }} workspace &bull; Add your hackathon features below.
                </p>
            </div>

            <div class="flex items-center gap-2">
                <button
                    @click="activeTab = 'overview'"
                    :class="activeTab === 'overview' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'"
                    class="px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors"
                >
                    Overview
                </button>
                <button
                    @click="activeTab = 'features'"
                    :class="activeTab === 'features' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'"
                    class="px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors"
                >
                    Feature Sandbox
                </button>
            </div>
        </div>

        <!-- Main Workspace Area -->
        <div v-if="activeTab === 'overview'" class="space-y-6">
            <div class="border border-dashed border-slate-800 rounded-2xl p-12 text-center space-y-4 bg-slate-900/30">
                <div class="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto text-xl">
                    🚀
                </div>
                <div class="space-y-1">
                    <h3 class="text-base font-semibold text-white">Main Canvas Ready</h3>
                    <p class="text-sm text-slate-400 max-w-md mx-auto">
                        This view (<code class="text-xs bg-slate-800 px-1.5 py-0.5 rounded text-indigo-300">src/views/DashboardView.vue</code>) is wired to Vue Router and ready for your hackathon core app logic.
                    </p>
                </div>
            </div>
        </div>

        <div v-else class="space-y-4">
            <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
                <h3 class="text-base font-semibold text-white mb-2">Sandbox Input</h3>
                <p class="text-xs text-slate-400 mb-4">Quick reactive state demo using Vue 3 script setup.</p>
                <input
                    v-model="featureTitle"
                    type="text"
                    placeholder="Type to test reactivity..."
                    class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <p v-if="featureTitle" class="mt-3 text-xs text-indigo-300 bg-indigo-950/40 border border-indigo-800/50 p-2.5 rounded-lg">
                    Live input: {{ featureTitle }}
                </p>
            </div>
        </div>
    </div>
</template>
