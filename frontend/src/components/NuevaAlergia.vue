<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir alergia</h1>
        <h3>Rellena por favor todos los campos</h3>

        <div v-if="!pacienteStore.paciente">
            <label>Documento o nombre del paciente:</label>
            <input v-model="busqueda" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-if="pacienteStore.paciente">
            <p><strong>Paciente:</strong> {{ pacienteStore.paciente.nombre_completo }}</p>

            <div>
                <label>Alergeno:</label>
                <input v-model="alergia.alergeno" type="text" required />
            </div>

            <div>
                <label>Número de síntomas:</label>
                <input type="number" v-model.number="cantidadSintomas" min="1" />
                <button @click="generarSelects">Generar</button>
            </div>

            <div v-if="sintomasSeleccionados.length > 0">
                <div v-for="(id, index) in sintomasSeleccionados" :key="index">
                    <label>Síntoma {{ index + 1 }}:</label>
                    <select v-model="sintomasSeleccionados[index]">
                        <option disabled value="">Selecciona un síntoma</option>
                        <option v-for="s in listaSintomas" :key="s.id" :value="s.id">
                            {{ s.sintoma }}
                        </option>
                    </select>
                </div>
            </div>

            <button @click="enviarAlergia">Enviar</button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { pacienteStore } from '@/stores/pacienteStore'

const emit = defineEmits(['volver'])

const busqueda = ref('')
const listaSintomas = ref([])
const cantidadSintomas = ref(0)
const sintomasSeleccionados = ref([])

const alergia = ref({
    alergeno: ''
})

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
    pacienteStore.alergias = await window.pywebview.api.obtener_alergias_paciente(resultado.id)
}

const generarSelects = () => {
    if (cantidadSintomas.value < 1) {
        alert('Debes indicar al menos un síntoma')
        return
    }
    sintomasSeleccionados.value = Array(cantidadSintomas.value).fill('')
}

const enviarAlergia = async () => {
    if (!alergia.value.alergeno.trim() || sintomasSeleccionados.value.some((s) => s === '')) {
        alert('Todos los campos son obligatorios')
        return
    }

    const sintomasNombres = sintomasSeleccionados.value.map((id) => {
        const sintomaObj = listaSintomas.value.find((s) => s.id === id)
        return sintomaObj ? sintomaObj.sintoma : ''
    })

    const datos = {
        paciente_id: pacienteStore.paciente.id,
        alergeno: alergia.value.alergeno.trim(),
        sintomas: sintomasNombres,
        fecha_registro: new Date().toISOString().split('T')[0]
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.add_alergia(datos)

    pacienteStore.alergias = await window.pywebview.api.obtener_alergias_paciente(pacienteStore.paciente.id)

    alert(respuesta)
    emit('volver')
}

onMounted(async () => {
    await window.pywebview?.ready
    listaSintomas.value = await window.pywebview.api.obtener_sintomas()
})
</script>

<style scoped></style>
