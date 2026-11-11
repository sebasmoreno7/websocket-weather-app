# frontend

## Desarrollo y verificación

Requiere Node >=22.12.0. La compilación usa Vite y las pruebas Vitest.

```bash
npm ci --ignore-scripts
npm start
npm test
npm run build
npm audit
```

El resultado de producción se conserva en `build/`. Las rutas de la aplicación
y los recursos de `public/` se mantienen. Las variables públicas existentes
`REACT_APP_*` siguen disponibles; nunca uses ese prefijo para secretos.

La migración retira Create React App y su cadena de compilación sin mantenimiento.
Las pruebas existentes comprueban el comportamiento de la aplicación.
