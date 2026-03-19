# RecoveriStudio — Automatización Post-Compra
## Versión 1.0 | 18 de Marzo de 2026 | Sesión 11
## Estado: BORRADOR – Revisión del Jefe
## Propósito: Mensaje proactivo para eliminar los tickets de la Bandeja A y B antes de que ocurran

---

## ¿Qué es Esto?

Un mensaje proactivo enviado a cada comprador después de la compra. Etsy permite a los vendedores enviar un mensaje automático por cada pedido. Este mensaje:

1.  Agradece al cliente
2.  Les proporciona instrucciones de descarga (evita los tickets de la Bandeja A)
3.  Explica lo que han comprado y cómo usarlo (evita los tickets de la Bandeja B)
4.  Ofrece un canal de soporte (captura cualquier otra cosa al principio)
5.  Siembra la idea de una interacción futura (lista de correo electrónico, compra repetida)

---

## Plantilla de Mensaje Post-Compra

### Configurar en: Etsy > Administrador de Tienda > Ajustes > Información y Apariencia > Mensaje a Compradores

```
¡Gracias por su compra en RecoveriStudio!

¡TUS ARCHIVOS ESTÁN LISTOS PARA DESCARGARSE

1.  Compruebe su correo electrónico para obtener un enlace de descarga de Etsy
2.  O vaya a: Su Cuenta > Compras > encuentre este pedido > haga clic en "Descargar Archivos"
3.  Los enlaces de descarga son válidos por 30 días

Si ha pagado con PayPal, podría tardar unos minutos más – compruebe su carpeta de spam si es necesario.

¿QUÉ INCLUYE?

Su descarga contiene: [esto mostrará automáticamente la descripción de la lista de productos]

Si los archivos están en una carpeta ZIP:
- Windows: haga clic derecho > "Extraer todo"
- Mac: haga doble clic para extraer automáticamente

¿NECESITA AYUDA?

Responda a este mensaje y le responderemos en un plazo de 2 horas. Estamos aquí para los problemas de descarga, preguntas de compatibilidad o cualquier otra cosa.

¡Disfrute de sus nuevas herramientas!
— El Equipo de RecoveriStudio
```

---

## Notas de Configuración de Etsy

*   El "Mensaje a Compradores" de Etsy se envía automáticamente con cada confirmación de pedido.
*   Es el MISMO mensaje para todos los productos (no puede personalizarse por lista de productos)
*   Manténgalo lo suficientemente genérico para que funcione con cualquier tipo de producto.
*   Longitud máxima: 2.000 caracteres (la plantilla anterior es de aproximadamente 850)
*   El mensaje aparece en la bandeja de entrada de Etsy Messages del comprador.

---

## Mejoras Futuras (no ahora – después de los primeros datos de ventas)

### Fase 2 – Captura de Lista de Correo Electrónico (cuando esté activa recoveri.io)

Agregue al mensaje post-compra:

```
ASISTENCIA EXCLUSIVA

Únete a nuestra lista de correo electrónico para obtener un 20% de descuento en su próxima compra:
recoveri.io/exclusivo

También recibirás acceso anticipado a nuevos productos y recursos gratuitos.
```

Esto cumple con las reglas de Etsy: no estás enviando mensajes a ellos, solo los invitas a suscribirse voluntariamente a través de tu propio sitio web.

### Fase 3 – Descarga PDF de Seguimiento

Incluya un PDF de una página en cada archivo ZIP que contenga:

*   Instrucciones de descarga/configuración con capturas de pantalla
*   Preguntas frecuentes para este tipo de producto
*   Enlace a recoveri.io para recursos
*   Información de contacto de soporte

Este PDF actúa como una capa de prevención "en el producto" – el cliente lo ve incluso si omite el mensaje de Etsy.

---

## Impacto Preventivo

| Bandeja | Cómo Esto Evita los Tickets |
|---|---|
| A – Descarga y Acceso | Los pasos 1-3 cubren la descarga, la extracción de ZIP, la demora de PayPal |
| B – Comprensión del Producto | La sección "Qué incluye" + la descripción del archivo |
| A + B combinadas | "¿Necesita ayuda?" captura cualquier cosa que los instrucciones hayan perdido, ANTES de que el cliente se frustre |

Objetivo: reducir los tickets de la Bandeja A en un 40-50% en el primer mes.

---

*Automatización Post-Compra v1 | Sesión 11 | 18 de Marzo de 2026*
*Alineado a: Marco CS Framework v2 Control de Prevención, Habilidad 132, Estrategia de Marca v1 (fase 2 de captura de correo electrónico)*