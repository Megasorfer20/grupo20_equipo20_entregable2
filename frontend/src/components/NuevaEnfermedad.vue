<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir enfermedad</h1>
        <h3>Rellena por favor todos los campos</h3>

        <div v-if="!pacienteStore.paciente">
            <label>Documento o nombre del paciente:</label>
            <input v-model="busqueda" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-if="pacienteStore.paciente">
            <p><strong>Paciente:</strong> {{ pacienteStore.paciente.nombre_completo }}</p>

            <div v-for="(s, i) in sintomasSeleccionados" :key="i">
                <label>Síntoma {{ i + 1 }}:</label>
                <select v-model="sintomasSeleccionados[i]">
                    <option disabled value="">Selecciona un síntoma</option>
                    <option v-for="sint in listaSintomas" :key="sint.id" :value="sint.sintoma">
                        {{ sint.sintoma }}
                    </option>
                </select>
            </div>

            <button @click="enviarEnfermedad">Enviar</button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { pacienteStore } from '@/stores/pacienteStore'

const emit = defineEmits(['volver'])

const busqueda = ref('')
const listaSintomas = ref([])
const sintomasSeleccionados = ref(['', '', ''])

const buscarPaciente = async () => {
    if (!busqueda.value) {
        alert('Ingresa documento o nombre')
        return
    }

    await window.pywebview?.ready
    const resultado = await window.pywebview.api.buscar_paciente(busqueda.value)

    if (!resultado || Object.keys(resultado).length === 0) {
        alert('Paciente no encontrado.')
        return
    }

    pacienteStore.paciente = resultado
    pacienteStore.enfermedades = await window.pywebview.api.obtener_enfermedades_paciente(resultado.id)
}

const enviarEnfermedad = async () => {
    if (!pacienteStore.paciente) {
        alert('No hay paciente cargado.')
        return
    }

    if (sintomasSeleccionados.value.some((s) => s === '')) {
        alert('Todos los síntomas deben ser seleccionados.')
        return
    }

    const datos = {
        paciente_id: pacienteStore.paciente.id,
        sintomas: sintomasSeleccionados.value,
        fecha_registro: new Date().toISOString()
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.registrar_enfermedad_paciente(datos)

    pacienteStore.enfermedades = await window.pywebview.api.obtener_enfermedades_paciente(pacienteStore.paciente.id)

    alert(respuesta)
    emit('volver')
}

onMounted(async () => {
    await window.pywebview?.ready
    const lista = await window.pywebview.api.obtener_sintomas()
    listaSintomas.value = lista
})
</script>

<style scoped></style>
