#include <Printer.ice>

module Example {
  interface PrinterFactory {
    Printer* make(string name);
  };
};
