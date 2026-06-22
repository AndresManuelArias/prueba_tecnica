/**
 * Permite emular latencias de red reales de forma no bloqueante.
 * @param {number} ms - Milisegundos de espera.
 */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

module.exports = { sleep };