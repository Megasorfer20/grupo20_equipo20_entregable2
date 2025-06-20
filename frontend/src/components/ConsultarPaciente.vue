<template>
    <section>
        <button @click="$emit('volver')">Volver</button>

        <h1>Consultar datos del paciente</h1>
        <p>Información del paciente: <br /></p>

        <h3>Más información del paciente</h3>
        <div>
            <button>Enfermedades paciente</button>
            <button>Alergias Paciente</button>
            <button>Tratamientos Paciente</button>
        </div>

        <h3>¿Qué deseas hacer?</h3>

        <div>
            <button @click="$emit('nuevaEnfermedadRoute')">Añadir enfermedad</button>
            <button @click="$emit('nuevaAlergiaRoute')">Añadir alergia</button>
            <button @click="$emit('nuevTratamientoRoute')">Añadir tratamiento</button>
        </div>
    </section>
</template>

<script setup></script>

<style scoped></style>
