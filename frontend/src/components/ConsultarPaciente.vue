<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <div v-if="!pacienteStore.paciente">
            <h1>Consultar datos del paciente</h1>
            <input v-model="busqueda" placeholder="Nombre o documento" />
            <button @click="buscarPaciente">Buscar</button>
        </div>

        <div v-else>
            <h1>Información del paciente</h1>
            <p><strong>Nombre:</strong> {{ pacienteStore.paciente.nombre_completo }}</p>
            <p><strong>Apellido:</strong> {{ pacienteStore.paciente.apellidos }}</p>
            <p><strong>Edad:</strong> {{ calcularEdad(pacienteStore.paciente.fecha_nacimiento) }}</p>
            <p><strong>Fecha nacimiento:</strong> {{ pacienteStore.paciente.fecha_nacimiento }}</p>
            <p><strong>Género:</strong> {{ pacienteStore.paciente.genero }}</p>
            <p><strong>Identificación:</strong> {{ pacienteStore.paciente.numero_identificacion }}</p>
            <p><strong>Celular:</strong> {{ pacienteStore.paciente.celular_contacto }}</p>
            <p><strong>Fecha de registro:</strong> {{ pacienteStore.paciente.fecha_registro }}</p>

            <h3>Más información del paciente</h3>
            <div>
                <button @click="mostrarModal('enfermedades')">Enfermedades paciente</button>
                <button @click="mostrarModal('alergias')">Alergias paciente</button>
                <button @click="mostrarModal('tratamientos')">Tratamientos paciente</button>
            </div>

            <h3>¿Qué deseas hacer?</h3>
            <div>
                <button @click="$emit('nuevaEnfermedadRoute')">Añadir enfermedad</button>
                <button @click="$emit('nuevaAlergiaRoute')">Añadir alergia</button>
                <button @click="$emit('nuevTratamientoRoute')">Añadir tratamiento</button>
                <button @click="eliminarPaciente">Eliminar paciente</button>
            </div>
        </div>

        <!-- MODALES -->
        <div v-if="modal === 'enfermedades'" class="modal">
            <div class="modal-content">
                <h3>Enfermedades del paciente</h3>
                <table>
                    <tr>
                        <th>Enfermedad</th>
                        <th>Síntomas</th>
                        <th>Fecha</th>
                    </tr>
                    <tr v-for="e in pacienteStore.enfermedades" :key="e.id">
                        <td>{{ e.nombre || 'Enfermedad no especificada' }}</td>
                        <td>{{ e.sintomas.join(', ') }}</td>
                        <td>{{ e.fecha_registro }}</td>
                    </tr>
                </table>
                <button @click="cerrarModal">Cerrar</button>
            </div>
        </div>

        <div v-if="modal === 'alergias'" class="modal">
            <div class="modal-content">
                <h3>Alergias del paciente</h3>
                <table>
                    <tr>
                        <th>Alergeno</th>
                        <th>Síntomas</th>
                        <th>Fecha</th>
                    </tr>
                    <tr v-for="a in pacienteStore.alergias" :key="a.id">
                        <td>{{ a.alergeno }}</td>
                        <td>{{ a.sintomas.join(', ') }}</td>
                        <td>{{ a.fecha_registro }}</td>
                    </tr>
                </table>
                <button @click="cerrarModal">Cerrar</button>
            </div>
        </div>

        <div v-if="modal === 'tratamientos'" class="modal">
            <div class="modal-content scrollable">
                <h3>Tratamientos del paciente</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Medicamento</th>
                            <th>Dosis</th>
                        </tr>
                    </thead>
                    <tbody>
                        <template v-for="t in pacienteStore.tratamientos" :key="t.id">
                            <tr v-for="(med, i) in t.medicamentos" :key="`${t.id}-${i}`">
                                <td>{{ t.fecha_registro }}</td>
                                <td>{{ med }}</td>
                                <td>{{ t.dosis_medicamentos[i] || 'Sin especificar' }}</td>
                            </tr>
                        </template>
                    </tbody>
                </table>
                <button @click="cerrarModal">Cerrar</button>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { pacienteStore } from '@/stores/pacienteStore'

const emit = defineEmits(['volver', 'nuevaEnfermedadRoute', 'nuevaAlergiaRoute', 'nuevTratamientoRoute'])
const busqueda = ref('')
const modal = ref(null)

const eliminarPaciente = async () => {
    if (!pacienteStore.paciente) {
        alert('No hay paciente seleccionado para eliminar.')
        return
    }

    const confirmacion = confirm('¿Estás seguro de que deseas eliminar este paciente? Esta acción no se puede deshacer.')
    if (confirmacion) {
        await window.pywebview?.ready
        await window.pywebview.api.deletar_paciente(pacienteStore.paciente.id)
        pacienteStore.paciente = null
        pacienteStore.enfermedades = []
        pacienteStore.alergias = []
        pacienteStore.tratamientos = []
        emit('volver')
    }
}

const buscarPaciente = async () => {
    if (!busqueda.value) {
        alert('Por favor, ingresa nombre o número de documento.')
        return
    }

    await window.pywebview?.ready
    const res = await window.pywebview.api.buscar_paciente(busqueda.value)

    if (!res || Object.keys(res).length === 0) {
        alert('Paciente no encontrado.')
        emit('volver')
        return
    }

    // Guardar en el store
    pacienteStore.paciente = res
    pacienteStore.enfermedades = await window.pywebview.api.obtener_enfermedades_paciente(res.id)
    pacienteStore.alergias = await window.pywebview.api.obtener_alergias_paciente(res.id)
    pacienteStore.tratamientos = await window.pywebview.api.obtener_tratamientos_paciente(res.id)
}

const mostrarModal = (tipo) => {
    modal.value = tipo
}

const cerrarModal = () => {
    modal.value = null
}

const calcularEdad = (fechaNacimiento) => {
    const hoy = new Date()
    const nacimiento = new Date(fechaNacimiento)
    let edad = hoy.getFullYear() - nacimiento.getFullYear()
    const m = hoy.getMonth() - nacimiento.getMonth()
    if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--
    }
    return edad
}

</script>

<style scoped>
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background: white;
    margin: 10% auto;
    padding: 20px;
    max-width: 600px;
    max-height: 70vh;
    overflow-y: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1em;
}
th,
td {
    border: 1px solid #ccc;
    padding: 8px;
}
</style>
