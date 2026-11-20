IF DB_ID('SISTEMA_RECURSOS_HIDRICOS') IS NULL
    CREATE DATABASE [SISTEMA_RECURSOS_HIDRICOS]
GO

USE [SISTEMA_RECURSOS_HIDRICOS]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Alertas](
	[id_alertas] [int] IDENTITY(1,1) NOT NULL,
	[id_modulo] [varchar](30) NOT NULL,
	[tipo_alerta] [varchar](100) NULL,
	[fecha_hora] [datetime] NOT NULL,
	[resuelta] [bit] NULL,
PRIMARY KEY CLUSTERED
(
	[id_alertas] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Consumo](
	[id_consumo] [int] IDENTITY(1,1) NOT NULL,
	[id_reservorio] [int] NOT NULL,
	[hora_fecha] [datetime] NOT NULL,
	[caudal_salida] [decimal](10, 2) NULL,
PRIMARY KEY CLUSTERED
(
	[id_consumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Historia_Bombeo](
	[id_historial] [int] IDENTITY(1,1) NOT NULL,
	[id_bomba] [int] NOT NULL,
	[fecha_hora_encendido] [datetime] NOT NULL,
	[fecha_hora_apagado] [datetime] NULL,
	[volumen_inyectado_estimado] [decimal](10, 2) NULL,
PRIMARY KEY CLUSTERED
(
	[id_historial] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Lecturas](
	[id_lectura] [bigint] IDENTITY(1,1) NOT NULL,
	[id_modulo] [varchar](30) NOT NULL,
	[fecha_hora] [datetime] NOT NULL,
	[nivel_agua] [decimal](10, 2) NULL,
	[calidad_senal] [int] NULL,
PRIMARY KEY CLUSTERED
(
	[id_lectura] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Mantenimiento](
	[id_mantenimiento] [int] IDENTITY(1,1) NOT NULL,
	[id_bomba] [int] NOT NULL,
	[costo] [decimal](10, 2) NULL,
	[descripcion] [text] NULL,
	[fecha_intervencion] [date] NULL,
PRIMARY KEY CLUSTERED
(
	[id_mantenimiento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Modulo](
	[id_modulo] [varchar](30) NOT NULL,
	[id_reservorio] [int] NOT NULL,
	[id_tipo_modulo] [int] NOT NULL,
	[nombre_modulo] [varchar](100) NOT NULL,
	[altura_instalacion] [decimal](10, 2) NULL,
	[estado] [bit] NOT NULL,
	[fecha_estado] [datetime] NULL,
PRIMARY KEY CLUSTERED
(
	[id_modulo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Reservorio](
	[id_reservorio] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](100) NOT NULL,
	[capacidad_maxima] [decimal](10, 2) NOT NULL,
	[ubicacion] [varchar](150) NULL,
	[fecha_construccion] [date] NULL,
PRIMARY KEY CLUSTERED
(
	[id_reservorio] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sistema_Bombeo](
	[id_bomba] [int] IDENTITY(1,1) NOT NULL,
	[id_reservorio] [int] NOT NULL,
	[nombre] [varchar](100) NOT NULL,
	[modelo] [varchar](100) NOT NULL,
	[caudal_L_s] [decimal](10, 2) NULL,
	[consumo_kw] [decimal](10, 2) NULL,
	[estado] [bit] NOT NULL,
	[horas_iniciales] [decimal](10, 2) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[id_bomba] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tipo_Modulo](
	[id_tipo_modulo] [int] IDENTITY(1,1) NOT NULL,
	[nombre_modulo] [varchar](100) NOT NULL,
	[margen_error_cm] [decimal](5, 2) NULL,
	[frecuencia_lectura_segundos] [int] NOT NULL,
PRIMARY KEY CLUSTERED
(
	[id_tipo_modulo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tipo_Usuario](
	[id_tipo_usuario] [int] IDENTITY(1,1) NOT NULL,
	[nombre_tipo] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[id_tipo_usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[nombre_tipo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios](
	[id_usuario] [int] IDENTITY(1,1) NOT NULL,
	[id_tipo_usuario] [int] NOT NULL,
	[usuario] [varchar](50) NOT NULL,
	[contrasena] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[id_usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Alertas] ADD  DEFAULT ((0)) FOR [resuelta]
GO
ALTER TABLE [dbo].[Sistema_Bombeo] ADD  DEFAULT ((0)) FOR [horas_iniciales]
GO
ALTER TABLE [dbo].[Alertas]  WITH CHECK ADD  CONSTRAINT [FK_Alertas_Modulo] FOREIGN KEY([id_modulo])
REFERENCES [dbo].[Modulo] ([id_modulo])
GO
ALTER TABLE [dbo].[Alertas] CHECK CONSTRAINT [FK_Alertas_Modulo]
GO
ALTER TABLE [dbo].[Consumo]  WITH CHECK ADD  CONSTRAINT [FK_Consumo_Reservorio] FOREIGN KEY([id_reservorio])
REFERENCES [dbo].[Reservorio] ([id_reservorio])
GO
ALTER TABLE [dbo].[Consumo] CHECK CONSTRAINT [FK_Consumo_Reservorio]
GO
ALTER TABLE [dbo].[Historia_Bombeo]  WITH CHECK ADD  CONSTRAINT [FK_HistoriaBombeo_Sistema] FOREIGN KEY([id_bomba])
REFERENCES [dbo].[Sistema_Bombeo] ([id_bomba])
GO
ALTER TABLE [dbo].[Historia_Bombeo] CHECK CONSTRAINT [FK_HistoriaBombeo_Sistema]
GO
ALTER TABLE [dbo].[Lecturas]  WITH CHECK ADD  CONSTRAINT [FK_Lecturas_Modulo] FOREIGN KEY([id_modulo])
REFERENCES [dbo].[Modulo] ([id_modulo])
GO
ALTER TABLE [dbo].[Lecturas] CHECK CONSTRAINT [FK_Lecturas_Modulo]
GO
ALTER TABLE [dbo].[Mantenimiento]  WITH CHECK ADD  CONSTRAINT [FK_Mantenimiento_Sistema] FOREIGN KEY([id_bomba])
REFERENCES [dbo].[Sistema_Bombeo] ([id_bomba])
GO
ALTER TABLE [dbo].[Mantenimiento] CHECK CONSTRAINT [FK_Mantenimiento_Sistema]
GO
ALTER TABLE [dbo].[Modulo]  WITH CHECK ADD  CONSTRAINT [FK_Modulo_Reservorio] FOREIGN KEY([id_reservorio])
REFERENCES [dbo].[Reservorio] ([id_reservorio])
GO
ALTER TABLE [dbo].[Modulo] CHECK CONSTRAINT [FK_Modulo_Reservorio]
GO
ALTER TABLE [dbo].[Modulo]  WITH CHECK ADD  CONSTRAINT [FK_Modulo_Tipo] FOREIGN KEY([id_tipo_modulo])
REFERENCES [dbo].[Tipo_Modulo] ([id_tipo_modulo])
GO
ALTER TABLE [dbo].[Modulo] CHECK CONSTRAINT [FK_Modulo_Tipo]
GO
ALTER TABLE [dbo].[Sistema_Bombeo]  WITH CHECK ADD  CONSTRAINT [FK_Bombeo_Reservorio] FOREIGN KEY([id_reservorio])
REFERENCES [dbo].[Reservorio] ([id_reservorio])
GO
ALTER TABLE [dbo].[Sistema_Bombeo] CHECK CONSTRAINT [FK_Bombeo_Reservorio]
GO
ALTER TABLE [dbo].[Usuarios]  WITH CHECK ADD  CONSTRAINT [FK_Usuarios_TipoUsuario] FOREIGN KEY([id_tipo_usuario])
REFERENCES [dbo].[Tipo_Usuario] ([id_tipo_usuario])
GO
ALTER TABLE [dbo].[Usuarios] CHECK CONSTRAINT [FK_Usuarios_TipoUsuario]
GO
