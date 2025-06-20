<template>
    <section>
        <button @click="$emit('volver')">Volver</button>
        <h1>Editar paciente</h1>

        <div v-if="!pacienteEncontrado">
            <label>Buscar paciente por documento o nombre:</label>
            <input v-model="busqueda" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-else>
            <h3>Modifica los campos que quieras editar</h3>
            <form @submit.prevent="actualizarPaciente">
                <div>
                    <label>Nombre completo:</label>
                    <input v-model="paciente.nombre_completo" type="text" required />
                </div>

                <div>
                    <label>Fecha de nacimiento:</label>
                    <input v-model="paciente.fecha_nacimiento" type="date" required />
                </div>

                <div>
                    <label>Género:</label>
                    <select v-model="paciente.genero" required>
                        <option disabled value="">Selecciona un género</option>
                        <option>Masculino</option>
                        <option>Femenino</option>
                        <option>Otro</option>
                    </select>
                </div>

                <div>
                    <label>Número de identificación:</label>
                    <span>{{ paciente.numero_identificacion }}</span>
                </div>

                <div>
                    <label>Celular de contacto:</label>
                    <input v-model="paciente.celular_contacto" type="number" required />
                </div>

                <div>
                    <label>Fecha de registro:</label>
                    <span>{{ paciente.fecha_registro }}</span>
                </div>

                <button type="submit">Guardar cambios</button>
            </form>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['volver'])

const busqueda = ref('')
const paciente = ref(null)
const pacienteEncontrado = ref(false)

const buscarPaciente = async () => {
    if (!busqueda.value) {
        alert('Por favor ingresa un documento o nombre.')
        return
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.buscar_paciente(busqueda.value)

    if (!respuesta || Object.keys(respuesta).length === 0) {
        alert('Paciente no encontrado.')
        return
    }

    paciente.value = respuesta
    pacienteEncontrado.value = true
}

const actualizarPaciente = async () => {
    const campos = Object.values(paciente.value)
    if (campos.some((v) => v === '' || v === null)) {
        alert('Por favor, llena todos los campos.')
        return
    }

    await window.pywebview?.ready
    const respuesta = await window.pywebview.api.actualizar_paciente(paciente.value)
    alert(respuesta)
    emit('volver')
}
</script>

<style scoped></style>
