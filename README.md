# Mesa de partes digital - Los Olivos

Prototipo en Python de una mesa de partes digital, desarrollado para el desafío "Del archivador al algoritmo" del curso Fundamentos de Programación (CIIN1205P, UPN).

## Funcionalidades

- Registrar solicitudes** con validación de DNI (8 dígitos), nombre del solicitante y asunto obligatorio.
- Generación de correlativo municipal** en formato institucional (`MDLO-2026-0001`).
- Asignación automática de fecha y hora** de registro en el sistema.
- Derivación por área municipal** (Rentas, Obras Públicas, Licencias, Desarrollo Urbano, Seguridad Ciudadana).
- Control y actualización de estados del trámite** (REGISTRADO, EN PROCESO, ATENDIDO, RECHAZADO).
- Detección preventiva de trámites duplicados** según DNI y asunto.
- Buscar expedientes** por código correlativo o DNI.
- Listar expedientes** ordenados por código, DNI o solicitante.
- Persistencia de datos** mediante lectura y guardado en archivo de texto (`expedientes.txt`).

## Cómo ejecutar

Requisito: Python 3.

    python main.py

## Nota
Los datos de prueba deben ser ficticios. El archivo expedientes.txt no se sube al repositorio.
