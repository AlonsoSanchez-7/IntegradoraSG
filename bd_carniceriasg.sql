CREATE DATABASE IF NOT EXISTS bd_carniceriasg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bd_carniceriasg;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'empleado'
);

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio_kg DOUBLE NOT NULL,
    stock_kg DOUBLE NOT NULL,
    stock_minimo DOUBLE NOT NULL DEFAULT 5.0,
    fecha_caducidad DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    total DOUBLE NOT NULL,
    id_cliente INT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_kg DOUBLE NOT NULL,
    precio_kg DOUBLE NOT NULL,
    subtotal DOUBLE NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE
);

-- Usuario administrador por defecto
INSERT INTO usuario (nombre, usuario, contrasena, rol) 
VALUES ('Don Roberto (Dueño)', 'admin', '1234', 'admin');

-- Productos de prueba iniciales
INSERT INTO producto (nombre, descripcion, precio_kg, stock_kg, stock_minimo, fecha_caducidad) VALUES
('Bistec de Res', 'Corte fresco pulpa negra', 180.00, 35.0, 10.0, DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
('Chuleta de Cerdo', 'Chuleta ahumada con hueso', 115.00, 8.0, 10.0, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Carne Molida 80/20', 'Molida especial de res', 145.00, 20.0, 5.0, DATE_ADD(CURDATE(), INTERVAL 4 DAY));
