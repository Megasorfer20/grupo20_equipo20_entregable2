<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir tratamiento</h1>
        <h3>Rellena por favor todos los campos</h3>

        <div v-if="!pacienteStore.paciente" class="p-4">
            <label for="busqueda">Documento o nombre del paciente:</label>
            <input v-model="busqueda" id="busqueda" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-if="pacienteStore.paciente">
            <p><strong>Paciente:</strong> {{ pacienteStore.paciente.nombre_completo }}</p>

            <label for="cantidad">Número de medicamentos:</label>
            <input type="number" v-model.number="cantidad" min="1" id="cantidad" />

            <button @click="generarInputs">Continuar</button>

            <div v-if="medicamentos.length > 0" class="mt-3">
                <div v-for="(med, index) in medicamentos" :key="index" class="mb-2">
                    <label>Medicamento {{ index + 1 }}:</label>
                    <input type="text" v-model="med.nombre" placeholder="Nombre del medicamento" />

                    <label>Dosis:</label>
                    <input type="text" v-model="med.dosis" placeholder="Ej: 2 veces al día" />
                </div>

                <button @click="enviarTratamiento">Enviar tratamiento</button>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { pacienteStore } from '@/stores/pacienteStore'

const emit = defineEmits(['volver'])
const busqueda = ref('')

const cantidad = ref(0)
const medicamentos = ref([])

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
    pacienteStore.alergias = await window.pywebview.api.obtener_alergias_paciente(resultado.id)
    pacienteStore.tratamientos = await window.pywebview.api.obtener_tratamientos_paciente(resultado.id)
}

const generarInputs = () => {
    if (cantidad.value < 1) {
        alert('Debes ingresar un número válido de medicamentos')
        return
    }
    medicamentos.value = Array.from({ length: cantidad.value }, () => ({
        nombre: '',
        dosis: ''
    }))
}

const enviarTratamiento = async () => {
    if (!pacienteStore.paciente) {
        alert('No hay paciente cargado.')
        return
    }

    if (medicamentos.value.some((m) => m.nombre.trim() === '' || m.dosis.trim() === '')) {
        alert('Todos los campos son obligatorios')
        return
    }

    const datos = {
        paciente_id: pacienteStore.paciente.id,
        medicamentos: medicamentos.value.map((m) => m.nombre),
        dosis_medicamentos: medicamentos.value.map((m) => m.dosis),
        fecha_registro: new Date().toISOString().split('T')[0]
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.add_tratamiento(datos)

    // Actualiza el store con los nuevos tratamientos
    pacienteStore.tratamientos = await window.pywebview.api.obtener_tratamientos_paciente(pacienteStore.paciente.id)

    alert(respuesta)
    emit('volver')
}
</script>

<style scoped></style>
