-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-04-2026 a las 20:13:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `organizeit`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_tarea` int(11) NOT NULL,
  `nombre_tarea` varchar(255) NOT NULL,
  `categoria` enum('trabajo','hogar','personal') NOT NULL,
  `prioridad` enum('alta','media','baja') NOT NULL,
  `fecha_limite` date DEFAULT NULL,
  `usuario_email` varchar(100) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `completada` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_tarea`, `nombre_tarea`, `categoria`, `prioridad`, `fecha_limite`, `usuario_email`, `fecha_creacion`, `completada`) VALUES
(1, 'Terminar proyecto de programación web', 'trabajo', 'alta', '2024-12-15', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(2, 'Estudiar para examen de bases de datos', 'trabajo', 'alta', '2024-12-18', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(3, 'Preparar presentación del proyecto final', 'trabajo', 'media', '2024-12-20', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(4, 'Revisar documentación de Flask', 'trabajo', 'baja', '2024-12-25', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(5, 'Limpiar la cocina', 'hogar', 'media', '2024-12-10', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(6, 'Comprar víveres para la semana', 'hogar', 'alta', '2024-12-09', 'demo@organizeit.com', '2026-04-26 18:13:00', 1),
(7, 'Lavar la ropa', 'hogar', 'baja', '2024-12-12', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(8, 'Organizar el armario', 'hogar', 'baja', '2024-12-30', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(9, 'Ir al gimnasio', 'personal', 'media', '2024-12-11', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(10, 'Leer libro de desarrollo personal', 'personal', 'baja', '2024-12-28', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(11, 'Meditar 30 minutos', 'personal', 'alta', '2024-12-08', 'demo@organizeit.com', '2026-04-26 18:13:00', 1),
(12, 'Aprender una receta nueva', 'personal', 'media', '2024-12-22', 'demo@organizeit.com', '2026-04-26 18:13:00', 0),
(13, 'Revisar logs del sistema', 'trabajo', 'alta', '2024-12-10', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(14, 'Actualizar software del servidor', 'trabajo', 'alta', '2024-12-15', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(15, 'Crear copias de seguridad', 'trabajo', 'media', '2024-12-12', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(16, 'Documentar procesos internos', 'trabajo', 'baja', '2024-12-30', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(17, 'Pagar facturas del hogar', 'hogar', 'alta', '2024-12-09', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(18, 'Hacer mantenimiento al auto', 'personal', 'media', '2024-12-20', 'admin@organizeit.com', '2026-04-26 18:13:00', 0),
(19, 'Revisar informes mensuales', 'trabajo', 'alta', '2024-12-20', 'maria@email.com', '2026-04-26 18:13:00', 0),
(20, 'Preparar reunión con clientes', 'trabajo', 'alta', '2024-12-14', 'maria@email.com', '2026-04-26 18:13:00', 0),
(21, 'Actualizar hoja de cálculo de gastos', 'trabajo', 'media', '2024-12-18', 'maria@email.com', '2026-04-26 18:13:00', 0),
(22, 'Organizar el armario', 'hogar', 'baja', '2024-12-30', 'maria@email.com', '2026-04-26 18:13:00', 0),
(23, 'Preparar cena navideña', 'hogar', 'alta', '2024-12-24', 'maria@email.com', '2026-04-26 18:13:00', 0),
(24, 'Decorar la casa', 'hogar', 'media', '2024-12-15', 'maria@email.com', '2026-04-26 18:13:00', 0),
(25, 'Yoga matutino', 'personal', 'alta', '2024-12-10', 'maria@email.com', '2026-04-26 18:13:00', 0),
(26, 'Correr 5 kilómetros', 'personal', 'alta', '2024-12-10', 'juan@email.com', '2026-04-26 18:13:00', 1),
(27, 'Preparar maratón', 'personal', 'media', '2024-12-31', 'juan@email.com', '2026-04-26 18:13:00', 0),
(28, 'Leer 3 capítulos del libro', 'personal', 'baja', '2024-12-20', 'juan@email.com', '2026-04-26 18:13:00', 0),
(29, 'Reparar la lavadora', 'hogar', 'alta', '2024-12-12', 'juan@email.com', '2026-04-26 18:13:00', 0),
(30, 'Pintar la sala', 'hogar', 'media', '2024-12-28', 'juan@email.com', '2026-04-26 18:13:00', 0),
(31, 'Entregar reporte trimestral', 'trabajo', 'alta', '2024-12-15', 'juan@email.com', '2026-04-26 18:13:00', 0),
(32, 'Capacitación del personal nuevo', 'trabajo', 'media', '2024-12-22', 'juan@email.com', '2026-04-26 18:13:00', 0),
(33, 'Terminar diseño gráfico', 'trabajo', 'alta', '2024-12-14', 'ana@email.com', '2026-04-26 18:13:00', 0),
(34, 'Reunión con el equipo de marketing', 'trabajo', 'media', '2024-12-16', 'ana@email.com', '2026-04-26 18:13:00', 0),
(35, 'Enviar propuesta al cliente', 'trabajo', 'alta', '2024-12-11', 'ana@email.com', '2026-04-26 18:13:00', 1),
(36, 'Comprar regalos de navidad', 'personal', 'alta', '2024-12-20', 'ana@email.com', '2026-04-26 18:13:00', 0),
(37, 'Llamar a la familia', 'personal', 'media', '2024-12-24', 'ana@email.com', '2026-04-26 18:13:00', 0),
(38, 'Limpiar el jardín', 'hogar', 'baja', '2024-12-28', 'ana@email.com', '2026-04-26 18:13:00', 0),
(39, 'Cocinar galletas', 'hogar', 'media', '2024-12-22', 'ana@email.com', '2026-04-26 18:13:00', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usuario`, `email`, `contraseña`, `fecha_registro`) VALUES
(1, 'Usuario Demo', 'demo@organizeit.com', 'd3ad9315b7be5dd53b31a273b3b3aba5defe700808305aa16a3062b76658a791', '2026-04-26 18:12:59'),
(2, 'Administrador', 'admin@organizeit.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', '2026-04-26 18:12:59'),
(3, 'María García', 'maria@email.com', '626e3c805e77eeb472c42c6be607be2af7ac5c08fd7050f278e0330fe81abf57', '2026-04-26 18:12:59'),
(4, 'Juan Pérez', 'juan@email.com', 'f6ccb3e8d609012238c0b39e60b2c9632b3cdede91e035dad1de43469768f4cc', '2026-04-26 18:12:59'),
(5, 'Ana López', 'ana@email.com', 'e82827b00b2ca8620beb37f879778c082b292a52270390cff35b6fe3157f4e8b', '2026-04-26 18:13:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `idx_usuario_email` (`usuario_email`),
  ADD KEY `idx_categoria` (`categoria`),
  ADD KEY `idx_prioridad` (`prioridad`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`usuario_email`) REFERENCES `usuarios` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
