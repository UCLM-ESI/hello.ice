[["ice-prefix"]]
module IceCloud {

  dictionary<string, string> Parameters;
  exception CreationError { string reason; };

  interface ServerFactory {
    Object* make(string node, string serverTemplate, Parameters params)
      throws CreationError;
  };
};
