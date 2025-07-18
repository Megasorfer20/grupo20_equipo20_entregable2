<template>
    <Bienvenidos v-if="panels[0]" @nuevoPacienteRoute="() => togglePanel(1)" @editarPacienteRoute="() => togglePanel(2)" @consultarPacienteRoute="() => togglePanel(3)" @listarPacientes="() => togglePanel(7)" />

    <NuevoPaciente v-if="panels[1]" @volver="() => togglePanel(0)" />

    <EditarPaciente v-if="panels[2]" @volver="() => togglePanel(0)" />

    <ConsultarPaciente v-if="panels[3]" @volver="() => togglePanel(0)" @nuevaEnfermedadRoute="() => togglePanel(4)" @nuevaAlergiaRoute="() => togglePanel(5)" @nuevTratamientoRoute="() => togglePanel(6)" />

    <NuevaEnfermedad v-if="panels[4]" @volver="() => togglePanel(3)" />

    <NuevaAlergia v-if="panels[5]" @volver="() => togglePanel(3)" />

    <NuevoTratamiento v-if="panels[6]" @volver="() => togglePanel(3)" />

    <ListarPacientes v-if="panels[7]" :visible="panels[7]" @volver="() => togglePanel(0)" />
</template>

<script setup>
import Bienvenidos from '@/components/Bienvenida.vue'
import NuevoPaciente from '@/components/NuevoPaciente.vue'
import EditarPaciente from '@/components/EditarPaciente.vue'
import ConsultarPaciente from '@/components/ConsultarPaciente.vue'
import NuevaEnfermedad from '@/components/NuevaEnfermedad.vue'
import NuevaAlergia from '@/components/NuevaAlergia.vue'
import NuevoTratamiento from '@/components/NuevoTratamiento.vue'
import { pacienteStore } from '@/stores/pacienteStore'

import { ref } from 'vue'
import ListarPacientes from './components/ListarPacientes.vue'

const panels = ref([true, false, false, false, false, false, false, false])

const togglePanel = (openPanel) => {
    panels.value = panels.value.map((_, index) => index === openPanel)

    if (openPanel === 0) {
        pacienteStore.paciente = null
        pacienteStore.enfermedades = []
        pacienteStore.alergias = []
        pacienteStore.tratamientos = []
    }
}
</script>

<style>
@import '@/assets/main.css';
</style>
