[["ice-prefix"]]
module IceCloud {

  dictionary<string, string> Parameters;
  exception CreationError{};

  interface Factory {
    Object* make(string node, string serverTemplate, Parameters params)
      throws CreationError;
  };
};
