/**
 * Estructura de un nodo dentro del almacenamiento de la caché.
 * @typedef {Object} CacheNode
 * @property {*} value - El dato real almacenado.
 * @property {number} expiresAt - Timestamp en milisegundos cuando este dato muere.
 */

class AdvancedCache {
  /**
   * @param {Object} options
   * @param {number} options.maxSize - Capacidad máxima de elementos permitidos.
   * @param {number} options.defaultTTL - Tiempo de vida por defecto en milisegundos.
   */
  constructor({ maxSize = 1000, defaultTTL = 60000 } = {}) {
    this.maxSize = maxSize;
    this.defaultTTL = defaultTTL;
    
    this.storage = new Map();
  }

  /**
   * Guarda un elemento en la caché con un TTL específico.
   * Aplica la política de evicción LRU si se supera el tamaño máximo.
   * @param {string} key 
   * @param {*} value 
   * @param {number} [ttl] - TTL opcional en milisegundos para esta llave.
   */
  set(key, value, ttl = this.defaultTTL) {
    const now = Date.now();
    const expiresAt = now + ttl;

    if (this.storage.has(key)) {
      this.storage.delete(key);
    } 
    else if (this.storage.size >= this.maxSize) {
      const oldestKey = this.storage.keys().next().value;
      console.warn(`⚠️ [Cache Eviction] Límite alcanzado (${this.maxSize}). Expulsando la llave menos usada: "${oldestKey}"`);
      this.storage.delete(oldestKey);
    }

    this.storage.set(key, { value, expiresAt });
  }

  /**
   * Obtiene un elemento de la caché si existe y no ha expirado (Evicción Pasiva).
   * @param {string} key 
   * @returns {*|null} Retorna el valor o null si no existe/expiró.
   */
  get(key) {
    if (!this.storage.has(key)) {
      return null;
    }

    const node = this.storage.get(key);
    const now = Date.now();

    // Verificación Pasiva de TTL
    if (now > node.expiresAt) {
      console.log(`⏱️ [Passive TTL] La llave "${key}" ha expirado. Eliminando...`);
      this.storage.delete(key);
      return null;
    }

    // Toque LRU: Como fue accedida, la refrescamos moviéndola al final del Map
    this.storage.delete(key);
    this.storage.set(key, node);

    return node.value;
  }


  get size() {
    return this.storage.size;
  }
}

module.exports = AdvancedCache;