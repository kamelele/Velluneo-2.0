# Fictional two-board contract review

This is original, non-confidential demonstration data, not a real human approval,
measurement, simulation, manufacturing qualification or product design recommendation.

POWER supplies 4.8–5.2 V with a declared 500 mA budget. LED accepts 4.5–5.5 V and
declares a 300 mA load. Cable pin 1 connects power and pin 2 connects ground.
The MCU on POWER and LED firmware agree UART, 115200 baud, 8N1. Their startup
behavior keeps the LED output off until a valid command; loss of commands turns it off.
CASE allocates a 40 by 20 mm board outline, mounting points, connector position,
8 mm component height and 0.2 mm geometric tolerance for this fictional product.
All numbers are local example decisions. None are portfolio-wide limits.

The recorded evidence is only a demonstration of a document review. Real projects
must replace it with actual approved requirements, calculations and measurements.
