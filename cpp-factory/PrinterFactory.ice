#include <printer.ice>

module Example {
  interface PrinterFactory {
    Printer* make(string name);
  };
};
