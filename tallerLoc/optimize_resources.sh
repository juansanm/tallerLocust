MIN_CPU=0.1
MAX_CPU=1.0
MIN_MEM=128
MAX_MEM=1024
STEP_CPU=0.1
STEP_MEM=64
TARGET_USERS=10000
SPAWN_RATE=500
update_compose() {
    local cpu=$1
    local mem=$2
    local replicas=$3
    
    cat > docker-compose.locust.yaml << EOF
version: '3.8'
services:
  api:
    image: juanfelipe/ml-inference-api:latest
    deploy:
      resources:
        limits:
          cpus: '${cpu}'
          memory: ${mem}M
      replicas: ${replicas}
    networks:
      - locust-network
    restart: unless-stopped
  locust-master:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --master -H http://api:8000
    networks:
      - locust-network
    depends_on:
      - api
  locust-worker:
    image: locustio/locust
    volumes:
      - ./locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --worker --master-host locust-master
    networks:
      - locust-network
    depends_on:
      - locust-master
    deploy:
      replicas: 3

networks:
  locust-network:
    driver: bridge
EOF
}
for cpu in $(seq $MIN_CPU $STEP_CPU $MAX_CPU); do
    for mem in $(seq $MIN_MEM $STEP_MEM $MAX_MEM); do
        echo "Probando con CPU: $cpu, Memoria: ${mem}M"
        update_compose $cpu $mem 1  
        # Reiniciar servicios
        docker-compose -f docker-compose.locust.yaml down
        docker-compose -f docker-compose.locust.yaml up -d
        sleep 100
        echo "Ejecutando prueba con $TARGET_USERS usuarios a $SPAWN_RATE usuarios/segundo"     
        read -p "¿La prueba fue exitosa? (s/n): " result
        if [ "$result" = "s" ]; then
            echo "Configuración encontrada: CPU=$cpu, MEM=${mem}M"
            exit 0
        fi
    done
done
echo "No se encontró una configuración"