const AdvancedCache = require("./src/cache");
const DatabaseMock = require("./src/simulator");

async function runDemo() {

  console.log("INICIANDO PRUEBA DE ESTRÉS CONCURRENTE");
 
  const cache = new AdvancedCache({
    maxSize: 5,
    defaultTTL: 3000,
    cleanupInterval: 2000
  });

  const db = new DatabaseMock();
  const PRODUCT_KEY = "product_101";
  let peticionCount = 50;

  console.log(`[*] Lanzando ${peticionCount} peticiones en PARALELO para la llave "${PRODUCT_KEY}"...`);
  
  const poolPeticiones = [];
  for (let i = 1; i <= peticionCount; i++) {
    poolPeticiones.push(
      cache.getOrFetch(PRODUCT_KEY, () => db.findProductById(PRODUCT_KEY))
    );
  }

  const resultados = await Promise.all(poolPeticiones);

  console.log(`\n✅ Las ${peticionCount} peticiones concurrentes fueron resueltas con éxito.`);
  console.log(`[Métricas DB] Consultas reales hechas al driver SQL: ${db.totalQueries}`);
  console.log(`Muestra del payload retornado:`, resultados[0]);
  


  console.log(`[*] Volviendo a consultar la llave "${PRODUCT_KEY}" (Debe ser un Cache HIT)...`);
  const startHitTime = Date.now();
  const hitResult = await cache.getOrFetch(PRODUCT_KEY, () => db.findProductById(PRODUCT_KEY));
  const elapsedHitTime = Date.now() - startHitTime;

  console.log(`[HIT Exitoso] Obtenido en: ${elapsedHitTime}ms (DB no fue tocada)`);
  console.log(`[Métricas DB] Consultas totales acumuladas en DB: ${db.totalQueries}`);

  cache.close();
  console.log(" Demostración finalizada con éxito.");
}

runDemo().catch(console.error);