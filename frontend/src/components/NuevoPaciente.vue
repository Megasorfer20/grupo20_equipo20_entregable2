<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir paciente</h1>
        <h3>Rellena por favor todos los campos</h3>

        <form @submit.prevent="enviarPaciente">
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
                <input v-model="paciente.numero_identificacion" type="number" required />
            </div>

            <div>
                <label>Celular de contacto:</label>
                <input v-model="paciente.celular_contacto" type="number" required />
            </div>

            <button type="submit">Enviar</button>
        </form>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['volver'])

const paciente = ref({
    nombre_completo: '',
    fecha_nacimiento: '',
    genero: '',
    numero_identificacion: '',
    celular_contacto: ''
})

const enviarPaciente = async () => {
    const campos = Object.values(paciente.value)
    if (campos.some((v) => v === '' || v === null)) {
        alert('Por favor, llena todos los campos.')
        return
    }

    const fechaHoy = new Date().toISOString().split('T')[0]
    const datosFinales = {
        ...paciente.value,
        fecha_registro: fechaHoy
    }

    console.log('Paciente registrado:', datosFinales)

    await window.pywebview?.ready;

    const respuesta = await window.pywebview.api.add_paciente(datosFinales);

    alert(respuesta);
    emit('volver')
}
</script>

<style scoped></style>
