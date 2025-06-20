<template>
    <section>
        <h1>Añadir tratamiento</h1>
        <h3>Rellena por favor todos los campos</h3>

        <div class="p-4">
            <label for="cantidad">Número de medicamentos:</label>
            <input type="number" v-model.number="cantidad" min="1" id="cantidad" />

            <button @click="generarInputs">Continuar</button>

            <div v-if="medicamentos.length > 0" class="mt-3">
                <div v-for="(medicamento, index) in medicamentos" :key="index" class="mb-2">
                    <label>Medicamento {{ index + 1 }}:</label>
                    <input type="text" v-model="medicamentos[index]" placeholder="Nombre del medicamento" />
                </div>

                <button @click="enviarMedicamentos">Enviar</button>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const cantidad = ref(0)
const medicamentos = ref([])

const generarInputs = () => {
    if (cantidad.value < 1) {
        alert('Debes ingresar un número válido de medicamentos')
        return
    }
    medicamentos.value = Array(cantidad.value).fill('')
}

const enviarMedicamentos = () => {
    if (medicamentos.value.some((m) => m.trim() === '')) {
        alert('Todos los campos son obligatorios')
        return
    }

    const listaFinal = [...medicamentos.value]
    console.log('Medicamentos enviados:', listaFinal)
}
</script>

<style scoped>
input {
  margin-right: 10px;
  padding: 4px;
}
button {
  margin-top: 10px;
  padding: 6px 12px;
}
</style>
