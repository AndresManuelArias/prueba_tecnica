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
   * @param {number} options.cleanupInterval - Intervalo del barrido activo en milisegundos.
   */
  constructor({ maxSize = 1000, defaultTTL = 60000, cleanupInterval = 10000 } = {}) {
    this.maxSize = maxSize;
    this.defaultTTL = defaultTTL;
    this.cleanupInterval = cleanupInterval;
    

    this.storage = new Map();

    this.inFlightPromises = new Map();

    this.startExpiredCleaner();
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
    } else if (this.storage.size >= this.maxSize) {
      const oldestKey = this.storage.keys().next().value;
      console.warn(`[Cache Eviction] Límite alcanzado (${this.maxSize}). Expulsando por LRU: "${oldestKey}"`);
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

    if (now > node.expiresAt) {
      console.log(`[Passive TTL] La llave "${key}" ha expirado. Eliminando...`);
      this.storage.delete(key);
      return null;
    }


    this.storage.delete(key);
    this.storage.set(key, node);

    return node.value;
  }

  /**
   * Método de consulta de alta concurrencia con mitigación de estampida (Cache Stampede Protection).
   * Si el dato no existe, agrupa todas las llamadas concurrentes en una única promesa hacia el fetcher.
   * * @param {string} key - La llave a buscar.
   * @param {Function} fetcher - Función asíncrona que va a la fuente original (DB/API) si no hay caché.
   * @param {number} [ttl] - TTL personalizado para esta llave.
   * @returns {Promise<*>} El valor final resuelto.
   */
  async getOrFetch(key, fetcher, ttl = this.defaultTTL) {
    const cachedValue = this.get(key);
    if (cachedValue !== null) {
      return cachedValue;
    }

    if (this.inFlightPromises.has(key)) {
      console.log(`[Promise Coalescing] Petición concurrente acoplada para la llave: "${key}". Evitando llamada duplicada a la DB.`);
      return this.inFlightPromises.get(key);
    }

    console.log(`[Cache Miss] Llave "${key}" no disponible. Creando promesa única de carga hacia la fuente original...`);
    
    const fetchPromise = (async () => {
      try {
        const freshData = await fetcher();
        
        this.set(key, freshData, ttl);
        
        return freshData;
      } finally {
        this.inFlightPromises.delete(key);
      }
    })();

    this.inFlightPromises.set(key, fetchPromise);

    return fetchPromise;
  }

  startExpiredCleaner() {
    this.cleanerIntervalId = setInterval(() => {
      const now = Date.now();
      let deletedCount = 0;

      for (const [key, node] of this.storage.entries()) {
        if (now > node.expiresAt) {
          this.storage.delete(key);
          deletedCount++;
        } else {
          break;
        }
      }

      if (deletedCount > 0) {
        console.log(`[Active Cleaner] Barrido ejecutado. Se eliminaron ${deletedCount} llaves expiradas en segundo plano.`);
      }
    }, this.cleanupInterval);

    if (this.cleanerIntervalId.unref) {
      this.cleanerIntervalId.unref();
    }
  }

  close() {
    if (this.cleanerIntervalId) {
      clearInterval(this.cleanerIntervalId);
    }
  }

  get size() {
    return this.storage.size;
  }
}

module.exports = AdvancedCache;