<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Añadir paciente</h1>
        <h3>Rellena por favor todos los campos</h3>

        <form @submit.prevent="enviarPaciente">
            <div>
                <label>Nombres :</label>
                <input v-model="paciente.nombre_completo" type="text" required pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$" maxlength="100" />
            </div>

            <div>
                <label>Apellidos:</label>
                <input v-model="paciente.apellidos" type="text" required pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$" maxlength="100" />
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
                    <option>No binario</option>
                    <option>Prefiero no decirlo</option>
                </select>
            </div>

            <div>
                <label>Número de identificación:</label>
                <input v-model="paciente.numero_identificacion" type="text" required pattern="^[0-9]+$" inputmode="numeric" />
            </div>

            <div>
                <label>Celular de contacto:</label>
                <input v-model="paciente.celular_contacto" type="text" required pattern="^[0-9]{10}$" maxlength="10" inputmode="numeric" />
            </div>

            <button type="submit">Enviar</button>
        </form>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['volver'])

const esValidoNumero = (numero) => /^[0-9]{10}$/.test(numero)
const esNombreValido = (nombre) => /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre)
const esNumero = (valor) => /^[0-9]+$/.test(valor)

const paciente = ref({
    nombre_completo: '',
    apellidos: '',
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

    if (!esValidoNumero(paciente.value.celular_contacto)) {
        alert('Número de celular deben tener exactamente 10 dígitos.')
        return
    }

    if (!esNombreValido(paciente.value.nombre_completo)) {
        alert('El nombre solo debe contener letras y espacios.')
        return
    }

    if (!esNumero(paciente.value.numero_identificacion)) {
        alert('El número de identificación debe contener solo dígitos.')
        return
    }

    const fechaHoy = new Date().toISOString()
    const datosFinales = {
        ...paciente.value,
        fecha_registro: fechaHoy
    }

    console.log('Paciente registrado:', datosFinales)

    await window.pywebview?.ready

    const respuesta = await window.pywebview.api.add_paciente(datosFinales)

    alert(respuesta)
    emit('volver')
}
</script>

<style scoped></style>
