module UCLM {
  interface Hello {
    ["freeze:write"]
    void puts(string str);
  };

  class HelloPersistent implements Hello {
    int useCount;
  };
};

