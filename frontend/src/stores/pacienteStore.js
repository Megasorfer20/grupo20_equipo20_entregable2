import { reactive } from 'vue'

export const pacienteStore = reactive({
  paciente: null,
  enfermedades: [],
  alergias: [],
  tratamientos: [],
})