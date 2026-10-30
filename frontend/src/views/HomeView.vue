<script setup lang="ts">
import { useAppStore } from '@/stores/useAppStore'

const appStore = useAppStore()
</script>

<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <!-- Hero Section -->
        <div class="text-center max-w-3xl mx-auto space-y-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold tracking-wide">
                <span>CodeSphere 3.0 &bull; Build4Better Hackathon</span>
            </div>

            <h1 class="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
                Welcome to <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-violet-400 to-purple-400">Team {{ appStore.teamName }}</span>
            </h1>

            <p class="text-base sm:text-lg text-slate-400 leading-relaxed">
                Full-stack starter kit wired with Vue 3, Tailwind CSS v4, Pinia, Vue Router, FastAPI, and Supabase. Ready for rapid feature development tomorrow!
            </p>

            <div class="flex items-center justify-center gap-4 pt-2">
                <router-link
                    to="/dashboard"
                    class="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-5 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition-all text-sm hover:scale-[1.02]"
                >
                    Open Workspace &rarr;
                </router-link>

                <button
                    @click="appStore.openHealthModal()"
                    class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium px-5 py-2.5 rounded-xl transition-all text-sm"
                >
                    Run Diagnostics
                </button>
            </div>
        </div>

        <!-- Team & Architecture Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            <!-- Team Card -->
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
                <div class="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4">
                    👥
                </div>
                <h3 class="text-base font-semibold text-white mb-2">Team Members</h3>
                <ul class="space-y-1.5 text-sm text-slate-400">
                    <li v-for="member in appStore.members" :key="member" class="flex items-center gap-2">
                        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
                        <span>{{ member }}</span>
                    </li>
                </ul>
            </div>

            <!-- Tech Stack Card -->
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
                <div class="w-10 h-10 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400 mb-4">
                    ⚡
                </div>
                <h3 class="text-base font-semibold text-white mb-2">Tech Stack</h3>
                <p class="text-sm text-slate-400 leading-relaxed">
                    Vue 3 (Composition API) + Tailwind CSS v4 on the frontend; FastAPI + Supabase PostgreSQL on the backend.
                </p>
            </div>

            <!-- Architecture Card -->
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
                <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4">
                    🛡️
                </div>
                <h3 class="text-base font-semibold text-white mb-2">Multi-Member Ready</h3>
                <p class="text-sm text-slate-400 leading-relaxed">
                    Modular views, stores, and routers allow teammates to build independently without git conflicts.
                </p>
            </div>
        </div>
    </div>
</template>
