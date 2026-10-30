<script setup lang="ts">
import { useAppStore } from '@/stores/useAppStore'

const appStore = useAppStore()
</script>

<template>
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-6">
                <router-link to="/" class="flex items-center gap-2.5 group">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                        BM
                    </div>
                    <div>
                        <span class="font-bold text-white text-base tracking-tight block">Build4Better</span>
                        <span class="text-[10px] text-slate-400 block -mt-1 tracking-wider uppercase">Team {{ appStore.teamName }}</span>
                    </div>
                </router-link>

                <nav class="hidden md:flex items-center gap-1 pl-4 border-l border-slate-800 text-sm">
                    <router-link
                        to="/"
                        class="px-3 py-1.5 rounded-md text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
                        active-class="bg-slate-800 text-white font-medium"
                    >
                        Home
                    </router-link>
                    <router-link
                        to="/dashboard"
                        class="px-3 py-1.5 rounded-md text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
                        active-class="bg-slate-800 text-white font-medium"
                    >
                        Workspace
                    </router-link>
                </nav>
            </div>

            <div class="flex items-center gap-3">
                <button
                    @click="appStore.openHealthModal()"
                    class="bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-xs font-medium px-3 py-1.5 rounded-full border border-slate-700/80 flex items-center gap-2 transition-all cursor-pointer hover:border-slate-600"
                >
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>System Status</span>
                </button>
            </div>
        </div>
    </header>
</template>
