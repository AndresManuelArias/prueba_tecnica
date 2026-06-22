const { sleep } = require("./utils");

class DatabaseMock {
  constructor() {
    this.queryCounter = 0;
  }

  /**
   * Simula una operación de I/O pesada (ej: buscar un producto en DB).
   * @param {string} productId 
   * @returns {Promise<Object>} El registro fresco de la DB.
   */
  async findProductById(productId) {
    this.queryCounter++;
    await sleep(1500);
    
    return {
      id: productId,
      name: "Licencia",
      price: 850.00,
      fetchedAt: new Date().toLocaleTimeString()
    };
  }

  get totalQueries() {
    return this.queryCounter;
  }
}

module.exports = DatabaseMock;