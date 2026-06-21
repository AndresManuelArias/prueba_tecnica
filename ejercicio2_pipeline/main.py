import tracemalloc
from datetime import datetime
from pipeline.generator import data_stream_generator
from pipeline.stages import filter_stage, transform_stage, window_aggregation_stage
from pipeline.core import DeclarativePipeline

def run_pipeline_demo():
    print("=" * 60)
    print("🚀 INICIANDO DEMOSTRACIÓN DEL PIPELINE DE DATOS PEREZOSO")
    print("=" * 60)

    tracemalloc.start()

    TOTAL_REGISTROS = 100_000
    print(f"[*] Preparando fuente de datos: Stream masivo de {TOTAL_REGISTROS:,} registros.")


    source_stream = data_stream_generator(total_records=TOTAL_REGISTROS)

    pipeline_stages = [
        lambda stream: filter_stage(stream, target_type="heartbeat"),  # Etapa 1: Filtrar ruidos
        transform_stage,                                               # Etapa 2: Aplicar tasas/metadatos
        lambda stream: window_aggregation_stage(stream, window_minutes=5) # Etapa 3: Agrupar por ventanas
    ]


    pipeline_engine = DeclarativePipeline(stages=pipeline_stages)
    processed_windows = pipeline_engine.execute(source_stream)

    print("[*] Tuberías conectadas con éxito empleando Lazy Evaluation.")
    print("[*] Procesando y consumiendo el stream bloque por bloque...")
    print("-" * 60)

    total_windows_emitted = 0
    total_records_processed = 0

    for i, window in enumerate(processed_windows):
        total_windows_emitted += 1
        total_records_processed += len(window)
        
        if i < 3:
            window_start = window[0]["timestamp"].strftime("%H:%M:%S")
            window_end = window[-1]["timestamp"].strftime("%H:%M:%S")
            print(f"📦 [Ventana {i+1}] Emitida con {len(window):>4} eventos | Rango Temporal Local: {window_start} -> {window_end}")

    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_kb = peak_mem / 1024

    print("-" * 60)
    print("📊 RESULTADOS DE LA AUDITORÍA DE RENDIMIENTO (SENIOR METRICS)")
    print("-" * 60)
    print(f"✅ Total de registros procesados:  {total_records_processed:,}")
    print(f"✅ Total de ventanas de 5m creadas: {total_windows_emitted}")
    print(f"🔥 PICO MÁXIMO DE MEMORIA RAM UTILIZADO: {peak_kb:.2f} KB")
    print("=" * 60)
    print("💡 CONCLUSIÓN: La memoria se mantuvo baja y plana debido a que")
    print("   los datos fluyeron bajo demanda sin cargarse en listas globales.")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline_demo()