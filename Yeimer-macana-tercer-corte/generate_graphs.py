# Script: Genera gráfica "clicks_by_user.png" a partir de assets/data/clickstream_data.csv
import os
import sys
import pandas as pd
import matplotlib
# For headless environments (server/CI) force Agg
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

OUT_DIR = os.path.join("assets", "images")
CSV_PATH = os.path.join("assets", "data", "clickstream_data.csv")
OUT_IMG = os.path.join(OUT_DIR, "clicks_by_user.png")

def ensure_out():
    os.makedirs(OUT_DIR, exist_ok=True)

def generate_with_pyspark():
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import to_timestamp, sum as spark_sum, col
    spark = SparkSession.builder.appName("ClickstreamCharts").getOrCreate()
    df = spark.read.csv(CSV_PATH, header=True, inferSchema=True)
    if 'Timestamp' in df.columns:
        df = df.withColumn("Timestamp", to_timestamp(col("Timestamp")))
    total = df.groupBy("User_ID").agg(spark_sum("Clicks").alias("total_clicks")).orderBy(col("total_clicks").desc())
    pdf = total.toPandas().set_index("User_ID")
    spark.stop()
    return pdf

def generate_with_pandas():
    df = pd.read_csv(CSV_PATH, parse_dates=['Timestamp'], infer_datetime_format=True)
    total = df.groupby('User_ID')['Clicks'].sum().sort_values(ascending=False)
    pdf = total.head(100).to_frame('total_clicks')
    return pdf

def plot(pdf):
    plt.figure(figsize=(12,6))
    pdf['total_clicks'].head(20).plot.bar(color="#667eea")
    plt.title("Top 20 usuarios por total de clicks")
    plt.ylabel("Total Clicks")
    plt.tight_layout()
    plt.savefig(OUT_IMG, dpi=150)
    plt.close()
    print("Gráfica guardada en:", OUT_IMG)

def save_clicks_plot(df, out_path):
    try:
        # Asegura carpeta destino (maneja el caso donde 'assets/images' es un archivo)
        out_dir = os.path.dirname(out_path)
        if os.path.exists(out_dir):
            if not os.path.isdir(out_dir):
                # Respaldar el archivo conflictivo y crear la carpeta
                backup = out_dir + '.filebak'
                print(f"[WARN] '{out_dir}' existe y no es un directorio. Renombrando a '{backup}'")
                os.replace(out_dir, backup)
                os.makedirs(out_dir, exist_ok=True)
        else:
            os.makedirs(out_dir, exist_ok=True)

        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        if 'Clicks' in df.columns:
            df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce').fillna(0)
        else:
            print("ERROR: columna 'Clicks' no encontrada en CSV", file=sys.stderr)

        agg = df.groupby('User_ID')['Clicks'].sum().sort_values(ascending=False)
        top = agg.head(10)
        plt.figure(figsize=(10,6))
        top.plot(kind='bar', color='#2b7bba')
        plt.title('Top 10 usuarios por clics')
        plt.xlabel('User_ID')
        plt.ylabel('Total Clicks')
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close()
        print(f"[OK] Imagen guardada en: {os.path.abspath(out_path)}")
    except Exception as e:
        print("ERROR al generar la imagen:", e, file=sys.stderr)
        raise

def main():
    ensure_out()
    try:
        pdf = generate_with_pyspark()
    except Exception as e:
        print("pyspark falló o no instalado, intentando pandas:", e)
        try:
            pdf = generate_with_pandas()
        except Exception as e2:
            print("Error con pandas:", e2)
            sys.exit(1)
    plot(pdf)

if __name__ == "__main__":
    try:
        base = os.path.dirname(__file__) or '.'
        csv_path = os.path.join(base, 'assets','data','clickstream_data.csv')
        out_image = os.path.join(base, 'assets','images','clicks_by_user.png')
        print("Leyendo CSV desde:", os.path.abspath(csv_path))
        if not os.path.exists(csv_path):
            print("ERROR: CSV no existe en la ruta indicada.", file=sys.stderr)
            sys.exit(1)
        df = pd.read_csv(csv_path)
        print("Columnas detectadas:", list(df.columns))
        print("Primeras filas:\n", df.head().to_string(index=False))
        save_clicks_plot(df, out_image)
    except Exception as e:
        print("ERROR general:", e, file=sys.stderr)
        sys.exit(1)

# Cargar datos
data_path = 'assets/data/clickstream_data.csv'
df = pd.read_csv(data_path)

# Asegurarse de que la columna Timestamp sea de tipo datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Análisis por ventanas de 1 minuto
df.set_index('Timestamp', inplace=True)
windowed_clicks = df.resample('1T').sum()

# Top usuarios
top_users = df.groupby('User_ID').agg(
    sesiones=('Clicks', 'count'),
    total_clicks=('Clicks', 'sum')
).sort_values(by='total_clicks', ascending=False).head(15)

# Graficar Top usuarios
plt.figure(figsize=(10, 6))
top_users['total_clicks'].plot(kind='bar', color='#667eea')
plt.title('Top 15 usuarios por total de clicks')
plt.xlabel('User ID')
plt.ylabel('Total Clicks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/images/top_users_chart.png', dpi=150)
plt.close()

# Graficar análisis temporal
plt.figure(figsize=(10, 6))
windowed_clicks['Clicks'].plot(color='#764ba2')
plt.title('Análisis Temporal de Clicks')
plt.xlabel('Tiempo')
plt.ylabel('Total Clicks por Minuto')
plt.tight_layout()
plt.savefig('assets/images/temporal_analysis.png', dpi=150)
plt.close()

# Graficar relación clicks vs sesiones
plt.figure(figsize=(10, 6))
plt.scatter(top_users['sesiones'], top_users['total_clicks'], color='#28a745')
plt.title('Relación entre Clicks y Sesiones')
plt.xlabel('Número de Sesiones')
plt.ylabel('Total Clicks')
plt.tight_layout()
plt.savefig('assets/images/clicks_vs_sessions.png', dpi=150)
plt.close()

# Graficar distribución de usuarios
plt.figure(figsize=(10, 6))
top_users['sesiones'].plot(kind='hist', bins=10, color='#dc3545', alpha=0.7)
plt.title('Distribución de Usuarios por Sesiones')
plt.xlabel('Número de Sesiones')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('assets/images/user_distribution.png', dpi=150)
plt.close()

# Graficar mapa de calor de actividad
activity_heatmap = df.pivot_table(index=df.index.date, columns='User_ID', values='Clicks', aggfunc='sum', fill_value=0)
plt.figure(figsize=(12, 6))
plt.imshow(activity_heatmap, aspect='auto', cmap='hot', interpolation='nearest')
plt.title('Mapa de Calor de Actividad de Usuarios')
plt.xlabel('User ID')
plt.ylabel('Fecha')
plt.colorbar(label='Total Clicks')
plt.tight_layout()
plt.savefig('assets/images/activity_heatmap.png', dpi=150)
plt.close()