# Proyecto Arquitectura de Software - Consultorio

## Descripción

Este repositorio pertenece al sistema **Consultorio**, el cual utiliza la arquitectura **SOA** (Arquitectura Orientada a Servicios) como fue explicado en clases. El sistema consta de diversos **servicios** y **clientes**, que interactúan a través de mensajes en el bus de servicio, permitiendo la comunicación entre los componentes del sistema.

Los archivos del repositorio incluyen los **servicios** correspondientes (como autenticación, registro de usuarios, etc.) y los **clientes** necesarios para interactuar con estos servicios.

---

## Instrucciones para levantar el sistema

### 1. Levantar el sistema con Docker Compose

Para ejecutar el sistema, primero necesitas levantar los **contenedores de Docker** que contienen la base de datos y el bus de servicio. Para ello, debes ejecutar el siguiente comando en la raíz del proyecto:

```bash
docker-compose up -d
```

### 2. Crear las tablas en la base de datos (si es la primera vez que usas el sistema)
Si es la primera vez que usas el sistema, necesitarás crear las tablas en la base de datos desde la raiz del proyecto. Para hacerlo, ejecuta el siguiente comando en la terminal:

```bash
python3 crear_tablas.py
```

### 3. Levantar los servicios
Para levantar todos los servicios del sistemas manera simultanea, en la raiz del proyecto debes ejecutar el siguiente comando por terminal:

```bash
python3 run_servicios.py
```

### 4. Detener el sistema
Cuando termines de trabajar con el sistema, puedes detenerlo de manera segura con el siguiente comando:
```bash
docker-compose down
```
