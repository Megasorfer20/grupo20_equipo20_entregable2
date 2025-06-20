<template>
    <section>
        <h1>¡Bienvenidos al sistema de gestión de pacientes!</h1>
        <h3>¿Qué deseas hacer?</h3>

        <div>
            <button @click="$emit('nuevoPacienteRoute')">Añadir paciente</button>
            <button @click="$emit('editarPacienteRoute')">Actualizar paciente</button>
            <button @click="$emit('consultarPacienteRoute')">Consultar paciente</button>
        </div>
    </section>
</template>

<script setup></script>

<style scoped></style>
