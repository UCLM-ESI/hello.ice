Descripción
===========

Este ejemplo describe una aplicación distribuida con IceGrid que despliega dos servidores Printer en dos nodos (node1 y node2). La aplicación incluye la definición de un objeto "bien conocido" llamado "printer1" para el objeto Printer del servidor desplegado en node1.

Crea tres nodos IceGrid en el computador de usuario, aunque solo se utilizan los dos primeros.

Aquí se indica el uso y significado de los distintos ficheros:

- `Makefile`: Tiene objetivos para arrancar y parar los tres nodos.
- `node1.config`: Configuración del primer nodo IceGrid. Incluye un Registry "colocalizado", es decir, que ambos se ejecutan en el mismo proceso.
- `node2.config`: Configuración del segundo nodo iceGrid.
- `node3.config`: Configuración del tercer nodo iceGrid.
- `locator.config`: Configuración de la referencia del Locator, necesaria para los clientes que accedan a los objetos desplegados.
- `default-templates.xml`: Las plantillas de servicios para la creación de aplicaciones desde el Registry.
- `printerapp-cpp.xml`: Aplicación distribuida que usa el Printer implementado en C++ (directorio hello.ice/cpp).
- `printerapp-java.xml`: Aplicación distribuida que usa el Printer implementado en Java (directorio hello.ice/java).
- `printerapp-py.xml`: Aplicación distribuida que usa el Printer implementado en Python (directorio hello.ice/py).
- `well-known.py`: Un cliente Python que invoca el objeto bien conocido "printer1".
- `query-client.py`: Ejemplo de uso de la interfaz IceGrid::Query para la búsqueda de objetos.


Ejecución
=========

Estas instrucciones utilizan el programa icegridadmin, pero todos estos pasos se pueden realizar también con icegridgui.

Arrancar los nodos:

    $ make start-grid

Cargar la aplicación en el Registry:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add printerapp-py.xml"

Distribución de los ficheros. La aplicación busca los programas a ejecutar en ${application.distrib}, que es una variable que contiene la ruta en la que el servicio de distribución IcePatch2 colocará los ficheros. Por tanto, es necesario ejecutar primero la distribución. Esto requiere dos pasos:

1. Preparar los ficheros. Por ejemplo para hello.ice/py se puede hacer con:

    py$ make gen-dist

que crea un directorio py/dist con los archivos listos para la distribución y un enlace en /tmp/printer-py, que facilita la configuración de IcePatch2.

2. Ejecutar la distribución en sí.

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application patch PrinterApp"

Todos los detalles de la configuración de IcePatch2 los puedes comprobar mirando directamente la descripción en el fichero XML o cargándolo con icegridgui.

Arrancar los servidores (ya que tienen activación manual):

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer1"
    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer2"

Puedes ver la salida de los servidores (dónde aparece el proxy del objeto) con:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter

Por último, puedes invocar el servidor PrinterServer1 con:

    $ ../py/client.py --Ice.Config=locator.config "printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter"

Y comprobar que se ha ejecutado mirando de nuevo la salida del servidor:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter
    0: Hello World!
