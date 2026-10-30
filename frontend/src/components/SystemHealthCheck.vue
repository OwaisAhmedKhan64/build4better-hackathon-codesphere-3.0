<!-- frontend/src/components/SystemHealth.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'
import type { Note, HealthStatus } from '@/types'

const backendStatus = ref<HealthStatus>('loading')
const dbStatus = ref<HealthStatus>('loading')
const backendMessage = ref('')
const dbMessage = ref('')

const notes = ref<Note[]>([])
const newTitle = ref('')
const isSubmitting = ref(false)

const checkBackend = async () => {
    backendStatus.value = 'loading'
    try {
        const res = await api.get('/')
        backendStatus.value = 'connected'
        backendMessage.value = res.data.message || 'FastAPI is online'
    } catch (err: any) {
        backendStatus.value = 'error'
        backendMessage.value = err.message || 'Cannot reach FastAPI'
    }
}

const checkDatabase = async () => {
    dbStatus.value = 'loading'
    try {
        const res = await api.get('/test-db')
        dbStatus.value = 'connected'
        notes.value = res.data.data || []
        dbMessage.value = `Connected! (${notes.value.length} notes found)`
    } catch (err: any) {
        dbStatus.value = 'error'
        dbMessage.value = err.response?.data?.detail || err.message || 'Database query failed'
    }
}

const handleAddNote = async () => {
    if (!newTitle.value.trim()) return
    isSubmitting.value = true
    try {
        await api.post(`/test-db?title=${encodeURIComponent(newTitle.value)}`)
        newTitle.value = ''
        await checkDatabase()
    } catch (err: any) {
        alert('Failed to insert: ' + (err.response?.data?.detail || err.message))
    } finally {
        isSubmitting.value = false
    }
}

const runAllChecks = () => {
    checkBackend()
    checkDatabase()
}

onMounted(() => {
    runAllChecks()
})
</script>

<template>
    <div
        class="w-full max-w-xl bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-2xl space-y-5 text-slate-100">
        <div class="text-center space-y-1">
            <h2 class="text-xl font-bold text-white">System Diagnostics</h2>
            <p class="text-xs text-slate-400">FastAPI &bull; Supabase Live Check</p>
        </div>

        <!-- Health Cards -->
        <div class="grid grid-cols-2 gap-3">
            <!-- FastAPI -->
            <div class="bg-slate-950/70 border border-slate-800 rounded-xl p-3">
                <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">FastAPI</span>
                    <span :class="{
                        'text-amber-400': backendStatus === 'loading',
                        'text-emerald-400': backendStatus === 'connected',
                        'text-rose-400': backendStatus === 'error'
                    }" class="text-xs font-semibold">
                        ● {{ backendStatus.toUpperCase() }}
                    </span>
                </div>
                <p class="text-xs text-slate-300 truncate">{{ backendMessage || 'Checking...' }}</p>
            </div>

            <!-- Supabase -->
            <div class="bg-slate-950/70 border border-slate-800 rounded-xl p-3">
                <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Supabase</span>
                    <span :class="{
                        'text-amber-400': dbStatus === 'loading',
                        'text-emerald-400': dbStatus === 'connected',
                        'text-rose-400': dbStatus === 'error'
                    }" class="text-xs font-semibold">
                        ● {{ dbStatus.toUpperCase() }}
                    </span>
                </div>
                <p class="text-xs text-slate-300 truncate">{{ dbMessage || 'Checking...' }}</p>
            </div>
        </div>

        <!-- Database Interaction -->
        <div class="bg-slate-950/40 border border-slate-800/80 rounded-xl p-4 space-y-3">
            <form @submit.prevent="handleAddNote" class="flex gap-2">
                <input v-model="newTitle" type="text" placeholder="Test row insert..."
                    class="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                <button type="submit" :disabled="isSubmitting || !newTitle.trim()"
                    class="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold px-3 py-1.5 rounded-lg">
                    Insert
                </button>
            </form>

            <!-- Records list -->
            <div class="max-h-32 overflow-y-auto space-y-1.5 pr-1">
                <div v-for="note in notes" :key="note.id"
                    class="bg-slate-900/80 border border-slate-800 p-2 rounded flex items-center justify-between text-xs">
                    <span class="text-slate-200 truncate">{{ note.title }}</span>
                    <span class="text-slate-500 text-[10px]">#{{ note.id }}</span>
                </div>
            </div>
        </div>

        <!-- Controls -->
        <div class="flex justify-between items-center text-xs text-slate-400">
            <button @click="runAllChecks" class="hover:text-white transition-colors">
                ↻ Refresh Checks
            </button>
        </div>
    </div>
</template>