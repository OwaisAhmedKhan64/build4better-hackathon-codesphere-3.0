import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
    const teamName = ref('Black Mesa')
    const members = ref(['Owais Ahmed Khan', 'Barira Waris', 'Naveed Zahir'])
    const isHealthModalOpen = ref(false)

    function openHealthModal() {
        isHealthModalOpen.value = true
    }

    function closeHealthModal() {
        isHealthModalOpen.value = false
    }

    function toggleHealthModal() {
        isHealthModalOpen.value = !isHealthModalOpen.value
    }

    return {
        teamName,
        members,
        isHealthModalOpen,
        openHealthModal,
        closeHealthModal,
        toggleHealthModal,
    }
})
