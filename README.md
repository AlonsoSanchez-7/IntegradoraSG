# Point-of-Sale System for Carnicería SG

A desktop point-of-sale system made for a real local butcher shop in Durango, Mexico.

## The problem
The shop used a generic store system that did not fit the way it sells. It needed software made for its own process.

## The solution
A team of five students developed a system with four modules:
- **Sales** – register each sale.
- **Product management** – add and update products.
- **Daily cash register closing** – close the cash register at the end of the day.
- **Stock control** – keep track of the products in stock.

## Technologies
Python, graphical interface, MySQL.

## Files
| File | Purpose |
| --- | --- |
| `main.py` | Starts the program |
| `conexionBD.py` | Connects Python to the MySQL database |
| `producto.py` | Product logic |
| `cliente.py` | Customer logic |
| `usuario.py` | User logic |
| `venta.py` | Sales logic |
| `bd_carniceriasg.sql` | Database structure |

## How to run
1. Install Python and MySQL.
2. Import `bd_carniceriasg.sql` into MySQL.
3. Check the connection data in `conexionBD.py`.
4. Run `python main.py`.

## My role
Co-developer. I wrote Python code and helped connect the program to the database.

## Team
Team project, 5 members. Universidad Tecnológica de Durango.
