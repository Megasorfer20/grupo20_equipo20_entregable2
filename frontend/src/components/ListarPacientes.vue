<template>
    <section>
        <button @click="$emit('volver')">Volver</button>
        <div class="modal-content">
            <h3>Listado de pacientes</h3>
            <table>
                <tr>
                    <th>Documento</th>
                    <th>Nombres</th>
                    <th>Apellidos</th>
                </tr>
                <tr v-for="a in pacientes" :key="a.id">
                    <td>{{ a.numero_identificacion }}</td>
                    <td>{{ a.nombre_completo }}</td>
                    <td>{{ a.apellidos }}</td>
                </tr>
            </table>
        </div>
    </section>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
const emit = defineEmits(['volver'])
const props = defineProps({ visible: Boolean })

let pacientes = ref([])

const cargarPacientes = async () => {
    if (window.pywebview) {
        pacientes.value = await window.pywebview.api.listar_pacientes()
    }
}

onMounted(() => {
    if (props.visible) {
        cargarPacientes()
    }
})

watch(
    () => props.visible,
    (nuevo) => {
        if (nuevo) {
            cargarPacientes()
        }
    }
)

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
.modal-content {
    background: white;
    margin: 10px auto;
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
