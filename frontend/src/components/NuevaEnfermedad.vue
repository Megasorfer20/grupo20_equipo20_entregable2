<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir enfermedad</h1>
        <h3>Rellena por favor todos los campos</h3>

        <div>
            <label>Documento o nombre del paciente:</label>
            <input v-model="busqueda" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-if="pacienteEncontrado">
            <p><strong>Paciente:</strong> {{ paciente.nombre_completo }} (ID: {{ paciente.id }})</p>

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

const emit = defineEmits(['volver'])

const busqueda = ref('')
const paciente = ref(null)
const pacienteEncontrado = ref(false)

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

    paciente.value = resultado
    pacienteEncontrado.value = true
}

const enviarEnfermedad = async () => {
    if (sintomasSeleccionados.value.some((s) => s === '')) {
        alert('Todos los síntomas deben ser seleccionados.')
        return
    }

    const datos = {
        paciente_id: paciente.value.id,
        sintomas: sintomasSeleccionados.value,
        fecha_registro: new Date().toISOString().split('T')[0]
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.registrar_enfermedad_paciente(datos)
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
