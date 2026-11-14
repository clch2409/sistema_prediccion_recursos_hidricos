/* =====================================================================
   MIGRACIÓN para una base YA CREADA: id_modulo pasa de INT a VARCHAR(30)

   Los ids antiguos (1, 2, 3...) se convierten así:
     - si el módulo tenía codigo_dispositivo  -> ese código pasa a ser su id_modulo
     - si no tenía                            -> queda como 'MOD-1', 'MOD-2'...
   Lo ideal es que ANTES de ejecutar esto llenes Modulo.codigo_dispositivo con los códigos reales
   (EMI-... / REC-...): así tus módulos quedan con su código como id. Esa columna se elimina al final.
   Si ya hay lecturas guardadas con ids 'MOD-n', es más simple borrar las lecturas de prueba.

   Haz una copia de seguridad antes de ejecutar.
   ===================================================================== */
USE [SISTEMA_RECURSOS_HIDRICOS];
GO

BEGIN TRANSACTION;

-- 1) Quitar las llaves foráneas que apuntan a Modulo
ALTER TABLE Alertas  DROP CONSTRAINT FK_Alertas_Modulo;
ALTER TABLE Lecturas DROP CONSTRAINT FK_Lecturas_Modulo;

-- 2) Pasar a texto las columnas id_modulo de Alertas y Lecturas (1 -> '1')
ALTER TABLE Alertas  ALTER COLUMN id_modulo VARCHAR(30) NOT NULL;
ALTER TABLE Lecturas ALTER COLUMN id_modulo VARCHAR(30) NOT NULL;

-- 3) Reemplazar esos ids por el nuevo valor (codigo_dispositivo o 'MOD-n')
UPDATE a SET a.id_modulo = ISNULL(m.codigo_dispositivo, 'MOD-' + CAST(m.id_modulo AS VARCHAR(10)))
FROM Alertas a INNER JOIN Modulo m ON CAST(m.id_modulo AS VARCHAR(30)) = a.id_modulo;

UPDATE l SET l.id_modulo = ISNULL(m.codigo_dispositivo, 'MOD-' + CAST(m.id_modulo AS VARCHAR(10)))
FROM Lecturas l INNER JOIN Modulo m ON CAST(m.id_modulo AS VARCHAR(30)) = l.id_modulo;

-- 4) Crear la tabla Modulo nueva (id_modulo de texto, sin IDENTITY) y copiar los datos
CREATE TABLE Modulo_nuevo (
    id_modulo          VARCHAR(30)   NOT NULL PRIMARY KEY,
    id_reservorio      INT           NOT NULL,
    id_tipo_modulo     INT           NOT NULL,
    nombre_modulo      VARCHAR(100)  NOT NULL,
    altura_instalacion DECIMAL(10,2) NULL,
    estado             BIT           NOT NULL,
    fecha_estado       DATETIME      NULL
);

INSERT INTO Modulo_nuevo (id_modulo, id_reservorio, id_tipo_modulo, nombre_modulo,
                          altura_instalacion, estado, fecha_estado)
SELECT ISNULL(codigo_dispositivo, 'MOD-' + CAST(id_modulo AS VARCHAR(10))),
       id_reservorio, id_tipo_modulo, nombre_modulo, altura_instalacion, estado, fecha_estado
FROM Modulo;

DROP TABLE Modulo;
EXEC sp_rename 'Modulo_nuevo', 'Modulo';

-- 5) Volver a crear las llaves foráneas
ALTER TABLE Modulo   ADD CONSTRAINT FK_Modulo_Reservorio FOREIGN KEY (id_reservorio)  REFERENCES Reservorio(id_reservorio);
ALTER TABLE Modulo   ADD CONSTRAINT FK_Modulo_Tipo       FOREIGN KEY (id_tipo_modulo) REFERENCES Tipo_Modulo(id_tipo_modulo);
ALTER TABLE Alertas  ADD CONSTRAINT FK_Alertas_Modulo    FOREIGN KEY (id_modulo)      REFERENCES Modulo(id_modulo);
ALTER TABLE Lecturas ADD CONSTRAINT FK_Lecturas_Modulo   FOREIGN KEY (id_modulo)      REFERENCES Modulo(id_modulo);

COMMIT TRANSACTION;
GO

-- Verificación
SELECT id_modulo, id_reservorio, nombre_modulo, estado FROM Modulo;
