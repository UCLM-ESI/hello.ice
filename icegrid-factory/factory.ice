#include "printer.ice"

module Example {
  exception FactoryError { string reason; };

  interface PrinterFactory {
    Printer* make(string serverName) throws FactoryError;
  };
};
